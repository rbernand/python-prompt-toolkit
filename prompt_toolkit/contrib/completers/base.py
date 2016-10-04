from __future__ import unicode_literals

from six import string_types
from prompt_toolkit.completion import Completer, Completion

__all__ = (
    'WordCompleter',
)


class WordCompleter(Completer):
    """
    Simple autocompletion on a list of words.

    :param words: List of words.
    :param ignore_case: If True, case-insensitive completion.
    :param meta_dict: Optional dict mapping words to their meta-information.
    :param WORD: When True, use WORD characters.
    :param sentence: When True, don't complete by comparing the word before the
        cursor, but by comparing all the text before the cursor. In this case,
        the list of words is just a list of strings, where each string can
        contain spaces. (Can not be used together with the WORD option.)
    :param match_middle: When True, match not only the start, but also in the
                         middle of the word.
    """
    def __init__(self, words, ignore_case=False, meta_dict=None, WORD=False,
                 sentence=False, match_middle=False):
        assert not (WORD and sentence)

        self.words = list(words)
        self.ignore_case = ignore_case
        self.meta_dict = meta_dict or {}
        self.WORD = WORD
        self.sentence = sentence
        self.match_middle = match_middle
        assert all(isinstance(w, string_types) for w in self.words)

    def get_completions(self, document, complete_event):
        # Get word/text before cursor.
        if self.sentence:
            word_before_cursor = document.text_before_cursor
        else:
            word_before_cursor = document.get_word_before_cursor(WORD=self.WORD)

        if self.ignore_case:
            word_before_cursor = word_before_cursor.lower()

        def word_matches(word):
            """ True when the word before the cursor matches. """
            if self.ignore_case:
                word = word.lower()

            if self.match_middle:
                return word_before_cursor in word
            else:
                return word.startswith(word_before_cursor)

        for a in self.words:
            if word_matches(a):
                display_meta = self.meta_dict.get(a, '')
                yield Completion(a, -len(word_before_cursor), display_meta=display_meta)


class TreeCompleter(Completer):
    def __init__(self, nodes, ignore_case=False, meta_dict=None, WORD=False,
                 sentence=False, match_middle=False):
        self._nodes = nodes
        self._ignore_case = ignore_case
        self._meta_dict = meta_dict
        self._WORD = WORD

    def get_completions(self, document, complete_event):
        word_before_cursor = document.text_before_cursor

        if self._ignore_case:
            word_before_cursor = word_before_cursor.lower()

        words_before_cursor = word_before_cursor.split()
        if words_before_cursor:
            word_before_cursor = words_before_cursor[-1]
        else:
            word_before_cursor = ""

        def word_matches(word):
            if self._ignore_case:
                word = word.lower()
            return word.startswith(word_before_cursor)

        root = self._nodes
        for word in words_before_cursor:
            try:
                if not isinstance(root[word], str):
                    root = root[word]
                else:
                    root = None
                    break
            except:
                break
        else:
            word_before_cursor = ""
        if root:
            for a in root:
                if word_matches(a):
                    if isinstance(root[a], str):

                        display_meta = root[a]
                    else:
                        display_meta = ", ".join(root[a])
                    yield Completion(a, -len(word_before_cursor), display_meta=display_meta)

