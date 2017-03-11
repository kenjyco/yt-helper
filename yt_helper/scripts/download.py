from __future__ import unicode_literals
import os
import re
import logging
import click
import input_helper as ih
from glob import glob
import youtube_dl

"""
See:

- https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
- https://github.com/rg3/youtube-dl/issues/6584
"""


LOGFILE = 'log--yt-helper.log'
logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(funcName)s: %(message)s',
        level=logging.DEBUG,
        filename=LOGFILE,
        filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def delete_all_extra_files(path='.'):
    for fname in glob(os.path.join(path, '*.f???.*')):
        os.remove(fname)
        logging.debug('Removed {}'.format(repr(fname)))
    for fname in glob(os.path.join(path, '**/*.f???.*')):
        os.remove(fname)
        logging.debug('Removed {}'.format(repr(fname)))


class MyLogger(object):
    def debug(self, msg):
        logging.debug(msg)

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

    def info(self, msg):
        logging.info(msg)


def my_hook(d):
    if d['status'] == 'finished':
        logging.info('Downloaded {} ({}) in {}'.format(
            d.get('filename', 'unknown file'),
            d.get('_total_bytes_str', 'unknown bytes'),
            d.get('_elapsed_str', 'unknown time'),
        ))


def av_from_url(url, **kwargs):
    """Download audio and/or video from a URL with `youtube-dl`

    - playlist: if True, allow downloading entire playlist
    - quiet: if True, don't print messages to stdout
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
        'quiet': kwargs.get('quiet', True),
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
    if kwargs.get('mp3', True):
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
        logging.info('Fetching {}'.format(url))
        ydl.download([url])

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

    return info


@click.command()
@click.option(
    '--template', '-o', 'template', default='',
    help='string representing generated filenames'
)
@click.option(
    '--playlist', '-p', 'playlist', is_flag=True, default=False,
    help='Allow downloading entire playlist'
)
@click.option(
    '--thumbnail', '-t', 'thumbnail', is_flag=True, default=False,
    help='Download thumbnail image of video'
)
@click.option(
    '--description', '-d', 'description', is_flag=True, default=False,
    help='Download description of video to a file'
)
@click.option(
    '--subtitles', '-s', 'subtitles', is_flag=True, default=False,
    help='Embed subtitles in the downloaded video'
)
@click.option(
    '--audio-only', '-a', 'audio_only', is_flag=True, default=False,
    help='Don\'t keep the video file if one was downloaded'
)
@click.option(
    '--mp3', '-m', 'mp3', is_flag=True, default=False,
    help='Convert downloaded audio to MP3 file'
)
@click.argument('args', nargs=-1)
def main(**kwargs):
    """Wrapper to 'av_from_url'

    - args: urls or filenames containing urls
    """
    args = kwargs.pop('args')
    urls = ih.get_all_urls(*args)
    results = []
    for url in urls:
        results.append(av_from_url(url, **kwargs))
    delete_all_extra_files()

    from pprint import pprint
    with open(LOGFILE, 'a') as fp:
        pprint(results, fp)


if __name__ == '__main__':
    main()
