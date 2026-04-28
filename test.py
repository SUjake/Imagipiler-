from lexer import get_lexer
from parser import parser
from sementic import SemanticAnalyzer

code = """
int x = 5
float y = 2.5
string z = 4
x = x + 1
show(x)
"""

lexer = get_lexer()
ast = parser.parse(code, lexer=lexer)

sem = SemanticAnalyzer()
sem.analyze(ast)

if sem.errors:
    print("Semantic errors:")
    for err in sem.errors:
        print(" -", err)
else:
    print("Semantic analysis passed.")