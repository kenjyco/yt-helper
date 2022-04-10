from setuptools import setup, find_packages


with open('README.rst', 'r') as fp:
    long_description = fp.read()

with open('requirements.txt', 'r') as fp:
    requirements = fp.read().splitlines()

with open('requirements-redis-helper.txt', 'r') as fp:
    requirements_redis_helper = fp.read().splitlines()

setup(
    name='yt-helper',
    version='0.2.9',
    description='Light wrapper to youtube-dl',
    long_description=long_description,
    author='Ken',
    author_email='kenjyco@gmail.com',
    license='MIT',
    url='https://github.com/kenjyco/yt-helper',
    download_url='https://github.com/kenjyco/yt-helper/tarball/v0.2.9',
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
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: Developers',
    ],
    keywords = ['youtube-dl', 'youtube', 'download']
)
