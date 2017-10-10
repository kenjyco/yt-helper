## Install

Install system av tools

```
% sudo apt-get install -y libav-tools sox rtmpdump

or

% brew install libav sox rtmpdump
```

Install with `pip`

```
% pip install yt-helper
```

## Usage

The `yt-download` and `yt-search` scripts are provided

```
% venv/bin/yt-download --help
Usage: yt-download [OPTIONS] [ARGS]...

  Wrapper to 'av_from_url'

  - args: urls or filenames containing urls

Options:
  -o, --template TEXT       string representing generated filenames
  -h, --max-height INTEGER  maximum height of video (i.e. 1080, 720, 480,
                            240.. default 720)
  -p, --playlist            Allow downloading entire playlist
  -t, --thumbnail           Download thumbnail image of video
  -d, --description         Download description of video to a file
  -s, --subtitles           Embed subtitles in the downloaded video
  -a, --audio-only          Don't keep the video file if one was downloaded
  -m, --mp3                 Convert downloaded audio to MP3 file
  --help                    Show this message and exit.

% venv/bin/yt-search --help
Usage: yt-search [OPTIONS] [QUERY]

  Pass a search query to google and attempt to download selected audio/vid

Options:
  --page INTEGER                  page number of results
  --since [|year|month|week|day]  limit results by time
  --site TEXT                     limit results by site/domain (default
                                  youtube.com)
  -h, --max-height INTEGER        maximum height of video (i.e. 1080, 720,
                                  480, 240.. default 720)
  -s, --subtitles                 Embed subtitles in the downloaded video
  -a, --audio-only                Don't keep the video file if one was
                                  downloaded
  --help                          Show this message and exit.
```

> Note: to use `yt-search`, you must also install `parse-helper`. See
> [parse-helper README](https://github.com/kenjyco/parse-helper/blob/master/README.md).
