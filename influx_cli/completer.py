from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder

from .completion import KEYWORDS

class InfluxCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor(WORD=True)
        suggestions = fuzzyfinder(word, KEYWORDS)
        return [Completion(s, -len(word), display_meta='keyword') for s in suggestions]
