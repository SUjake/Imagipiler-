from graphviz import Digraph
from html import escape 


def build_token_table(tokens):
    rows = ""
    for tok in tokens:
        
        rows += f"""
        <TR>
            <TD>{escape(str(tok.type))}</TD>
            <TD>{escape(str(tok.value))}</TD>
            <TD>{tok.lineno}</TD>
            <TD>{tok.lexpos}</TD>
        </TR>
        """
        
    return f'''<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD BGCOLOR="black"><FONT COLOR="white"><B>Type</B></FONT></TD>
            <TD BGCOLOR="black"><FONT COLOR="white"><B>Value</B></FONT></TD>
            <TD BGCOLOR="black"><FONT COLOR="white"><B>Line</B></FONT></TD>
            <TD BGCOLOR="black"><FONT COLOR="white"><B>Pos</B></FONT></TD>
        </TR>
        {rows}
    </TABLE>>'


def build_ir_table(ir_code):
    rows = ""
    for i, instr in enumerate(ir_code):
        rows += f"""
        <TR>
            <TD>{i}</TD>
            <TD>{escape(str(instr))}</TD>
        </TR>
        """

    return f'''<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD><B>#</B></TD>
            <TD><B>Algorithm representation</B></TD>
        </TR>
        {rows}
    </TABLE>>'''