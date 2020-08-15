from pygments.token import Token

from influx_prompt.tabular import json_to_tabular_result


def test_error_in_json():
    j = {
        'results': [{
            'statement_id': 0,
            'error': 'database name required'
        }]
    }
    result = json_to_tabular_result(j)
    assert result == [
        (Token.Red, '[ERROR] '),
        (Token, 'database name required'),
        (Token, '\n'),
        (Token, '\n')
    ]


def test_ordinary_json():
    j = {
        'results': [{
            'statement_id': 0,
            'series': [{
                'name': 'mymeas',
                'columns': ['time', 'myfield', 'mytag'],
                'values': [['2018-04-22T11:33:25.512241551Z', 91, '1']]
            }]
        }]
    }
    result = json_to_tabular_result(j)
    assert result == [
        (Token, 'name: '),
        (Token.Green, 'mymeas'),
        (Token, '\n'),
        (Token.Orange, 'time                            '),
        (Token.Orange, 'myfield  '),
        (Token.Orange, 'mytag  '),
        (Token, '\n'),
        (Token.Orange, '---                             '),
        (Token.Orange, '---      '),
        (Token.Orange, '---    '),
        (Token, '\n'),
        (Token, '2018-04-22T11:33:25.512241551Z  '),
        (Token, '91       '),
        (Token, '1      '),
        (Token, '\n'),
        (Token, '\n'),
        (Token, '\n')
    ]


def test_empty_value_in_json():
    j = {
        'results': [{
            'statement_id': 0,
            'series': [{
                'name': 'mymeas',
                'columns': ['time', 'myfield', 'mytag'],
                'values': [
                    ['2018-04-22T11:33:25.512241551Z', 91, '1'],
                    ['2018-05-23T12:08:32.214580837Z', 91, None]
                ]
            }]
        }]
    }
    result = json_to_tabular_result(j)
    assert result == [
        (Token, 'name: '),
        (Token.Green, 'mymeas'),
        (Token, '\n'),
        (Token.Orange, 'time                            '),
        (Token.Orange, 'myfield  '),
        (Token.Orange, 'mytag  '),
        (Token, '\n'),
        (Token.Orange, '---                             '),
        (Token.Orange, '---      '),
        (Token.Orange, '---    '),
        (Token, '\n'),
        (Token, '2018-04-22T11:33:25.512241551Z  '),
        (Token, '91       '),
        (Token, '1      '),
        (Token, '\n'),
        (Token, '2018-05-23T12:08:32.214580837Z  '),
        (Token, '91       '),
        (Token, '       '),
        (Token, '\n'),
        (Token, '\n'),
        (Token, '\n')
    ]
