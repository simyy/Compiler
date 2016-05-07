#!/usr/bin/env python
# -*- coding: utf-8 -*-

class UnkownTokenName(Exception):
    def __init__(self, token_name):
        self.token_name

    def __str__(self):
        return 'UnkownTokenName <%s>' % self.token_name


class NodeChildrens(object):
    def __init__(self, tokens):
        self.tokens = tokens

    def update(self, tokens):
        self.tokens.update(tokens)

    def add(self):
        return self.tokens[0].value + self.tokens[1].value

    def sub(self):
        return self.tokens[0].value - self.tokens[1].value

    def mux(self):
        return self.tokens[0].value * self.tokens[1].value

    def div(self):
        return self.tokens[0].value / self.tokens[1].value

    def _if(self):
        if self.tokens[0]:
            return self.tokens[1].value
        else:
            return self.tokens[2].value


def calcuate(node):
    if hasattr(NodeChildrens, node.token_name):
        f = getattr(NodeChildrens, node.token_name)
        return f(node.children)
    else:
        raise UnkownTokenName(node.token_name)


class ASTNode(object):
    def __init__(self, token, children=[]):
        self.token = token
        self.children = children
 
    @property
    def token_name(self):
        return self.token.name

    def add_child(self, child):
        self.children.append(child)

    def update_children(self, children):
        self.children.extend(children)

    def get_children(self):
        return self.children

    @property
    def value(self):
        return calcuate(self)

    def __repr__(self):
        return '(%s (%s))' % (self.token.name, ','.join([str(x) for x in self.children]))


class ASTTree(object):
    def __init__(self):
        self.nodes = []

    def add(self, ast_node):
        self.nodes.append(ast_node)


def parse(tokens):
    root = None
    last_priority = 0
    last_children = []
    for token in tokens:
        if token.is_opt:
            root = ASTNode(token)
            token = tokens.next
            last_children.append(token)
            root.update_children(last_children)
        else:
            last_children.append(token)
    print root


if __name__ == '__main__':
    from lexer import lex
    with open('test.s') as f:
        characters = f.read()
        tokens = lex(characters) 
        parse(tokens)
