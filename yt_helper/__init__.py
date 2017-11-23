from __future__ import unicode_literals
import os
import re
import logging
from glob import glob
from pprint import pprint
from functools import partial
from urllib.parse import urlparse
import youtube_dl
try:
    import redis_helper as rh
    import input_helper as ih
    from redis import ConnectionError as RedisConnectionError

except ImportError:
    QUERIES = None
    URLS = None
    FILES = None
    AUDIO_COMMENTS = None
    VIDEO_COMMENTS = None
else:
    try:
        QUERIES = rh.Collection(
            'av',
            'query',
            unique_field='query',
            json_fields='basenames,related',
            insert_ts=True,
        )

        URLS = rh.Collection(
            'av',
            'url',
            unique_field='url',
            index_fields='domain',
            json_fields='basenames',
            insert_ts=True,
        )

        FILES = rh.Collection(
            'av',
            'file',
            unique_field='basename',
            index_fields='vid,audio',
            json_fields='queries_in,queries_out,exts,yt',   # queries & exts are lists, yt is dict of info
            insert_ts=True,
        )

        AUDIO_COMMENTS = rh.Collection(
            'audio',
            'comment',
            index_fields='basename',
            json_fields=','.join(ih.SPECIAL_TEXT_RETURN_FIELDS),
            insert_ts=True,
        )

        VIDEO_COMMENTS = rh.Collection(
            'vid',
            'comment',
            index_fields='basename',
            json_fields=','.join(ih.SPECIAL_TEXT_RETURN_FIELDS),
            insert_ts=True,
        )
    except RedisConnectionError:
        QUERIES = None
        URLS = None
        FILES = None
        AUDIO_COMMENTS = None
        VIDEO_COMMENTS = None

"""
See:

- https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
- https://github.com/rg3/youtube-dl/issues/6584
"""


LOGFILE = os.path.abspath('log--yt-helper.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOGFILE, mode='a')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(funcName)s: %(message)s'
))
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
logger.addHandler(file_handler)
logger.addHandler(console_handler)
IGNORE_INFO_KEYS = (
    'age_limit',
    'annotations',
    'automatic_captions',
    'episode_number',
    'format_id',
    'format_note',
    'formats',
    'http_headers',
    'is_live',
    'license',
    'player_url',
    'preference',
    'protocol',
    'requested_subtitles',
    'requested_formats',
    'season_number',
    'series',
    'start_time',
    'vcodec',
    'webpage_url',
    'webpage_url_basename',
)


def get_real_basename(filename=''):
    """Return basename of filename, removing extension and any `*.f???` component"""
    if filename:
        basename, ext = os.path.splitext(os.path.basename(filename))
        return re.sub(r'(^.*)\.f\d+$', r'\1', basename)
    return ''


def delete_all_extra_files(path='.'):
    for fname in glob(os.path.join(path, '*.f???.*')):
        os.remove(fname)
        logger.debug('Removed {}'.format(repr(fname)))
    for fname in glob(os.path.join(path, '**/*.f???.*')):
        os.remove(fname)
        logger.debug('Removed {}'.format(repr(fname)))


class MyLogger(object):
    def debug(self, msg):
        logger.debug(msg)

    def warning(self, msg):
        logger.warning(msg)

    def error(self, msg):
        logger.error(msg)

    def info(self, msg):
        logger.info(msg)


