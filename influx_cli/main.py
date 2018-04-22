import argparse
import getpass
import re

from prompt_toolkit import CommandLineInterface, Application, AbortAction
from prompt_toolkit.buffer import Buffer, AcceptAction
from prompt_toolkit.shortcuts import create_prompt_layout, create_eventloop, print_tokens
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.filters import Always
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.styles import style_from_dict
from pygments.token import Token
from pygments.lexers.sql import SqlLexer

from . import __version__
from .completer import InfluxCompleter
from .influx_client import Client

class InfluxCli(object):
    style = style_from_dict({
        Token.Red: '#ff0000',
        Token.Orange: '#ff8000',
        Token.Yellow: '#ffff00',
        Token.Green: '#44ff44',
        Token.Blue: '#0000ff',
        Token.Indigo: '#4b0082',
        Token.Violet: '#9400d3'
    })
    def __init__(self, args, password):
        self.args = args
        self.args['password'] = password
        self.completer = InfluxCompleter()
        self.history = InMemoryHistory()
        self.eventloop = create_eventloop()
        self.influx_client = Client(self.args)

    def run_cli(self):
        self.cli = self._build_cli()
        print('Version: {0}'.format(__version__))
        print_tokens([
            (Token.Red, 'W'),
            (Token.Orange, 'e'),
            (Token.Yellow, 'l'),
            (Token.Green, 'c'),
            (Token.Blue, 'o'),
            (Token.Indigo, 'm'),
            (Token.Violet, 'e'),
        ], style=self.style)
        print('!')
        print_tokens([
            (Token.Green, 'Any issue please post to '),
            (Token.Yellow, 'https://github.com/RPing/influx-cli/issues'),
            (Token, '\n'),
        ], style=self.style)
        if self.args['database'] is None:
            print_tokens([(Token.Yellow, '[Warning] ')], style=self.style)
            print('You havn\'t set database. use "use <database>" to specify database.')

        try:
            while True:
                document = self.cli.run()
                query = document.text

                is_processed = self.process_extra_command(query)
                if not is_processed:
                    result = self.influx_client.query(
                        query,
                        self.args['database'],
                        self.args['epoch'],
                    )
                    print(result)
        except EOFError:
            print('Goodbye!')

    def process_extra_command(self, q):
        use_pattern = re.compile(r"use\s(?P<database>\w+);?", re.IGNORECASE)
        m = use_pattern.match(q)
        if m:
            database = m.group('database')
            self.args['database'] = database
            print('database now set to {0}'.format(database))
            return True
        return False

    def _build_cli(self):
        layout = create_prompt_layout(
            message='{0}> '.format(self.args['username']),
            lexer=PygmentsLexer(SqlLexer),
        )

        # with self._completer_lock:
        buf = Buffer(
            completer=self.completer,
            history=self.history,
            complete_while_typing=Always(),
            accept_action=AcceptAction.RETURN_DOCUMENT
        )

        key_binding_manager = KeyBindingManager(
            enable_abort_and_exit_bindings=True,
        )

        application = Application(
            layout=layout,
            buffer=buf,
            key_bindings_registry=key_binding_manager.registry,
            on_exit=AbortAction.RAISE_EXCEPTION,
            on_abort=AbortAction.RETRY,
            ignore_case=True
        )

        cli = CommandLineInterface(application=application, eventloop=self.eventloop)

        return cli


def cli():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action="help", help="show this help message and exit")
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument("-h", "--host", help="hostname to connect to InfluxDB (Default='localhost')", default='localhost')
    parser.add_argument("-p", "--port", help="port to connect to InfluxDB (Default=8086)", default=8086)
    parser.add_argument("-u", "--username", help="user to connect (Default='root')", default='root')
    parser.add_argument("-pw", "--password", help="prompt password of the user (Default='root')", action='store_true')
    parser.add_argument("-d", "--database", help="database name to connect to (Default=None)")
    parser.add_argument("--ssl", help="use https instead of http to connect to InfluxDB (Default=False)", action='store_true')
    parser.add_argument("--ssl-cert", help="verify SSL certificates for HTTPS requests (Default=False)", action='store_true')
    parser.add_argument("--timeout", help="number of seconds Requests will wait for your client to establish a connection (Default=None)")
    parser.add_argument("--retry", help="number of retries your client will try before aborting (Default=3)", default=3)
    parser.add_argument("--epoch", help="response timestamps to be in epoch format, format can be h/m/s/ms/u/ns . " \
        "It will use RFC3339 UTC format if no format provided.")
    args = parser.parse_args()
    if args.password:
        password = getpass.getpass()
    else:
        password = 'root'

    influx_cli = InfluxCli(vars(args), password)
    influx_cli.run_cli()

if __name__ == "__main__":
    cli()
