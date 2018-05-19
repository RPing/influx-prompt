import os

import requests
import pytest

USER = os.getenv('PYTEST_USER', 'root')
PASSWORD = os.getenv('PYTEST_PASSWORD', 'root')
HOST = os.getenv('PYTEST_HOST', 'localhost')
PORT = os.getenv('PYTEST_PORT', 8086)
DATABASE = os.getenv('PYTEST_DATABASE', None)
SSL = os.getenv('PYTEST_SSL', False)
SSLCERT = os.getenv('PYTEST_SSLCERT', False)
TIMEOUT = os.getenv('PYTEST_TIMEOUT', None)
RETRY = os.getenv('PYTEST_RETRY', 3)


def ping():
    baseurl = "http://{0}:{1}".format(HOST, PORT)
    url = baseurl + '/ping'

    requests.head(url)

def create_test_db():
    params = {}
    params['q'] = 'CREATE DATABASE _test_db'
    baseurl = "http://{0}:{1}".format(HOST, PORT)
    url = baseurl + '/query'

    requests.post(url, params=params)

def drop_test_db():
    params = {}
    params['q'] = 'DROP DATABASE _test_db'
    baseurl = "http://{0}:{1}".format(HOST, PORT)
    url = baseurl + '/query'

    requests.post(url, params=params)

def select_test_db(measure):
    params = {}
    params['q'] = 'SELECT * FROM ' + measure
    params['db'] = '_test_db'
    baseurl = "http://{0}:{1}".format(HOST, PORT)
    url = baseurl + '/query'

    result = requests.get(url, params=params)
    return result.json()
