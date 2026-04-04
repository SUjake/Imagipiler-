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


def visualize_ast(root,tokens,ir_code):
    dot = Digraph()
    
    counter = 0
    dot.attr(rankdir="TB")
    #dot.attr(nodesep="1.0", ranksep="1.5")  

    def get_shape(node):
        if node.type == "=":
            return "diamond"

        elif node.type in ["id", "num", "str"]:
            return "box"

        elif node.type in ["+", "-", "*", "/", "^"]:
            return "circle"

        elif node.type in ["<", ">", "<=", ">=", "==", "!="]:
            return "hexagon"

        elif node.type in ["show", "take"]:
            return "parallelogram"   # I/O operations

        elif node.type == "decl":
            return "component"       # declaration

        elif node.type == "while":
            return "octagon"

        elif node.type == "for":
            return "doublecircle"

        elif node.type == "block":
            return "folder"

        elif node.type == "S":
            return "folder"

        return "ellipse"

    dot.attr('node', fontname="Arial")

    def get_color(node):
        if node.type == "num":
            return "lightgreen"

        elif node.type == "str":
            return "pink"

        elif node.type == "id":
            return "lightblue"

        elif node.type in ["+", "-"]:
            return "yellow"

        elif node.type in ["*", "/"]:
            return "orange"

        elif node.type == "^":
            return "red"

        elif node.type in ["<", ">", "<=", ">=", "==", "!="]:
            return "purple"

        elif node.type == "=":
            return "lightgrey"

        elif node.type == "decl":
            return "cyan"

        elif node.type in ["show", "take"]:
            return "gold"

        elif node.type == "while":
            return "lightcoral"

        elif node.type == "for":
            return "lightseagreen"

        elif node.type == "block":
            return "white"

        elif node.type == "S":
            return "white"

        return "white"