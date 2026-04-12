import parser
import algorithm
from sementic import SemanticAnalyzer
from lexer import get_lexer, get_tokens_list
from visualiser import visualize_ast


code = """
int  = 5
string s  = "Suryansh saini is so cool"
#hiii 
string e = "this is error"

while(x>0)
{
    show(ans)
    show(ans2)
    x = x-1
}
"""

# reset error count (important)
parser.SyntaxCount = 0

tokens_list = get_tokens_list(code)
lexer = get_lexer()

# parse
result = parser.parser.parse(code, lexer=lexer)

# IR
ir = algorithm.IRGenerator()
if result:
    ir.generate(result)

# AST visualize
if result is None:
    print("Parsing failed. AST not generated.")
else:
    visualize_ast(result, tokens_list, ir.code)

# syntax errors
print("Syntax Errors:", parser.SyntaxCount)

# semantic phase
if parser.SyntaxCount == 0:
    analyzer = SemanticAnalyzer()
    analyzer.analyze(result)

    if analyzer.errors:
        print("\n--- SEMANTIC ERRORS ---")
        for err in analyzer.errors:
            print(err)
    else:
        print("\nNo semantic errors. You're clean.")
else:
    print("\nDue to syntax errors semantic analysis is skipped\n")