#!/usr/bin/env python
"""
Autocompletion example.

Press [Tab] to complete the current word.
- The first Tab press fills in the common part of all completions
    and shows all the completions. (In the menu)
- Any following tab press cycles through all the possible completions.
"""
from __future__ import unicode_literals

from prompt_toolkit.contrib.completers import TreeCompleter
from prompt_toolkit import prompt


animal_completer = TreeCompleter({
    "abc": {"coucou": "print hello"},
    "def": {"list": "print hello",
            "help": "coucou"},
}
, ignore_case=True)


def main():
    text = prompt('Give some animals: ', completer=animal_completer,
                  complete_while_typing=True,
                  display_completions_in_columns=True)
    print('You said: %s' % text)


if __name__ == '__main__':
    main()
