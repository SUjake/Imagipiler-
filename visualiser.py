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
    </TABLE>>'''