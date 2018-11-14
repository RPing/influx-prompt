from __future__ import absolute_import, unicode_literals
import re
import time
import random

import requests


class Client(object):
    get_sql_keywords = ['SELECT', 'SHOW']
    post_sql_keywords = ['ALTER', 'CREATE', 'DELETE',
                         'DROP', 'GRANT', 'KILL', 'REVOKE']

    def __init__(self, args):
        self.host = args['host']
        self.port = args['port']
        self.username = args['username']
        self.password = args['password']
        self.database = args['database']
        self.ssl = args['ssl']
        self.verify_ssl = args['ssl_cert']
        self.hide_invalid_ssl_warnings = args['hide_invalid_ssl_warnings']
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
        """borrow some code from influxdb-python"""
        request_args = self._make_request_args(q, database, epoch)

        retry = True
        _try = 0
        while retry:
            try:
                if self.hide_invalid_ssl_warnings:
                    requests.packages.urllib3.disable_warnings()
                response = self._session.request(**request_args)
                break
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.HTTPError,
                    requests.exceptions.Timeout):
                _try += 1
                if self.retries != 0:
                    retry = _try < self.retries
                if request_args['method'] == 'POST':
                    time.sleep((2 ** _try) * random.random() / 100.0)
                if not retry:
                    raise

        if response.status_code == 204:
            return {}
        else:
            j = response.json()
            return j

    def ping(self):
        url = "{0}/{1}".format(self._baseurl, 'ping')

        if self.hide_invalid_ssl_warnings:
            requests.packages.urllib3.disable_warnings()

        requests.head(url, verify=self.verify_ssl)

    def _make_request_args(self, q, database, epoch):
        first_word = q.split()[0].upper()

        params = {}
        params['q'] = q
        params['db'] = database or self.database

        if first_word == 'INSERT':
            m = re.search(r"INSERT\s(?P<write_cmd>.+);?", q, re.IGNORECASE)
            write_cmd = m.group('write_cmd')
            url = "{0}/{1}".format(self._baseurl, 'write')
            method = 'POST'

            if epoch is not None:
                params['precision'] = epoch

            return {
                'method': method,
                'url': url,
                'auth': (self.username, self.password),
                'params': params,
                'headers': self._headers,
                'verify': self.verify_ssl,
                'timeout': self.timeout,
                'data': write_cmd,
            }

        if epoch is not None:
            params['epoch'] = epoch

        if first_word in self.get_sql_keywords:
            url = "{0}/{1}".format(self._baseurl, 'query')
            method = 'GET'
        elif first_word in self.post_sql_keywords:
            url = "{0}/{1}".format(self._baseurl, 'query')
            method = 'POST'
        else:  # unknown command.
            return {
                'method': 'POST',
                'url': "{0}/{1}".format(self._baseurl, 'query'),
                'auth': (self.username, self.password),
                'params': params,
                'headers': self._headers,
                'verify': self.verify_ssl,
                'timeout': self.timeout,
            }

        return {
            'method': method,
            'url': url,
            'auth': (self.username, self.password),
            'params': params,
            'headers': self._headers,
            'verify': self.verify_ssl,
            'timeout': self.timeout,
        }
