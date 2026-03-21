import ply.lex as lex


#:p:- Ye daal diye hai tokens maine issi ke around work karna SARTHAK 

tokens = (
    'ID','NUMBER','STRING',

    'PLUS','MINUS','MULT','DIV','POWER',
    'EQUALS','ERROR',

    'LPAREN','RPAREN',
    'LBRACE','RBRACE',
    'SEMICOLON','NEWLINE',

    'LT','GT','LE','GE','EQ','NE',

    # keywords
    'SHOW','TAKE',
    'INT','FLOAT','STRING_TYPE',
    'WHILE','FOR','IF'
)

reserved = {
    'show': 'SHOW',
    'take': 'TAKE',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING_TYPE',
    'while': 'WHILE',
    'for': 'FOR',
    'if': 'IF'
}
