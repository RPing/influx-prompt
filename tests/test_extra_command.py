import pytest

from influx_cli.extra_command import process_extra_command

def test_use_database(default_args):
    msg = process_extra_command(default_args, 'use TEST')
    assert default_args['database'] == 'TEST'
    assert msg == 'database now set to TEST'

def test_sql_command(default_args):
    msg = process_extra_command(default_args, 'SELECT * FROM mymeas')
    assert msg == ''
