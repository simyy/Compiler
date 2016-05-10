#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys


class TOKENTYPE(object):
    IGN = 0 # ignore
    OPT = 1 # oprate
    SCP = 1 # reserved
    INT = 2 # int
    STR = 3 # string


class TokenRegex(object):
    def __init__(self, regex, name,type=TOKENTYPE.OPT, priority=1):
        self.regex = regex
        self.name = name
        self.type = type
        self.priority = priority
        self.value = None


class Token(object):
    def __init__(self, value, token_regex):
        self.value = int(value) if value.isdigit() else value
        self.name = token_regex.name
        self.type = token_regex.type
        self.priority = token_regex.priority

    def __repr__(self):
        return '<Token(\'%s\') %s %s>' % (self.name, self.value, self.priority)

    def is_end(self):
        return True if self.name == 'end' else False


_TokenRegexs = (
    TokenRegex(r'\=', 'eq'),
    TokenRegex(r'\+', 'add'),
    TokenRegex(r'\-', 'sub'),
    TokenRegex(r'\*', 'mux', priority=2),
    TokenRegex(r'\/', 'div', priority=2),
    TokenRegex(r'\(', '(', type=TOKENTYPE.SCP, priority=3),
    TokenRegex(r'\)', ')', type=TOKENTYPE.SCP, priority=3),
    TokenRegex(r'\{', '{', type=TOKENTYPE.SCP, priority=3),
    TokenRegex(r'\}', '}', type=TOKENTYPE.SCP, priority=3),
    TokenRegex(r'if', '_if'),
    TokenRegex(r'else', '_else'),
    TokenRegex(r';', 'end'),
    TokenRegex(r'[0-9]+', 'int',  type=TOKENTYPE.INT),
    TokenRegex(r'[a-zA-Z][a-zA-Z0-9_]*', 'str', type=TOKENTYPE.STR),
    TokenRegex(r'\n', 'enter', type=TOKENTYPE.IGN),
    TokenRegex(r' ', 'blank', type=TOKENTYPE.IGN),
)


TOKEN_SCP_MATCH = {
    '(':  ')',
    '{':  '}',
}


def lex(characters):
    pos = 0 
    length = len(characters)
    while pos < length:
        for token_regex in _TokenRegexs:
            regex = re.compile(token_regex.regex)
            r = regex.match(characters, pos)
            if r:
                if token_regex.type is not TOKENTYPE.IGN:
                    yield Token(r.group(0), token_regex)
                pos = r.end(0)
                break
        else:
            print 'char:', characters[pos]
            sys.stderr.write('Illgal character: %s\n' % characters[pos])
            sys.exit(1)


if __name__ == '__main__':
    with open('test.s') as f:
        characters = f.read()
        tokens = lex(characters) 
        for i in tokens:
            print i
