import parser
import intermidiate
from sementic import SemanticAnalyzer
import lexer
from visualiser import visualize_ast
from asm import AssemblyGenerator
from asmFromat import format_assembly
from rich.console import Console


def run_compiler(code, console=None):
    # ---------------- CONSOLE SETUP ----------------
    if console is None:
        console = Console()

    # Inject SAME console everywhere (CRITICAL)
    parser.console = console
    lexer.console = console

    # ---------------- RESET FLAGS ----------------
    parser.SyntaxCount = 0
    asmFlag = 0
    lexer.lexError = False

    console.print("[bold cyan]Starting Compilation...[/bold cyan]\n")

    # ---------------- LEXICAL ----------------
    tokens_list = lexer.get_tokens_list(code)
    lex = lexer.get_lexer()

    # ---------------- PARSING ----------------
    result = parser.parser.parse(code, lexer=lex)

    # ---------------- IR GENERATION ----------------
    ir = intermidiate.IRGenerator()
    if result:
        ir.generate(result)

    # ---------------- AST VISUALIZATION ----------------
    ast_path = None

    if result is None:
        console.print("[bold red]Parsing failed. AST not generated.[/bold red]")
    else:
        ast_path = visualize_ast(result, tokens_list, ir.code)

    # ---------------- ERROR REPORT ----------------
    console.print(f"[yellow]Syntax Errors:[/yellow] {parser.SyntaxCount}")
    console.print(f"[yellow]Lexical Error:[/yellow] {lexer.lexError}")

    # ---------------- SEMANTIC ANALYSIS ----------------
    if parser.SyntaxCount == 0 and not lexer.lexError and result is not None:

        analyzer = SemanticAnalyzer()
        analyzer.analyze(result)

        if analyzer.errors:
            console.print("\n[bold red]--- SEMANTIC ERRORS ---[/bold red]")
            for err in analyzer.errors:
                console.print(f"[red]{err}[/red]")
        else:
            console.print("\n[bold green]No semantic errors. You're clean.[/bold green]\n")
            asmFlag = 1
    else:
        console.print("\n[bold yellow]Due to lexical/syntax errors semantic analysis is skipped[/bold yellow]\n")

    # ---------------- ASSEMBLY GENERATION ----------------
    if asmFlag:
        generator = AssemblyGenerator()
        generator.generate(result)
        format_assembly(generator.code, generator.get_data(), console)
    else:
        console.print("[bold red]Due to Errors , Assembly formation is skipped[/bold red]")

    console.print("\n[bold cyan]Compilation Finished[/bold cyan]")

    # 🔥 return AST path for frontend
    return ast_path