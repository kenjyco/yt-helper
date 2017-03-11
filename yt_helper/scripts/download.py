import click
import input_helper as ih
import yt_helper as yh


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
        results.append(yh.av_from_url(url, **kwargs))
    yh.delete_all_extra_files()

    from pprint import pprint
    with open(yh.LOGFILE, 'a') as fp:
        pprint(results, fp)


if __name__ == '__main__':
    main()
