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