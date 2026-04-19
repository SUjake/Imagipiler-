class AssemblyGenerator:
    OP_MAP = {
        "+": "gen_add",
        "-": "gen_sub",
        "*": "gen_mul",
        "/": "gen_div",
        "<": "gen_compare",
        ">": "gen_compare",
        "==": "gen_compare",
        "!=": "gen_compare",
        "=": "gen_assign",
    }

    def __init__(self):
        self.code = []
        self.data = {}
        self.addr_counter = 0      # for variables
        self.pc = 0                # program counter (instructions)
        self.label_count = 0

    # ---------- UTIL ----------
    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def emit(self, line):
        addr = f"0x{self.pc:04X}"

        line = line.strip()

        # Handle comments or empty
        if not line or line.startswith(";"):
            self.code.append((addr, line, "", ""))
            self.pc += 2
            return

        parts = line.split(None, 1)  # split once: instr + rest

        instr = parts[0].upper()
        op1, op2 = "", ""

        if len(parts) > 1:
            operands = parts[1].split(",", 1)
            op1 = operands[0].strip()
            if len(operands) > 1:
                op2 = operands[1].strip()

        self.code.append((addr, instr, op1, op2))
        self.pc += 2

    def emit_label(self, label):
        addr = f"0x{self.pc:04X}"
        self.code.append((addr, f"{label}:", "", ""))
#-----------------------------------------------------------------
#>>> Declairation variable 
#TODO "Suryansh bhai ye ds ko change mat karna "
    def declare_var(self, name, dtype="dd"):
        if name not in self.data:
            addr = f"0x{self.addr_counter:04X}"
            size_map = {
                "dd": 4,
                "df": 6,
                "ds": 12
            }
            self.data[name] = {
                "addr": addr,
                "type": dtype
            }
            self.addr_counter += size_map[dtype]
#-------------------------------------------------------
    def get_addr(self, name):
        return self.data[name]["addr"]

    # ---------- CORE ----------
    def generate(self, node):
        if node is None:
            return

        method_name = self.OP_MAP.get(node.type, f"gen_{node.type}")
        method = getattr(self, method_name, self.generic_gen)
        return method(node)

    def generic_gen(self, node):
        for child in node.children:
            if child:
                self.generate(child)

    # ---------- DECL ----------
    def gen_decl(self, node):
        name = node.children[0].value
        expr = node.children[1]

        type_map = {
            "int": "dd",
            "float": "df",
            "string": "ds"
        }

        dtype = type_map.get(node.value, "dd")  
#! default = int ( agar change karna hoga toh bata dena)
        
        self.declare_var(name, dtype)
        self.generate(expr)
        self.emit(f"MOV [{self.get_addr(name)}], eax")
        #print("DEBUG TYPE:", node.value, "→", dtype)

    # ---------- ASSIGN ----------
    def gen_assign(self, node):
        name = node.children[0].value
        expr = node.children[1]

        self.generate(expr)
        self.emit(f"MOV [{self.get_addr(name)}], eax")

    # ---------- ID ----------
    def gen_id(self, node):
        self.emit(f"MOV eax, [{self.get_addr(node.value)}]")

    # ---------- NUM ----------
    def gen_num(self, node):
        self.emit(f"MOV eax, {node.value}")

    # ---------- ARITH ----------
    def gen_add(self, node):
        self.generate(node.children[0])
        self.emit("PUSH eax")

        self.generate(node.children[1])
        self.emit("MOV ebx, eax")

        self.emit("POP eax")
        self.emit("ADD eax, ebx")

    def gen_sub(self, node):
        self.generate(node.children[0])
        self.emit("PUSH eax")

        self.generate(node.children[1])
        self.emit("MOV ebx, eax")

        self.emit("POP eax")
        self.emit("SUB eax, ebx")

    def gen_mul(self, node):
        self.generate(node.children[0])
        self.emit("PUSH eax")

        self.generate(node.children[1])
        self.emit("MOV ebx, eax")

        self.emit("POP eax")
        self.emit("IMUL eax, ebx")

    def gen_div(self, node):
        self.generate(node.children[0])
        self.emit("PUSH eax")

        self.generate(node.children[1])
        self.emit("MOV ebx, eax")

        self.emit("POP eax")
        self.emit("CDQ")
        self.emit("IDIV ebx")

    # ---------- COMPARE ----------
    def gen_compare(self, node):
        op = node.type

        self.generate(node.children[0])
        self.emit("PUSH eax")
        
        self.generate(node.children[1])
        self.emit("MOV ebx, eax")

        self.emit("POP eax")
        self.emit("CMP eax, ebx")

        true_label = self.new_label()
        end_label = self.new_label()

        if op == "==":
            self.emit(f"JE {true_label}")
        elif op == "!=":
            self.emit(f"JNE {true_label}")
        elif op == "<":
            self.emit(f"JL {true_label}")
        elif op == ">":
            self.emit(f"JG {true_label}")

        self.emit("MOV eax, 0")
        self.emit(f"JMP {end_label}")

        self.emit_label(true_label)
        self.emit("MOV eax, 1")

        self.emit_label(end_label)

    # ---------- IF ----------
    def gen_if(self, node):
        cond = node.children[0]
        block = node.children[1]

        end_label = self.new_label()

        self.generate(cond)
        self.emit("CMP eax, 0")
        self.emit(f"JE {end_label}")

        self.generate(block)

        self.emit_label(end_label)
    #-----------------------------

    def gen_str(self, node):
        self.emit(f'MOV eax, "{node.value}"')

    # ---------- WHILE ----------
    def gen_while(self, node):
        cond = node.children[0]
        block = node.children[1]

        start_label = self.new_label()
        end_label = self.new_label()

        self.emit_label(start_label)

        self.generate(cond)
        self.emit("CMP eax, 0")
        self.emit(f"JE {end_label}")

        self.generate(block)
        self.emit(f"JMP {start_label}")

        self.emit_label(end_label)

    # ---------- SHOW ----------
    def gen_show(self, node):
        self.generate(node.children[0])
        self.emit("print eax")

    # ---------- BLOCK ----------
    def gen_block(self, node):
        for stmt in node.children:
            self.generate(stmt)

    # ---------- OUTPUT ----------
    def get_output(self):
        data_section = ["section .data"]
        data_section = ["section .data"]

#** @Aditya ye 2 baar kyu likh rakha hai 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        for var, info in self.data.items():
            addr = info["addr"]
            dtype = info["type"]

            if dtype == "ds":
                init = '" "'        # fake empty string
            else:
                init = "0"          # for dd and df
            data_section.append(f"{addr} : {var} {dtype} {init}")


        text_section = ["section .text", "global _start", "_start:"]
        # convert tuple instructions → string
        formatted_code = []
        for addr, instr, op1, op2 in self.code:
            if instr.endswith(":"):  # label
                formatted_code.append(f"{addr} {instr}")
            else:
                line = f"{addr} {instr}"
                if op1:
                    line += f" {op1}"
                if op2:
                    line += f", {op2}"
                formatted_code.append(line)

        return "\n".join(data_section + [""] + text_section + formatted_code)
    
    def get_data(self):
        data_rows = []
        for var, info in self.data.items():
            data_rows.append((info["addr"], "DATA", var, f"{info['type']} 0"))
        return data_rows