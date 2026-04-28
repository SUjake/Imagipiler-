import ply.yacc as yacc
from lexer import tokens, get_lexer, get_tokens_list
from visualiser import visualize_ast
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

SyntaxCount = 0

console = Console()

def pretty_error(message, line=None, hint=None):
    text = Text()

    text.append("⚠ SYNTAX ERROR\n", style="bold yellow")
    text.append(f"{message}\n", style="yellow")

    if line:
        text.append(f"Line: {line}\n", style="dim yellow")

    if hint:
        text.append(f"Hint: {hint}", style="italic yellow")

    console.print(Panel(text, border_style="yellow"))


class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children or []
        self.value = value


precedence = (
    ('left', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'POWER')
)

SYNC_TOKENS = {
    'ID', 'INT', 'FLOAT', 'STRING_TYPE',
    'SHOW', 'TAKE', 'WHILE', 'FOR', 'IF',
    'LBRACE'
}

start = 'program'


def p_opt_newlines_empty(p):
    'opt_newlines :'
    pass

def p_opt_newlines_more(p):
    'opt_newlines : opt_newlines NEWLINE'
    pass


def p_stmt_sep_single(p):
    'stmt_sep : NEWLINE'
    pass

def p_stmt_sep_more(p):
    'stmt_sep : stmt_sep NEWLINE'
    pass


def p_stmt_list_single(p):
    'stmt_list : full_statement'
    if p[1] is None or p[1].type == "error":
        p[0] = []
    else:
        p[0] = [p[1]]

def p_stmt_list_more(p):
    'stmt_list : stmt_list full_statement'
    if p[2] is None or p[2].type == "error":
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[2]]

def p_stmt_list_trailing_newline(p):
    'stmt_list : stmt_list stmt_sep'
    p[0] = p[1]


def p_type(p):
    '''type : INT
            | FLOAT
            | STRING_TYPE'''
    p[0] = p[1]


def p_program(p):
    'program : opt_newlines stmt_list opt_newlines'
    p[0] = Node("S", p[2])


def p_statement_assign(p):
    'statement : ID EQUALS expression'
    p[0] = Node("=", [
        Node("id", value=p[1]),
        p[3]
    ])


def p_arith_plus(p):
    'arith_expr : arith_expr PLUS term'
    p[0] = Node("+", [p[1], p[3]])

def p_arith_minus(p):
    'arith_expr : arith_expr MINUS term'
    p[0] = Node("-", [p[1], p[3]])

def p_arith_term(p):
    'arith_expr : term'
    p[0] = p[1]


def p_expression_compare(p):
    '''expression : arith_expr LT arith_expr
                  | arith_expr GT arith_expr
                  | arith_expr LE arith_expr
                  | arith_expr GE arith_expr
                  | arith_expr EQ arith_expr
                  | arith_expr NE arith_expr'''
    p[0] = Node(p[2], [p[1], p[3]])

def p_expression_arith(p):
    'expression : arith_expr'
    p[0] = p[1]


def p_term_mult(p):
    'term : term MULT factor'
    p[0] = Node("*", [p[1], p[3]])

def p_term_div(p):
    'term : term DIV factor'
    p[0] = Node("/", [p[1], p[3]])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_number(p):
    'factor : NUMBER'
    p[0] = Node("num", value=p[1])

def p_factor_id(p):
    'factor : ID'
    p[0] = Node("id", value=p[1])

def p_factor_power(p):
    'factor : factor POWER term'
    p[0] = Node("^", [p[1], p[3]])

