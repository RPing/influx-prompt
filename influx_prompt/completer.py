from __future__ import absolute_import, unicode_literals
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder

from .completion import KEYWORDS, FUNCTIONS


class InfluxCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor(WORD=True)

        suggestions = fuzzyfinder(word, KEYWORDS + FUNCTIONS)
        for s in suggestions:
            if s in KEYWORDS:
                yield Completion(s, -len(word), display_meta='keyword')
            elif s in FUNCTIONS:
                yield Completion(s, -len(word), display_meta='function')
