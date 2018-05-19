import pytest
import requests

from .utils import (
    HOST, USER, PASSWORD, PORT,
    DATABASE, SSL, SSLCERT, TIMEOUT, RETRY,
)

@pytest.fixture
def default_args():
    return {
        'host': HOST,
        'port': PORT,
        'username': USER,
        'password': PASSWORD,
        'database': DATABASE,
        'ssl': SSL,
        'ssl_cert': SSLCERT,
        'timeout': TIMEOUT,
        'retry': RETRY,
    }