def p_factor_group(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


def p_statement_show(p):
    'statement : SHOW LPAREN expression RPAREN'
    p[0] = Node("show", [p[3]])

def p_statement_take(p):
    'statement : TAKE LPAREN ID RPAREN'
    p[0] = Node("take", [Node("id", value=p[3])])


def p_statement_decl_int(p):
    'statement : INT ID EQUALS expression'
    p[0] = Node("decl", [Node("id", value=p[2]), p[4]], value="int")

def p_statement_decl_float(p):
    'statement : FLOAT ID EQUALS expression'
    p[0] = Node("decl", [Node("id", value=p[2]), p[4]], value="float")

def p_statement_decl_string(p):
    'statement : STRING_TYPE ID EQUALS expression'
    p[0] = Node("decl", [Node("id", value=p[2]), p[4]], value="string")


def p_block(p):
    'block : LBRACE opt_newlines stmt_list opt_newlines RBRACE'
    p[0] = Node("block", p[3])


def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN opt_newlines block'
    p[0] = Node("while", [p[3], p[6]])

def p_statement_for(p):
    'statement : FOR LPAREN ID EQUALS expression SEMICOLON expression SEMICOLON ID EQUALS expression RPAREN opt_newlines block'
    p[0] = Node("for", [
        Node("=", [Node("id", value=p[3]), p[5]]),
        p[7],
        Node("=", [Node("id", value=p[9]), p[11]]),
        p[14]
    ])

def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN opt_newlines block'
    p[0] = Node("if", [p[3], p[6]])


# -------- ERROR HANDLING --------

def p_statement_while_error(p):
    'statement : WHILE LPAREN error RPAREN opt_newlines block'
    global SyntaxCount
    pretty_error("Invalid while loop skipped", p.lineno(1), "Check the condition inside while")
    p[0] = Node("error")
    SyntaxCount += 1

def p_statement_for_error(p):
    'statement : FOR LPAREN error RPAREN opt_newlines block'
    global SyntaxCount
    pretty_error("Invalid for loop skipped", p.lineno(1), "Check the condition inside while")
    p[0] = Node("error")
    SyntaxCount += 1

def p_statement_while_error_incomplete(p):
    'statement : WHILE LPAREN error block'
    global SyntaxCount
    pretty_error("Invalid while loop skipped", p.lineno(1), "You are missing ')' ")
    p[0] = Node("error")
    SyntaxCount += 1

def p_statement_for_error_loose(p):
    'statement : FOR LPAREN error block'
    global SyntaxCount
    pretty_error("Invalid for loop skipped", p.lineno(1), "You are missing ')' ")
    p[0] = Node("error")
    SyntaxCount += 1

def p_line_recover(p):
    'line : error NEWLINE'
    global SyntaxCount
    pretty_error("Bad line ", p.lineno(1), "there is an error in line")
    SyntaxCount += 1
    p[0] = []


def p_statement_decl_missing_equals(p):
    'statement : type ID expression'
    pretty_error("Invalid declaration", p.lineno(2), "Missing '=' in the declaration")
    p[0] = Node("error")
    global SyntaxCount
    SyntaxCount += 1

def p_statement_assign_error(p):
    'statement : ID EQUALS error'
    pretty_error("Invalid declaration", p.lineno(1), "The value you are assigning is invalid")
    p[0] = Node("error")
    global SyntaxCount
    SyntaxCount += 1

def p_statement_decl_error(p):
    'statement : type ID EQUALS error'
    pretty_error("Invalid declaration", p.lineno(1), "The value you are assigning is invalid")
    p[0] = Node("error")
    global SyntaxCount
    SyntaxCount += 1

def p_statement_decl_missing_id(p):
    'statement : type EQUALS error'
    pretty_error("Invalid declaration", p.lineno(1), "Missing identifier in declairation")
    p[0] = Node("error")
    global SyntaxCount
    SyntaxCount += 1

def p_statement_decl_bad_id(p):
    'statement : type ERROR EQUALS error'
    pretty_error("Invalid declaration", p.lineno(1), "The identifier you are using is wrong ")
    p[0] = Node("error")
    global SyntaxCount
    SyntaxCount += 1

def p_statement_decl_broken(p):
    'statement : type error NEWLINE'
    pretty_error("Invalid declaration", p.lineno(1), "Expected variable name or assignment after type ")
    p[0] = Node("error")
    global SyntaxCount
    SyntaxCount += 1


def p_factor_error(p):
    'factor : ERROR'
    console.print("[bold red]Bad string detected[/bold red]")
    p[0] = Node("error")


def p_full_statement(p):
    'full_statement : statement stmt_sep'
    p[0] = p[1]


def p_error(p):
    if not p:
        console.print("[bold red][SYNTAX ERROR][/bold red] Unexpected EOF")
        return

    console.print(f"[bold red][SYNTAX ERROR][/bold red] Line {p.lineno}, Token '{p.value}'")
    global SyntaxCount
    SyntaxCount += 1


def p_factor_string(p):
    'factor : STRING'
    p[0] = Node("str", value=p[1])


parser = yacc.yacc(
    start='program',
    write_tables=False,
    debug=False,
    errorlog=yacc.NullLogger()
)


def print_tree(node, level=0):
    console.print("  " * level + f"{node.type} ({node.value})")
    for child in node.children:
        print_tree(child, level + 1)