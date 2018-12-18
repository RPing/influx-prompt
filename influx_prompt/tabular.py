from __future__ import absolute_import, unicode_literals
import jsane
from pygments.token import Token

from .compat import string


def json_to_tabular_result(j):
    '''return an array for print_tokens'''
    jj = jsane.from_dict(j)
    results = jj.results.r(default=[])
    tabular_result = []

    for r in results:
        if 'error' in r:
            tabular_result.append((Token.Red, '[ERROR] '))
            tabular_result.append((Token, r['error']))
            tabular_result.append((Token, '\n'))
            continue

        rr = jsane.from_dict(r)
        series = rr.series[0].r(default=None)

        if series:
            series = rr.series[0]
            name = series.name.r(default=None)
            columns = series.columns.r(default=[])
            values = series.values.r(default=[])

            column_amount = len(columns)
            longest_value_len = [0] * column_amount
            _calculate_value_len(
                column_amount,
                columns,
                values,
                longest_value_len
            )

            if name is not None:
                tabular_result.append((Token, 'name: '))
                tabular_result.append((Token.Green, name))
                tabular_result.append((Token, '\n'))

            for index, column in enumerate(columns):
                tabular_result.append((
                    Token.Orange,
                    '{column: <{width}}'.format(
                        column=column,
                        width=longest_value_len[index]+2
                    )
                ))
            tabular_result.append((Token, '\n'))

            for index in range(column_amount):
                tabular_result.append((
                    Token.Orange,
                    '{divider: <{width}}'.format(
                        divider='---',
                        width=longest_value_len[index]+2
                    )
                ))
            tabular_result.append((Token, '\n'))

            for value in values:
                for index, value_ in enumerate(value):
                    tabular_result.append((
                        Token,
                        '{value: <{width}}'.format(
                            value=string(value_),
                            width=longest_value_len[index]+2
                        )
                    ))
                tabular_result.append((Token, '\n'))
    tabular_result.append((Token, '\n'))

    return tabular_result


def _calculate_value_len(column_amount, columns, values, longest_value_len):
    for index in range(column_amount):
        for value in values:
            if value[index] is None:  # value is null
                value[index] = ''

            value_len = len(string(value[index]))
            if longest_value_len[index] < value_len:
                longest_value_len[index] = value_len

        column_len = len(string(columns[index]))
        if longest_value_len[index] < column_len:
            longest_value_len[index] = column_len
