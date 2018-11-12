import pytest

from .utils import (
    HOST, USER, PASSWORD, PORT,
    DATABASE, SSL, SSLCERT, TIMEOUT, RETRY,
    HIDE_INVALID_SSL_WARNINGS,
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
        'hide_invalid_ssl_warnings': HIDE_INVALID_SSL_WARNINGS,
    }
