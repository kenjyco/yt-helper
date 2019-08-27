Install
-------

Install system av tools

::

   % sudo apt-get install -y sox rtmpdump
   % sudo apt-get install -y libav-tools
   % [[ $? -ne 0 ]] && sudo apt-get install -y ffmpeg

   or

   % brew install libav sox rtmpdump

Install with ``pip``

::

   % pip3 install yt-helper

Usage
-----

The ``yt-download`` script is provided

::

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

Optional Installs
-----------------

Collections/models (QUERIES, URLS, FILES, COMMENTS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to make use of the ``QUERIES``, ``URLS``, ``FILES``, and
``COMMENTS`` collections, you must also install the ``redis-helper``
package and have a Redis server running.

If the collections/models are available, some functions will save
relevant info to them.

   See: https://github.com/kenjyco/redis-helper#intro

Install Redis and start server

::

   % sudo apt-get install -y redis-server

   or

   % brew install redis@3.2
   % brew services start redis@3.2

Install with ``pip``

::

   % pip3 install redis-helper
