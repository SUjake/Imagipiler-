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

#--------------------------------------------
#:p:- FACTOR

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

def p_factor_string(p):
    'factor : STRING'
    p[0] = Node("str", value=p[1])

def p_factor_error(p):
    'factor : ERROR'
    print("Bad string detected")
    p[0] = Node("error")
#--------------------------------------------
#:p:- STATEMENT RULES
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

#--------------------------------------------
#:p:- Block rules
def p_block(p):
    'block : LBRACE opt_newlines stmt_list opt_newlines RBRACE'
    p[0] = Node("block", p[3])

def p_block_error(p):
    'block : LBRACE error'
    print("Recovering broken block")

    while True:
        tok = parser.token()
        if not tok:
            break
        if tok.type == 'RBRACE':
            break

    parser.errok()
    p[0] = Node("block", [])


#--------------------------------------------
parser = yacc.yacc(start='program')