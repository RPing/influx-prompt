class InfluxDBServerError(Exception):
    """Raised when a server error occurs. Borrow from influxdb-python."""

    def __init__(self, content):
        """Initialize the InfluxDBServerError handler."""
        super(InfluxDBServerError, self).__init__(content)
