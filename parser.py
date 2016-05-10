#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lexer import TOKENTYPE
from lexer import TOKEN_SCP_MATCH


class UnkownTokenName(Exception):
    def __init__(self, token_name):
        self.token_name

    def __str__(self):
        return 'UnkownTokenName <%s>' % self.token_name


class Opt(object):
    @staticmethod
    def add(self, children):
        return children[0].value + children[1].value

    @staticmethod
    def sub(self, children):
        return children[0].value - children[1].value

    @staticmethod
    def mux(self, children):
        return children[0].value * children[1].value

    @staticmethod
    def div(self, children):
        return children[0].value / children[1].value

    @staticmethod
    def _if(self, children):
        if children[0]:
            return children[1].value
        else:
            return children[2].value


def calcuate(node):
    if hasattr(Opt, node.token_name):
        f = getattr(Opt, node.token_name)
        return f(Opt, node.children)
    else:
        raise UnkownTokenName(node.token_name)


class ASTNode(object):
    def __init__(self, token):
        self.token = token
        self.children = list()
 
    @property
    def token_name(self):
        return self.token.name

    @property
    def priority(self):
        return self.token.priority

    @property
    def is_opt(self):
        return self.token.type == TOKENTYPE.OPT

    @property
    def is_scp(self):
        return self.token.type == TOKENTYPE.SCP

    def add_child(self, child):
        self.children.append(child)

    def pop_child(self):
        return self.children.pop()

    @property
    def value(self):
        if self.is_opt:
            return calcuate(self)
        else:
            return self.token.value

    def __str__(self):
        if not self.is_opt:
            return '(leaf [%s])' % self.token.value
        else:
            return '(%s %s, %s)' % (self.token_name, str(self.children[0]), 
                                    str(self.children[1]))
    __repr__ =  __str__


class ASTTree(object):
    def __init__(self):
        self.trees = list()

    def add(self, ast_tree):
        self.trees.append(ast_tree)


def parse(tokens, stop_name=None):
    last_opt = None
    for token in tokens:
        if stop_name and token.name == stop_name:
            return last_opt
        node = ASTNode(token)
        if node.is_opt:
            next_node = ASTNode(tokens.next())
            if next_node.is_scp:
                next_node = parse(tokens, 
                    stop_name=TOKEN_SCP_MATCH.get(next_node.token_name))
            if node.priority <= last_opt.priority:
                node.add_child(last_opt)
                node.add_child(next_node)
                last_opt = node
            else:
                node.add_child(last_opt.pop_child())
                node.add_child(next_node)
                last_opt.add_child(node)
        else:
            last_opt = node
        print last_opt
    return last_opt


if __name__ == '__main__':
    from lexer import lex
    with open('test.s') as f:
        characters = f.read()
        tokens = lex(characters) 
        root = parse(tokens)
        print root.value
