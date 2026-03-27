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