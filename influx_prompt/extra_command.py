from __future__ import absolute_import, unicode_literals
import re


def process_extra_command(args, query):
    use_pattern = re.compile(r"use\s(?P<database>\w+);?", re.IGNORECASE)
    m = use_pattern.match(query)
    if m:
        database = m.group('database')
        args['database'] = database
        return 'database now set to {0}'.format(database)

    if query == 'exit':
        raise EOFError

    return ''
