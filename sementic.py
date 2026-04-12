class SymbolTable:
    def __init__(self):
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})


    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare(self, name, typ):
        if name in self.scopes[-1]:
            raise Exception(f"Redeclaration of '{name}'")
        self.scopes[-1][name] = typ

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    

class SemanticAnalyzer:
    OP_MAP = {
        "=": "visit_assign",
        "+": "visit_add",
        "-": "visit_sub",
        "*": "visit_mul",
        "/": "visit_div",
        "^": "visit_pow",
        "<": "visit_compare",
        ">": "visit_compare",
        "<=": "visit_compare",
        ">=": "visit_compare",
        "==": "visit_compare",
        "!=": "visit_compare",
    }

    def __init__(self):
        self.symtab = SymbolTable()
        self.errors = []

    def analyze(self, node):
        if node is None:
            return None

        method_name = self.OP_MAP.get(node.type, f"visit_{node.type}")
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        result = None
        for child in node.children:
            if child is not None:
                result = self.analyze(child)
        return result

    def is_compatible(self, declared_type, expr_type):
        if declared_type == expr_type:
            return True
        if declared_type == "float" and expr_type == "int":
            return True
        return False

    def visit_decl(self, node):
        name = node.children[0].value
        expr = node.children[1]
        declared_type = node.value

        expr_type = self.analyze(expr)
        if expr_type == "error":
            return "error"

        if not self.is_compatible(declared_type, expr_type):
            self.errors.append(f"Type mismatch in declaration of '{name}'")
            return "error"

        try:
            self.symtab.declare(name, declared_type)
        except Exception as e:
            self.errors.append(str(e))
            return "error"

        return declared_type

    def visit_assign(self, node):
        name = node.children[0].value
        rhs = node.children[1]

        var_type = self.symtab.lookup(name)
        if var_type is None:
            self.errors.append(f"Undeclared variable '{name}'")
            return "error"

        rhs_type = self.analyze(rhs)
        if rhs_type == "error":
            return "error"

        if not self.is_compatible(var_type, rhs_type):
            self.errors.append(f"Type mismatch in assignment to '{name}'")
            return "error"

        return var_type

    def visit_num(self, node):
        if isinstance(node.value, int):
            return "int"
        if isinstance(node.value, float):
            return "float"
        self.errors.append(f"Invalid numeric literal '{node.value}'")
        return "error"

    def visit_str(self, node):
        return "string"

    def visit_id(self, node):
        typ = self.symtab.lookup(node.value)
        if typ is None:
            self.errors.append(f"Undeclared identifier '{node.value}'")
            return "error"
        return typ

    def visit_add(self, node):
        return self.visit_numeric_binop(node)

    def visit_sub(self, node):
        return self.visit_numeric_binop(node)

    def visit_mul(self, node):
        return self.visit_numeric_binop(node)

    def visit_div(self, node):
        return self.visit_numeric_binop(node)

    def visit_pow(self, node):
        return self.visit_numeric_binop(node)

    def visit_numeric_binop(self, node):
        left = self.analyze(node.children[0])
        right = self.analyze(node.children[1])

        if left not in ("int", "float") or right not in ("int", "float"):
            self.errors.append("Arithmetic operators require numeric operands")
            return "error"

        if left == "float" or right == "float":
            return "float"
        return "int"

    def visit_compare(self, node):
        left = self.analyze(node.children[0])
        right = self.analyze(node.children[1])

        if left == "error" or right == "error":
            return "error"

        if left != right and not (left in ("int", "float") and right in ("int", "float")):
            self.errors.append("Incompatible types in comparison")
            return "error"

        return "bool"

    def visit_block(self, node):
        self.symtab.enter_scope()
        try:
            for stmt in node.children:
                self.analyze(stmt)
        finally:
            self.symtab.exit_scope()
        return None

    def visit_show(self, node):
        self.analyze(node.children[0])
        return None

    def visit_take(self, node):
        name = node.children[0].value
        if self.symtab.lookup(name) is None:
            self.errors.append(f"Undeclared variable '{name}' in take()")
            return "error"
        return None

    def visit_if(self, node):
        cond_type = self.analyze(node.children[0])
        if cond_type not in ("bool", "int", "float"):
            self.errors.append("IF condition must be valid")
        self.analyze(node.children[1])
        return None

    def visit_while(self, node):
        cond_type = self.analyze(node.children[0])
        if cond_type not in ("bool", "int", "float"):
            self.errors.append("WHILE condition must be valid")
        self.analyze(node.children[1])
        return None