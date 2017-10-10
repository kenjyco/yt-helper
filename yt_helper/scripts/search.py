import click
import yt_helper as yh
import input_helper as ih
try:
    import parse_helper as ph
except ImportError:
    ph = None


@click.command()
@click.argument('query', nargs=1, default='')
@click.option(
    '--page', 'page', default=1, type=click.INT,
    help='page number of results'
)
@click.option(
    '--since', 'since', default='', type=click.Choice([
        '', 'year', 'month', 'week', 'day'
    ]),
    help='limit results by time'
)
@click.option(
    '--site', 'site', default='youtube.com',
    help='limit results by site/domain (default youtube.com)'
)
@click.option(
    '--max-height', '-h', 'max_height', default=720,
    help='maximum height of video (i.e. 1080, 720, 480, 240.. default 720)'
)
@click.option(
    '--subtitles', '-s', 'subtitles', is_flag=True, default=False,
    help='Embed subtitles in the downloaded video'
)
@click.option(
    '--audio-only', '-a', 'audio_only', is_flag=True, default=False,
    help='Don\'t keep the video file if one was downloaded'
)
def main(query, **kwargs):
    """Pass a search query to google and attempt to download selected audio/vid"""
    if not ph:
        print('You must install parse-helper first.')
        print('See https://github.com/kenjyco/parse-helper/blob/master/README.md')
        return

    query = query or ih.user_input('google query')
    if not query:
        return

    page = kwargs.pop('page')
    since = kwargs.pop('since')
    site = kwargs.pop('site')
    session = ph.new_requests_session()
    selected = ih.make_selections(
        ph.google_serp(query, session=session, page=page, since=since, site=site),
        wrap=False,
        item_format='{title} .::. {link}',
    )

    av_kwargs = {
        'query': query,
        'playlist': True
    }
    if kwargs['audio_only']:
        av_kwargs.update({
            'audio_only': True,
            'mp3': True
        })
    else:
        av_kwargs.update({
            'max_height': kwargs['max_height'],
            'subtitles': kwargs['subtitles']
        })

    if selected:
        results = [
            yh.av_from_url(x['link'], **av_kwargs)
            for x in selected
        ]
        return results
