# Compiler Practice

This is a compiler writen in python.

## Lexer

`lexer` is a Lexical analysis program.

Before generate ASTTree, codes must be separated in diffrent tokens.

`lexer` contains,

* define token regex/priority/type
* parse code in tokens


## Parser

`parser` is parse tokens and gennerate AST-Tree program.

With tokens of codes, generate a tree node by a token or some tokens,  then
calcuate value of every node to calcuate the answer.

`parser` contains,

* generate AST-Tree
* parse operator tokens
* parse scope tokens
* calcuate value of every AST-Tree


