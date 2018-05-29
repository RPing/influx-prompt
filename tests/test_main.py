import mock

from influx_prompt.main import cli


class MockCLI(object):
    def __init__(self, application=None, eventloop=None):
        pass

    def run(self):
        raise EOFError


@mock.patch('influx_prompt.main.print_tokens', side_effect=None)
@mock.patch('influx_prompt.main.CommandLineInterface', side_effect=MockCLI)
def test_main(mock_cli, mock_print_tokens):
    cli()
    mock_cli.assert_called()
    mock_print_tokens.assert_called()
