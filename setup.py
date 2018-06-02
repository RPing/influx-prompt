import re
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]

def find_version(*file_paths):
    # from https://github.com/eliangcs/http-prompt/blob/master/setup.py
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string')

setup(
    name='influx-prompt',
    version=find_version('influx_prompt', '__init__.py'),
    description='An interactive command-line influxdb cli with auto completion.',
    long_description=long_description,
    url='https://github.com/RPing/influx-prompt',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Terminals',
        'Topic :: Text Processing',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
    ],
    keywords='influx influxdb cli',
    packages=['influx_prompt'],
    zip_safe = False,
    author='Stephen Chen (RPing)',
    author_email='g1222888@gmail.com',
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['influx-prompt = influx_prompt.main:cli'],
    },
)
