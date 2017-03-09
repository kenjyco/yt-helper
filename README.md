## Install

```
% pip install yt-helper
```

## Usage

The `yt-download` script is provided

```
% venv/bin/yt-download --help
Usage: yt-download [OPTIONS] [ARGS]...

  Wrapper to 'av_from_url'

  - args: urls or filenames containing urls

Options:
  -o, --template TEXT  string representing generated filenames
  -p, --playlist       Allow downloading entire playlist
  -q, --quiet          Don't print messages to stdout
  -t, --thumbnail      Download thumbnail image of video
  -d, --description    Download description of video to a file
  -s, --subtitles      Embed subtitles in the downloaded video
  -a, --audio-only     Don't keep the video file if one was downloaded
  -m, --mp3            Convert downloaded audio to MP3 file
  --help               Show this message and exit.
```