def my_hook(d, url='', query='', dirname='', vid='', audio=''):
    if d['status'] == 'finished':
        filename = d.get('filename', '')
        logger.info('Downloaded {} ({}) in {}'.format(
            filename or 'unknown file',
            d.get('_total_bytes_str', 'unknown bytes'),
            d.get('_elapsed_str', 'unknown time'),
        ))
        basename = get_real_basename(filename)
        if FILES is not None:
            try:
                FILES.add(
                    basename=basename,
                    url=url,
                    vid=vid,
                    audio=audio,
                    queries_in=[query],
                    dirname=dirname,
                )
            except AssertionError:
                hash_id = FILES.get_hash_id_for_unique_value(basename)
                queries_in = FILES.get(
                    hash_id,
                    'queries_in',
                    update_get_stats=False
                )['queries_in']
                if query not in queries_in:
                    queries_in.append(query)
                FILES.update(
                    hash_id,
                    url=url,
                    vid=vid,
                    audio=audio,
                    queries_in=queries_in,
                    dirname=dirname,
                )
        if QUERIES is not None and query is not '':
            try:
                QUERIES.add(
                    query=query,
                    basenames=[basename],
                )
            except AssertionError:
                hash_id = QUERIES.get_hash_id_for_unique_value(query)
                basenames = QUERIES.get(
                    hash_id,
                    'basenames',
                    update_get_stats=False
                )['basenames']
                if basename not in basenames:
                    basenames.append(basename)
                QUERIES.update(
                    hash_id,
                    basenames=basenames
                )
        if URLS is not None and url is not '':
            domain = urlparse(url).netloc.replace('www.', '')
            try:
                URLS.add(
                    url=url,
                    domain=domain,
                    basenames=[basename],
                )
            except AssertionError:
                hash_id = URLS.get_hash_id_for_unique_value(url)
                basenames = URLS.get(
                    hash_id,
                    'basenames',
                    update_get_stats=False
                )['basenames']
                if basename not in basenames:
                    basenames.append(basename)
                URLS.update(
                    hash_id,
                    basenames=basenames
                )


def av_from_url(url, **kwargs):
    """Download audio and/or video from a URL with `youtube-dl`

    - playlist: if True, allow downloading entire playlist
    - thumbnail: if True, download thumbnail image of video
    - description: if True, download description of video to a file
    - max_height: maximum height of video (i.e. 1080, 720, 480, 240.. default 720)
    - subtitles: if True, embed subtitles in downloaded video (if available)
    - template: string representing generated filenames
    - audio_only: if True, don't keep the video file if one is downloaded
    - mp3: if True, convert downloaded audio to MP3 file
    - logger: a logger object with `debug`, `warning`, `error`, `info` methods
      that accept a message string and do something with it
    - hook: progress hook function that accepts a single positional argument
      (dict of info from youtube-dl; check 'status' key)
      and optional kwargs (for receiving 'url', 'query', and 'dirname')
    - query: the search query that produced 'url' in the results
    """
    try:
        max_height = int(kwargs.get('max_height', 720))
    except ValueError:
        max_height = 720
    hook = partial(
        kwargs.get('hook', my_hook),
        url=url,
        vid=not kwargs.get('audio_only'),
        audio=kwargs.get('audio_only') or kwargs.get('mp3'),
        query=kwargs.get('query', ''),
        dirname=os.getcwd(),
    )
    ydl_opts = {
        'restrictfilenames': True,
        'ignoreerrors': True,
        'noplaylist': not kwargs.get('playlist', False),
        'quiet': True,
        'writethumbnail': kwargs.get('thumbnail', False),
        'writedescription': kwargs.get('description', False),
        'writesubtitles': kwargs.get('subtitles', False),
        'keepvideo': True,
        # 'format': 'bestvideo[ext!=webm]+bestaudio[ext!=webm]/best[ext!=webm]',
        'format': 'bestvideo[height<=?{height}]+bestaudio/best[height<=?{height}]'.format(height=max_height),
        'logger': kwargs.get('logger', MyLogger()),
        'progress_hooks': [hook],
    }
    if 'template' in kwargs and kwargs['template']:
        ydl_opts.update({'outtmpl': kwargs['template']})
    if kwargs.get('audio_only', False):
        ydl_opts.update({
            'keepvideo': False,
            # 'format': 'bestaudio[ext!=webm]/best[ext!=webm]',
            'format': 'bestaudio/best',
        })
    if kwargs.get('mp3', False):
        ydl_opts.update({
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        })

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        logger.info('Fetching {}'.format(url))
        ydl.download([url])

    delete_all_extra_files()
    if info:
        for key in IGNORE_INFO_KEYS:
            info.pop(key, None)
        if 'entries' in info:
            # Playlist link was processed
            info['entries'] = [
                {
                    k: v
                    for k, v in entry.items()
                    if k not in IGNORE_INFO_KEYS
                }
                for entry in info['entries'] if entry
            ]

        with open(LOGFILE, 'a') as fp:
            pprint(info, fp)

    return info


from yt_helper import legacy
