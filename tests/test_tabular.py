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
        ('ansibrightred', '[ERROR] '),
        ('', 'database name required'),
        ('', '\n'),
    ]


def test_no_value_key():
    j = {
        'results': [{
            'statement_id': 0,
            'series': [
                {'name': '_internal', 'columns': ['name', 'query']},
                {'name': 'NOAA_water_database', 'columns': ['name', 'query']},
            ]
        }]
    }
    result = json_to_tabular_result(j)
    assert result == [
        ('', 'name: '),
        ('ansibrightgreen', '_internal'),
        ('', '\n'),
        ('orange', 'name  '),
        ('orange', 'query  '),
        ('', '\n'),
        ('orange', '---   '),
        ('orange', '---    '),
        ('', '\n'),
        ('', '\n'),
        ('', 'name: '),
        ('ansibrightgreen', 'NOAA_water_database'),
        ('', '\n'),
        ('orange', 'name  '),
        ('orange', 'query  '),
        ('', '\n'),
        ('orange', '---   '),
        ('orange', '---    '),
        ('', '\n'),
        ('', '\n'),
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
        ('', 'name: '),
        ('ansibrightgreen', 'mymeas'),
        ('', '\n'),
        ('orange', 'time                            '),
        ('orange', 'myfield  '),
        ('orange', 'mytag  '),
        ('', '\n'),
        ('orange', '---                             '),
        ('orange', '---      '),
        ('orange', '---    '),
        ('', '\n'),
        ('', '2018-04-22T11:33:25.512241551Z  '),
        ('', '91       '),
        ('', '1      '),
        ('', '\n'),
        ('', '\n'),
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
        ('', 'name: '),
        ('ansibrightgreen', 'mymeas'),
        ('', '\n'),
        ('orange', 'time                            '),
        ('orange', 'myfield  '),
        ('orange', 'mytag  '),
        ('', '\n'),
        ('orange', '---                             '),
        ('orange', '---      '),
        ('orange', '---    '),
        ('', '\n'),
        ('', '2018-04-22T11:33:25.512241551Z  '),
        ('', '91       '),
        ('', '1      '),
        ('', '\n'),
        ('', '2018-05-23T12:08:32.214580837Z  '),
        ('', '91       '),
        ('', '       '),
        ('', '\n'),
        ('', '\n'),
    ]


def test_multiple_series_json():
    j = {
        'results': [{
            'statement_id': 0,
            'series': [{
                'name': 'mymeas',
                'columns': ['time', 'myfield', 'mytag'],
                'values': [['2018-04-22T11:33:25.512241551Z', 91, '1']]
            },{
                'name': 'mymeas',
                'columns': ['time', 'myfield', 'mytag'],
                'values': [['2018-04-22T11:33:25.512241551Z', 92, '1']]
            },{
                'name': 'mymeas',
                'columns': ['time', 'myfield', 'mytag'],
                'values': [['2018-04-22T11:33:25.512241551Z', 93, '1']]
            }]
        }]
    }
    result = json_to_tabular_result(j)
    assert result == [
        ('', 'name: '),
        ('ansibrightgreen', 'mymeas'),
        ('', '\n'),
        ('orange', 'time                            '),
        ('orange', 'myfield  '),
        ('orange', 'mytag  '),
        ('', '\n'),
        ('orange', '---                             '),
        ('orange', '---      '),
        ('orange', '---    '),
        ('', '\n'),
        ('', '2018-04-22T11:33:25.512241551Z  '),
        ('', '91       '),
        ('', '1      '),
        ('', '\n'),
        ('', '\n'),
        ('', 'name: '),
        ('ansibrightgreen', 'mymeas'),
        ('', '\n'),
        ('orange', 'time                            '),
        ('orange', 'myfield  '),
        ('orange', 'mytag  '),
        ('', '\n'),
        ('orange', '---                             '),
        ('orange', '---      '),
        ('orange', '---    '),
        ('', '\n'),
        ('', '2018-04-22T11:33:25.512241551Z  '),
        ('', '92       '),
        ('', '1      '),
        ('', '\n'),
        ('', '\n'),
        ('', 'name: '),
        ('ansibrightgreen', 'mymeas'),
        ('', '\n'),
        ('orange', 'time                            '),
        ('orange', 'myfield  '),
        ('orange', 'mytag  '),
        ('', '\n'),
        ('orange', '---                             '),
        ('orange', '---      '),
        ('orange', '---    '),
        ('', '\n'),
        ('', '2018-04-22T11:33:25.512241551Z  '),
        ('', '93       '),
        ('', '1      '),
        ('', '\n'),
        ('', '\n'),
    ]
