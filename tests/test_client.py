import random
import requests

import pytest
import mock

from .utils import create_test_db, drop_test_db, select_test_db, ping, MockRequest
from influx_prompt.influx_client import Client


is_influx_running = True
try:
    ping()
except (requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        requests.exceptions.Timeout):
    is_influx_running = False

pytestmark = pytest.mark.skipif(
    not is_influx_running,
    reason="InfluxDB has not running yet.")


def setup_module():
    create_test_db()


def teardown_module():
    drop_test_db()


@pytest.fixture
def client(default_args):
    return Client(default_args)

@pytest.fixture
def client_ssl_warning_hidden(default_args):
    default_args["hide_invalid_ssl_warnings"] = True
    return Client(default_args)


def test_ping(client):
    client.ping()
    assert True

def test_ping_ssl_warning_hidden(client_ssl_warning_hidden):
    client_ssl_warning_hidden.ping()
    assert True

def test_insert(client):
    client.query('INSERT mymeas,mytag=12 myfield=91 1434055562000000000',
                 database='_test_db')
    # use requests to inspect it first.
    result = select_test_db('mymeas')
    assert result == {
        'results': [{
            'statement_id': 0,
            'series': [{
                'name': 'mymeas',
                'columns': ['time', 'myfield', 'mytag'],
                'values': [['2015-06-11T20:46:02Z', 91, '12']]
            }]
        }]
    }


def test_select(client):
    result = client.query('SELECT * FROM mymeas', database='_test_db')
    assert result == {
        'results': [{
            'statement_id': 0,
            'series': [{
                'name': 'mymeas',
                'columns': ['time', 'myfield', 'mytag'],
                'values': [['2015-06-11T20:46:02Z', 91, '12']]
            }]
        }]
    }


def test_select_with_epoch(client):
    result = client.query('SELECT * FROM mymeas',
                          database='_test_db', epoch='h')
    assert result == {
        'results': [{
            'statement_id': 0,
            'series': [{
                'name': 'mymeas',
                'columns': ['time', 'myfield', 'mytag'],
                'values': [[398348, 91, '12']]
            }]
        }]
    }


def test_delete(client):
    client.query('DELETE FROM mymeas', database='_test_db')
    result = select_test_db('mymeas')
    assert result == {
        'results': [{
            'statement_id': 0
        }]
    }


def test_insert_with_epoch(client):
    client.query('INSERT mymeas,mytag=12 myfield=91 398348',
                 database='_test_db', epoch='h')
    result = select_test_db('mymeas')
    assert result == {
        'results': [{
            'statement_id': 0,
            'series': [{
                'name': 'mymeas',
                'columns': ['time', 'myfield', 'mytag'],
                'values': [['2015-06-11T20:00:00Z', 91, '12']]
            }]
        }]
    }


@mock.patch('requests.Session.request')
def test_random_request_retry(mock_request, client):
    retries = random.randint(2, 3)
    mock_request.side_effect = MockRequest(retries).connection_error
    client.query('DELETE FROM mymeas', database='_test_db')
    mock_request.assert_called()


@mock.patch('requests.Session.request')
def test_exceed_retry(mock_request, client):
    retries = 4
    mock_request.side_effect = MockRequest(retries).connection_error
    with pytest.raises(requests.exceptions.ConnectionError):
        client.query('DELETE FROM mymeas', database='_test_db')


def test_unknown_query(client):
    result = client.query('I AM RPING, I COME FROM TAIWAN.')
    assert result == {
        'error': 'error parsing query: '
                 'found I, expected SELECT, DELETE, SHOW, CREATE, DROP, '
                 'EXPLAIN, GRANT, REVOKE, ALTER, SET, KILL '
                 'at line 1, char 1'
    }


def test_unknown_query_ssl_warning_hidden(client_ssl_warning_hidden):
    result = client_ssl_warning_hidden.query('I AM RPING, I COME FROM TAIWAN.')
    assert result == {
        'error': 'error parsing query: '
                 'found I, expected SELECT, DELETE, SHOW, CREATE, DROP, '
                 'EXPLAIN, GRANT, REVOKE, ALTER, SET, KILL '
                 'at line 1, char 1'
    }
