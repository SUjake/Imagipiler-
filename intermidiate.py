class IRGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, node):
        if node is None:
            return None

# ----- BASIC VALUES ----------------------
        if node.type == "num":
            return str(node.value)

        if node.type == "str":
            return f'"{node.value}"'

        if node.type == "id":
            return node.value

# ----- ARITHMETIC ------------------------
        if node.type in ["+", "-", "*", "/", "<", ">", "<=", ">=", "==", "!="]:
            left = self.generate(node.children[0])
            right = self.generate(node.children[1])
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {node.type} {right}")
            return temp

# ----- ASSIGNMENT -------------------------

        # ----- IF STATEMENT -----
        if node.type == "if":
            cond = self.generate(node.children[0])
            else_label = self.new_label()
            end_label = self.new_label()

            self.code.append(f"if {cond} False goto {else_label}")
            for stmt in node.children[1].children:
                self.generate(stmt)

            self.code.append(f"goto {end_label}")
            self.code.append(f"{else_label}:")
            self.code.append(f"{end_label}:")



        # ----- IF-ELSE STATEMENT -----
        if node.type == "ifelse":
            cond = self.generate(node.children[0])
            else_label = self.new_label()
            end_label = self.new_label()

            self.code.append(f"if {cond} False goto {else_label}")

            # then block
            for stmt in node.children[1].children:
                self.generate(stmt)

            self.code.append(f"goto {end_label}")

            # else block
            self.code.append(f"{else_label}:")
            for stmt in node.children[2].children:
                self.generate(stmt)

            self.code.append(f"{end_label}:")


        if node.type == "=":
            var = node.children[0].value
            val = self.generate(node.children[1])
            self.code.append(f"{var} = {val}")
            return var

# ----- DECLARATION -------------------------
        if node.type == "decl":
            var = node.children[0].value
            val = self.generate(node.children[1])
            self.code.append(f"{var} = {val}")
            return var

# ----- I/O -------------------------------
        if node.type == "show":
            val = self.generate(node.children[0])
            self.code.append(f"print {val}")

        if node.type == "take":
            var = node.children[0].value
            self.code.append(f"{var} = input")

        # ----- WHILE LOOP -----
        if node.type == "while":
            start = self.new_label()
            end = self.new_label()

            self.code.append(f"{start}:")

            cond = self.generate(node.children[0])
            self.code.append(f"if {cond} False goto {end} else go to next Line")

            for stmt in node.children[1].children:
                self.generate(stmt)

            self.code.append(f"goto {start}")
            self.code.append(f"{end}:")
        # ----- FOR LOOP -----
        if node.type == "for":
            init, cond, update, block = node.children

            self.generate(init)

            start = self.new_label()
            end = self.new_label()

            self.code.append(f"{start}:")

            cond_val = self.generate(cond)
            self.code.append(f"ifFalse {cond_val} goto {end}")

            for stmt in block.children:
                self.generate(stmt)

            self.generate(update)

            self.code.append(f"goto {start}")
            self.code.append(f"{end}:")


        if node.type in ["block", "S"]:
            for child in node.children:
                self.generate(child)

        return None