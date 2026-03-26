import ply.yacc as yacc

precedence = (
    ('left', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'POWER')
)

start = 'program'

def p_type(p):
    '''type : INT
            | FLOAT
            | STRING_TYPE'''
    p[0] = p[1]



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