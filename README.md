influx-prompt
===============================
[![PyPI version](https://badge.fury.io/py/influx-prompt.svg)](https://badge.fury.io/py/influx-prompt)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/influx-prompt.svg)](https://pypi.python.org/pypi/influx-prompt/)
[![Build Status](https://travis-ci.org/RPing/influx-prompt.svg?branch=master)](https://travis-ci.org/RPing/influx-prompt)
[![codecov](https://codecov.io/gh/RPing/influx-prompt/branch/master/graph/badge.svg)](https://codecov.io/gh/RPing/influx-prompt)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<img src="screenshot.gif" />

Overview
--------

An interactive command-line InfluxDB cli.

Inspired by [pgcli](https://github.com/dbcli/pgcli), [http-prompt
](https://github.com/eliangcs/http-prompt)

Requirement
--------
Python 3.6+, *nix system.

It hasn't tested on Windows.

Installation
--------------------

To install use pip:

    $ pip install influx-prompt

Or clone the repo:

    $ git clone https://github.com/RPing/influx-prompt.git
    $ python setup.py install

Usage
------------
influx-prompt `-h` / `--help` to list all options.

Ctrl+d / `exit` to exit.

Dead simple.

Contributing
------------

1. Fork to your repo
2. install `pipenv`
3. `pipenv shell`
4. `pipenv install --dev`
5. Finish your work, and use `tox` & `flake8` to test.
6. Pull requests!


Author
------------

A man who can't live without autocomplete, [Stephen Chen](https://github.com/RPing)

Related Projects
------------
- [pgcli](https://github.com/dbcli/pgcli)
- [mycli](https://github.com/dbcli/mycli)

Thanks
------------
[python-prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit), and of course, [InfluxDB](https://www.influxdata.com).


License
------------

MIT
