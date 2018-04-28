import time
import random

import json
import requests
import jsane

from .exceptions import InfluxDBServerError

class Client(object):
    get_sql_keywords = ['SELECT', 'SHOW']
    post_sql_keywords = ['ALTER', 'CREATE', 'DELETE', 'DROP', 'GRANT', 'KILL', 'REVOKE']

    def __init__(self, args):
        self.host = args['host']
        self.port = args['port']
        self.username = args['username']
        self.password = args['password']
        self.database = args['database']
        self.ssl = args['ssl']
        self.verify_ssl = args['ssl_cert']
        self.timeout = args['timeout']
        self.retries = args['retry']
        self._session = requests.Session()
        self._scheme = 'http' if self.ssl is False else 'https'
        self._baseurl = "{0}://{1}:{2}".format(
            self._scheme,
            self.host,
            self.port
        )
        self._headers = {
            'Content-Type': 'application/json',
            'Accept': 'text/plain'
        }

    def query(self, q, database=None, epoch=None):
        """borrow from influxdb-python"""
        url = "{0}/{1}".format(self._baseurl, 'query')
        method = self._get_http_method(q)

        params = {}
        params['q'] = q
        params['db'] = database or self.database

        if epoch is not None:
            params['epoch'] = epoch

        retry = True
        _try = 0
        while retry:
            try:
                response = self._session.request(
                    method=method,
                    url=url,
                    auth=(self.username, self.password),
                    params=params,
                    headers=self._headers,
                    verify=self.verify_ssl,
                    timeout=self.timeout,
                    # data=data,
                    # proxies=self._proxies,
                )
                break
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.HTTPError,
                    requests.exceptions.Timeout):
                _try += 1
                if self._retries != 0:
                    retry = _try < self.retries
                if method == 'POST':
                    time.sleep((2 ** _try) * random.random() / 100.0)
                if not retry:
                    raise

        if 500 <= response.status_code < 600:
            raise InfluxDBServerError(response.content)
        else:
            j = response.json()
            return j

    def _get_http_method(self, q):
        first_word = q.split()[0].upper()

        if first_word in self.get_sql_keywords:
            return 'GET'
        elif first_word in self.post_sql_keywords:
            return 'POST'
        else:
            return 'POST'
