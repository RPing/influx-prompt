import argparse

from prompt_toolkit import CommandLineInterface, Application, AbortAction
from prompt_toolkit.buffer import Buffer, AcceptAction
from prompt_toolkit.shortcuts import create_prompt_layout, create_eventloop
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.filters import Always
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.layout.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer

from . import __version__
from .completer import InfluxCompleter
from .influx_client import Client

class InfluxCli(object):
    def __init__(self, args):
        self.args = args
        self.completer = InfluxCompleter()
        self.history = InMemoryHistory()
        self.eventloop = create_eventloop()
        self.influx_client = Client(self.args)

    def run_cli(self):
        self.cli = self._build_cli()
        try:
            while True:
                document = self.cli.run()
                query = document.text

                result = self.influx_client.query(
                    query,
                    self.args['epoch'],
                    self.args['database'],
                )
                print(result)
                # print(result['error'])
                # if result['error']:
                #     print(result['error'])
        except EOFError:
            print('Goodbye!')

    def _build_cli(self):
        layout = create_prompt_layout(
            message='> ',
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
    parser.add_argument("-pw", "--password", help="password of the user (Default='root')", default='root')
    parser.add_argument("-d", "--database", help="database name to connect to (Default=None)")
    parser.add_argument("--ssl", help="use https instead of http to connect to InfluxDB (Default=False)", action='store_true')
    parser.add_argument("--ssl-cert", help="verify SSL certificates for HTTPS requests (Default=False)", action='store_true')
    parser.add_argument("--timeout", help="number of seconds Requests will wait for your client to establish a connection (Default=None)")
    parser.add_argument("--retry", help="number of retries your client will try before aborting (Default=3)", default=3)
    parser.add_argument("--epoch", help="response timestamps to be in epoch format, format can be h/m/s/ms/u/ns . " \
        "It will use RFC3339 UTC format if no format provided.")
    args = parser.parse_args()
    influx_cli = InfluxCli(vars(args))
    influx_cli.run_cli()

if __name__ == "__main__":
    cli()
