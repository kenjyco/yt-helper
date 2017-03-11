from setuptools import setup, find_packages


setup(
    name='yt-helper',
    version='0.1.3',
    description='Light wrapper to youtube-dl',
    author='Ken',
    author_email='kenjyco@gmail.com',
    license='MIT',
    url='https://github.com/kenjyco/yt-helper',
    download_url='https://github.com/kenjyco/yt-helper/tarball/v0.1.3',
    packages=find_packages(),
    install_requires=[
        'youtube-dl',
        'click',
        'input-helper',
    ],
    include_package_data=True,
    package_dir={'': '.'},
    package_data={
        '' : ['*.ini'],
    },
    entry_points={
        'console_scripts': [
            'yt-download=yt_helper.scripts.download:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: Developers',
    ],
    keywords = ['youtube-dl', 'youtube', 'download']
)
