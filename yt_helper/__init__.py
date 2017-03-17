from __future__ import unicode_literals
import os
import logging
from glob import glob
from pprint import pprint
import youtube_dl

"""
See:

- https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
- https://github.com/rg3/youtube-dl/issues/6584
"""


LOGFILE = 'log--yt-helper.log'
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


def my_hook(d):
    if d['status'] == 'finished':
        logger.info('Downloaded {} ({}) in {}'.format(
            d.get('filename', 'unknown file'),
            d.get('_total_bytes_str', 'unknown bytes'),
            d.get('_elapsed_str', 'unknown time'),
        ))


def av_from_url(url, **kwargs):
    """Download audio and/or video from a URL with `youtube-dl`

    - playlist: if True, allow downloading entire playlist
    - thumbnail: if True, download thumbnail image of video
    - description: if True, download description of video to a file
    - subtitles: if True, embed subtitles in downloaded video (if available)
    - template: string representing generated filenames
    - audio_only: if True, don't keep the video file if one is downloaded
    - mp3: if True, convert downloaded audio to MP3 file
    """
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
        'format': 'bestvideo+bestaudio/best',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
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
        formats = info.pop('formats', None)
        logger.info('Fetching {}'.format(url))
        ydl.download([url])

    delete_all_extra_files()
    for key in (
        'age_limit',
        'annotations',
        'automatic_captions',
        'episode_number',
        'format_id',
        'format_note',
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
    ):
        info.pop(key, None)

    with open(LOGFILE, 'a') as fp:
        pprint(info, fp)

    return info
