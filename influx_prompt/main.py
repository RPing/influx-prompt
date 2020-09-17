from __future__ import absolute_import, unicode_literals
import argparse
import getpass

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
# from prompt_toolkit.shortcuts import (
#     create_prompt_layout, print_tokens
# )
from prompt_toolkit.filters import Always
from prompt_toolkit.history import InMemoryHistory
# from prompt_toolkit.styles import style_from_dict
from pygments.token import Token
from pygments.lexers.sql import SqlLexer
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit

from . import __version__
from .completer import InfluxCompleter
from .influx_client import Client
from .extra_command import process_extra_command
from .tabular import json_to_tabular_result


class InfluxPrompt(object):
    # style = style_from_dict({
    #     Token.Red: '#ff0000',
    #     Token.Orange: '#ff8000',
    #     Token.Yellow: '#ffff00',
    #     Token.Green: '#44ff44',
    #     Token.Blue: '#0000ff',
    #     Token.Indigo: '#4b0082',
    #     Token.Violet: '#9400d3'
    # })

    def __init__(self, args, password):
        self.args = args
        self.args['password'] = password
        self.completer = InfluxCompleter()
        self.history = InMemoryHistory()
        self.influx_client = Client(self.args)

        self.influx_client.ping()
        self.cli = self._build_cli()

    def run_cli(self):
        # print('Version: {0}'.format(__version__))
        # print_tokens([
        #     (Token.Red, 'W'),
        #     (Token.Orange, 'e'),
        #     (Token.Yellow, 'l'),
        #     (Token.Green, 'c'),
        #     (Token.Blue, 'o'),
        #     (Token.Indigo, 'm'),
        #     (Token.Violet, 'e'),
        # ], style=self.style)
        # print('!')
        # print_tokens([
        #     (Token.Green, 'Any issue please post to '),
        #     (Token.Yellow, 'https://github.com/RPing/influx-prompt/issues'),
        #     (Token, '\n'),
        # ], style=self.style)
        # if self.args['database'] is None:
        #     print_tokens([(Token.Yellow, '[Warning] ')], style=self.style)
        #     print('You havn\'t set database. '
        #           'use "use <database>" to specify database.')

        try:
            while True:
                document = self.cli.run()
                query = document.text.strip()
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
                    print_tokens([
                        (Token.Red, '[ERROR] '),
                    ], style=self.style)
                    print(result['error'])
                    continue

                arr = json_to_tabular_result(result)
                print_tokens(arr, style=self.style)
        except EOFError:
            print('Goodbye!')

    def _build_cli(self):
        prompt = '{0}> '.format(self.args['username'])
        input_field = TextArea(
            height=1, prompt=prompt, multiline=False,
            wrap_lines=False)

        output_field = TextArea()

        container = HSplit([
            input_field,
            output_field,
        ])

        buf = Buffer(
            completer=self.completer,
            history=self.history,
            complete_while_typing=Always(),
        )

        kb = KeyBindings()

        @kb.add('c-d')
        def _(event):
            " Pressing Ctrl-d will exit the user interface. "
            event.app.exit()

        application = Application(
            layout=Layout(container, focused_element=input_field),
            key_bindings=kb,
            # buffer=buf,
            # ignore_case=True,
        )

        return application


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
