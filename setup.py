from setuptools import setup, find_packages


with open('README.rst', 'r') as fp:
    long_description = fp.read()

with open('requirements.txt', 'r') as fp:
    requirements = fp.read().splitlines()

with open('requirements-redis-helper.txt', 'r') as fp:
    requirements_redis_helper = fp.read().splitlines()

setup(
    name='yt-helper',
    version='0.2.10',
    description='Light wrapper to youtube-dl with a simplified CLI for downloading media',
    long_description=long_description,
    author='Ken',
    author_email='kenjyco@gmail.com',
    license='MIT',
    url='https://github.com/kenjyco/yt-helper',
    download_url='https://github.com/kenjyco/yt-helper/tarball/v0.2.10',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'redis-helper': requirements_redis_helper,
    },
    include_package_data=True,
    package_dir={'': '.'},
    package_data={
        '': ['*.ini'],
    },
    entry_points={
        'console_scripts': [
            'yt-download=yt_helper.scripts.download:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
    keywords=['youtube-dl', 'youtube', 'ffmpeg', 'sox', 'rtmpdump', 'video', 'audio', 'cli', 'command-line', 'download', 'helper', 'kenjyco']
)
