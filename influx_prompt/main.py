import argparse
import getpass

from prompt_toolkit import prompt, print_formatted_text, PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.formatted_text import FormattedText
from pygments.lexers.sql import SqlLexer

from . import __version__
from .completer import InfluxCompleter
from .influx_client import Client
from .extra_command import process_extra_command
from .tabular import json_to_tabular_result


class InfluxPrompt(object):
    def __init__(self, args, password):
        self.args = args
        self.args['password'] = password
        self.completer = InfluxCompleter()
        self.history = InMemoryHistory()
        self.influx_client = Client(self.args)

        self.influx_client.ping()

    def run_cli(self):
        print('Version: {0}'.format(__version__))
        print_formatted_text(FormattedText([
            ('ansibrightred', 'W'),
            ('orange', 'e'),
            ('ansibrightyellow', 'l'),
            ('ansibrightgreen', 'c'),
            ('blue', 'o'),
            ('indigo', 'm'),
            ('purple', 'e'),
            ('', '! ')
        ]), end='')
        print_formatted_text(FormattedText([
            ('', 'Open an issue here: '),
            ('ansibrightgreen', 'https://github.com/RPing/influx-prompt/issues'),
        ]))
        if self.args['database'] is None:
            print_formatted_text(FormattedText([
                ('ansibrightyellow', '[Warning] '),
            ]), end='')
            print('You haven\'t set database. '
                  'use "use <database>" to specify database.')

        session = PromptSession(
            lexer=PygmentsLexer(SqlLexer),
            search_ignore_case=True,
            history=self.history)

        prompt_text = '{0}> '.format(self.args['username'])
        while True:
            try:
                query = session.prompt(
                    prompt_text,
                    completer=self.completer,
                    complete_while_typing=True)
            except KeyboardInterrupt:
                continue
            except EOFError:
                print('Goodbye!')
                return

            query = query.strip()
            if query == '':
                continue

            msg = process_extra_command(self.args, query)
            if msg:
                print(msg)
                continue

            result = self.influx_client.query(
                query,
                self.args['database'],
                self.args['epoch'],
            )

            # top-level error.
            if 'error' in result:
                print_formatted_text(FormattedText([
                    ('ansibrightred', '[ERROR] '),
                ]), end='')
                print(result['error'])
                continue

            arr = json_to_tabular_result(result)
            print_formatted_text(FormattedText(arr))


def cli():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action="help",
                        help="show this help message and exit")
    parser.add_argument('-v', '--version',
                        action='version', version=__version__)
    parser.add_argument("-h", "--host", default='localhost',
                        help="hostname to connect to InfluxDB "
                        "(Default='localhost')")
    parser.add_argument("-p", "--port", default=8086,
                        help="port to connect to InfluxDB (Default=8086)")
    parser.add_argument("-u", "--username", default='root',
                        help="user to connect (Default='root')")
    parser.add_argument("-w", "--password", action='store_true',
                        help="prompt password of the user (Default='root')")
    parser.add_argument("-d", "--database",
                        help="database name to connect to (Default=None)")
    parser.add_argument("--ssl", action='store_true',
                        help="use https to connect to InfluxDB "
                        "(Default=False)")
    parser.add_argument("--ssl-cert", action='store_true',
                        help="verify SSL certificates for HTTPS requests "
                        "(Default=False)")
    parser.add_argument("--hide-invalid-ssl-warnings", action='store_true',
                        help="hide warnings for invalid SSL certificate for HTTPS requests "
                        "(Default=False)")
    parser.add_argument("--timeout",
                        help="number of seconds Requests will "
                        "wait for your client to establish a connection "
                        "(Default=None)")
    parser.add_argument("--retry", default=3,
                        help="number of retries your client will try"
                        " before aborting (Default=3)")
    parser.add_argument("--epoch",
                        help="response timestamps to be in epoch format, "
                        "format can be h/m/s/ms/u/ns . "
                        "It will use RFC3339 UTC format if no format provided")
    args = parser.parse_args()
    if args.password:
        password = getpass.getpass()
    else:
        password = 'root'

    influx_prompt = InfluxPrompt(vars(args), password)
    influx_prompt.run_cli()
