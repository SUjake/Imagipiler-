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
            return "parallelogram"

        elif node.type == "decl":
            return "component"

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