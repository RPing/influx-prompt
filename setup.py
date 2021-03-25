import re
from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


def find_version(*file_paths):
    # from https://github.com/eliangcs/http-prompt/blob/master/setup.py
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, *file_paths), "r", "latin1") as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string")


setup(
    name="influx-prompt",
    version=find_version("influx_prompt", "__init__.py"),
    description="An interactive command-line influxdb cli with auto completion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RPing/influx-prompt",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Terminals",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="influx influxdb cli",
    packages=["influx_prompt"],
    zip_safe=False,
    author="Stephen Chen (RPing)",
    author_email="g1222888@gmail.com",
    install_requires=[
        "requests~=2.24",
        "prompt-toolkit~=3.0",
        "jsane~=0.1",
        "fuzzyfinder~=2.1",
        "pygments~=2.7",
    ],
    entry_points={"console_scripts": ["influx-prompt = influx_prompt.main:cli"],},
)
