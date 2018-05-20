import pytest
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document

@pytest.fixture
def complete_event():
    from unittest.mock import Mock
    return Mock()

@pytest.fixture
def completer():
    from influx_cli.completer import InfluxCompleter
    return InfluxCompleter()

def test_keyword_completion(completer, complete_event):
    text = 'SEL'
    position = len(text)
    result = set(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))
    assert result == set([Completion(text='SELECT', start_position=-3, display_meta='keyword')])

def test_function_completion(completer, complete_event):
    text = 'COUN'
    position = len(text)
    result = set(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))
    assert result == set([Completion(text='COUNT()', start_position=-4, display_meta='function')])
