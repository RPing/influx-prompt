import json

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError

class Client(object):
    def __init__(self, args):
        self.executor = InfluxDBClient(
            host=args['host'],
            port=args['port'],
            username=args['username'],
            password=args['password'],
            database=args['database'],
            ssl=args['ssl'],
            verify_ssl=args['ssl_cert'],
            timeout=args['timeout'],
            retries=args['retry'],
        )

    def query(self, q, epoch, database):
        try:
            return self.executor.query(q, epoch=epoch, database=database)
        except InfluxDBClientError as e:
            return json.loads(e.content)
