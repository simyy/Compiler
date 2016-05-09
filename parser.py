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

    @property
    def priority(self):
        return self.token.priority

    @property
    def is_opt(self):
        return self.token.is_opt

    def add_child(self, child):
        self.children.append(child)

    def update_children(self, children):
        self.children.extend(children)

    def pop_child(self):
        return self.children.pop()

    def is_leaf(self):
        return True if not self.token.is_opt else False

    @property
    def value(self):
        if self.is_leaf:
            return self.token.value
        return calcuate(self)

    def __str__(self):
        if self.is_leaf:
            return '[leaf (%s)]' % self.token.value
        else:
            return '[%s (%s), (%s)]' % (self.token_name, str(self.children[0]), 
                                    str(self.children[1]))


class ASTTree(object):
    def __init__(self):
        self.trees = []

    def add(self, ast_tree):
        self.trees.append(ast_tree)


def parse(tokens):
    root = None
    last_opt = None
    for token in tokens:
        node = ASTNode(token)
        if node.is_opt:
            next_node = ASTNode(tokens.next())
            if node.priority <= last_opt.priority:
                node.add_child(last_opt)
            else:
                node.add_child(last_opt.pop_child())
            node.add_child(next_node)
            last_opt = node
            root = node
        else:
            last_opt = node
            root = node
    return root


if __name__ == '__main__':
    from lexer import lex
    with open('test.s') as f:
        characters = f.read()
        tokens = lex(characters) 
        root = parse(tokens)
        print root.value
