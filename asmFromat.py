from rich.table import Table
from rich.console import Console
from rich import box
from rich.text import Text

REGISTERS = {"eax", "ebx", "ecx", "edx"}
JUMPS = {"JMP", "JE", "JNE", "JG", "JL"}
STACK = {"PUSH","POP"}


def style_operand(op):
    if not op:
        return f"[#D8D7D9]----[/#D8D7D9]"

    op_clean = op.replace("[", "").replace("]", "")

    if op_clean in REGISTERS:
        return f"[#F3F752]{op}[/#F3F752]"

    return op


def format_assembly(code, data=None, console=None):
    # 🔥 fallback for CLI usage
    if console is None:
        console = Console()

    # ---------------- DATA SECTION ----------------
    if data:
        data_table = Table(
            title="Data Section",
            box=box.HEAVY,
            show_lines=True
        )

        data_table.add_column("Address", style="red")
        data_table.add_column("Type")
        data_table.add_column("Variable")
        data_table.add_column("Value")

        for addr, typ, var, val in data:
            data_table.add_row(
                f"[red]{addr}[/red]",
                f"[#9666DE]{typ}[/#9666DE]",
                f"[#86DE66]{var}[/#86DE66]",
                f"{val}"
            )

        console.print(data_table)

    # ---------------- CODE SECTION ----------------
    table = Table(
        title="Custom Assembly Output",
        box=box.HEAVY,
        show_lines=True
    )

    table.add_column("Address", style="red")
    table.add_column("Instruction")
    table.add_column("Reg1")
    table.add_column("Reg2")

    for addr, instr, op1, op2 in code:
        if instr.endswith(":"):
            label_text = Text(instr, style="bold white")
            table.add_row(
                f"[white]{addr}[/white]",
                "",
                label_text,
                "",
                style="bold"
            )
            continue

        instr_upper = instr.upper()

        # --- PRINT styling ---
        if instr_upper == "PRINT" or instr_upper == "; PRINT":
            instr_text = "[underline][#F527F2]PRINT[/#F527F2][/underline]"
            op1 = f"[underline][#F3F752]{op1}[/#F3F752][/underline]" if op1 else f"[#D8D7D9]----[/#D8D7D9]"
            op2 = f"[underline][#F3F752]{op2}[/#F3F752][/underline]" if op2 else f"[#D8D7D9]----[/#D8D7D9]"

        elif instr_upper in JUMPS:
            instr_text = f"[#2110B2]{instr_upper}[/#2110B2]"

        elif instr_upper in STACK:
            instr_text = f"[#38FFF5]{instr_upper}[/#38FFF5]"

        else:
            instr_text = instr_upper

        op1 = style_operand(op1)
        op2 = style_operand(op2)

        table.add_row(
            f"[red]{addr}[/red]",
            instr_text,
            op1,
            op2
        )

    console.print(table)