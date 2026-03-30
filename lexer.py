import ply.lex as lex
from rich.console import Console
from rich.table import Table
console = Console()

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

t_POWER =r'\^'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_LE = r'<='
t_GE = r'>='

t_EQ = r'=='
t_EQUALS  = r'='

t_NE = r'!='
t_LT = r'<'
t_GT = r'>'


# Ignore spaces and tabs
t_ignore = ' \t'

# ------------------------
# COMPLEX RULES
# ------------------------

def t_INVALID_ID(t):
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*'
    console.print(f"[red]Invalid identifier[/red] '{t.value}' at line {t.lineno}")
    t.type = 'ERROR'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_STRING(t):
    r'"([^"\n\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_UNTERMINATED_STRING(t):
    r'"([^"\n\\]|\\.)*\n'

    console.print(f"[red]Unterminated string[/red] at line {t.lineno}")

    t.lexer.lineno += 1

    # 🔥 RETURN A SPECIAL TOKEN INSTEAD
    t.type = 'ERROR'
    return t

def t_NUMBER(t):
    r'\d+\.\d+|\d+'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Comments (ignore)
def t_COMMENT(t):
    r'\#.*'
    pass

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = 'NEWLINE'
    return t


#------------------------------------------------------------------------------------------
# Error handling
def t_error(t):
    console.print(f"[red]Illegal character:[/red] '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# ------------------------
# BUILD LEXER
# ------------------------
lexer = lex.lex()

# ------------------------
# VISUALIZER FUNCTION
# ------------------------
def visualize_tokens(code):
    lexer.input(code)

    table = Table(title="Token Stream")

    table.add_column("Type", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Line", style="yellow")
    table.add_column("Position", style="magenta")

    while True:
        tok = lexer.token()
        if not tok:
            break

        table.add_row(
            tok.type,
            str(tok.value),
            str(tok.lineno),
            str(tok.lexpos)
        )

    console.print(table)

#_____________________________________

def get_tokens_list(code):
    lexer.input(code)
    tokens_list = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)

    return tokens_list

# ------------------------
# MAIN TEST
# ------------------------

def get_lexer():
    return lex.lex()

if __name__ == "__main__":
    code = '''
    int x = 10;
    float y = 20.5;
    show x + y;
    '''

    visualize_tokens(code)