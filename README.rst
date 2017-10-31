Install
-------

Install system av tools

::

    % sudo apt-get install -y libav-tools sox rtmpdump

    or

    % brew install libav sox rtmpdump

Install with ``pip``

::

    % pip3 install yt-helper

Usage
-----

The ``yt-download`` and ``yt-search`` scripts are provided

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

Optional Installs
-----------------

yt-search
~~~~~~~~~

In order to use the ``yt-search`` command, you must also install the
``parse-helper`` package and it’s dependencies.

Install system requirements for ``lxml``

::

    % sudo apt-get install -y libxml2 libxslt1.1 libxml2-dev libxslt1-dev zlib1g-dev

    or

    % brew install libxml2

Install with ``pip``

::

    % pip3 install parse-helper

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
