from mparser import parser, Node

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.reg_count = 0
        self.label_count = 0
        self.var_table = {}
        self.stack_offset = 0

    def get_temp_reg(self):
        reg = f'$t{self.reg_count}'
        self.reg_count = (self.reg_count + 1) % 4
        return reg

    def new_label(self):
        label = f'L{self.label_count}'
        self.label_count += 1
        return label

    def allocate_var(self, var):
        if var not in self.var_table:
            self.var_table[var] = self.stack_offset
            self.stack_offset += 4
            self.code.append(f'addi $sp, $sp, -4')

    def generate(self, node):
        # statements agrupados
        if node.type == 'statement_list':
            for stmt in node.children:
                self.generate(stmt)
            return

        # programa e main
        if node.type == 'program':
            self.code.append('.text')
            self.code.append('.globl main')
            for decl in node.children:
                if decl.type == 'func_def':
                    self.generate(decl)
            self.code.append('main:')
            self.var_table.clear(); self.stack_offset = 0
            for stmt in node.children:
                if stmt.type != 'func_def':
                    self.generate(stmt)
            self.code.append('li $v0, 10')
            self.code.append('syscall')
            return

        # definição de função
        if node.type == 'func_def':
            name = node.leaf
            params, stmts, ret_expr = node.children
            self.code.append(f'{name}:')
            self.code.append('addi $sp, $sp, -4')
            self.code.append('sw $ra, 0($sp)')
            body = CodeGenerator()
            for i, pname in enumerate(params.children):
                body.var_table[pname] = body.stack_offset
                body.stack_offset += 4
                body.code.append(f'sw $a{i}, {body.var_table[pname]}($sp)')
            body.generate(stmts)
            rreg = body.generate(ret_expr)
            body.code.append(f'move $v0, {rreg}')
            body.code.append('lw $ra, 0($sp)')
            body.code.append('addi $sp, $sp, 4')
            body.code.append('jr $ra')
            self.code.extend(body.code)
            return

        # chamada de função
        if node.type == 'call':
            regs = [self.generate(arg) for arg in node.children]
            for i, r in enumerate(regs[:4]):
                self.code.append(f'move $a{i}, {r}')
            self.code.append(f'jal {node.leaf}')
            tres = self.get_temp_reg()
            self.code.append(f'move {tres}, $v0')
            return tres

        # atribuição
        if node.type == 'assign':
            self.allocate_var(node.leaf)
            r = self.generate(node.children[0])
            off = self.var_table[node.leaf]
            self.code.append(f'sw {r}, {off}($sp)')
            return

        # número literal
        if node.type == 'number':
            r = self.get_temp_reg()
            self.code.append(f'li {r}, {node.leaf}')
            return r

        # variável
        if node.type == 'id':
            r = self.get_temp_reg()
            off = self.var_table.get(node.leaf, 0)
            self.code.append(f'lw {r}, {off}($sp)')
            return r

        # binário
        if node.type == 'binop':
            a = self.generate(node.children[0])
            b = self.generate(node.children[1])
            c = self.get_temp_reg()
            op = {'+':'add','-':'sub','*':'mul','/':'div'}[node.leaf]
            self.code.append(f'{op} {c}, {a}, {b}')
            return c

        # if / if-else
        if node.type in ('if','if_else'):
            a = self.generate(node.children[0])
            b = self.generate(node.children[1])
            cond = self.get_temp_reg()
            self.code.append(f'slt {cond}, {b}, {a}')
            if node.type == 'if':
                L = self.new_label()
                self.code.append(f'beq {cond}, $zero, {L}')
                self.generate(node.children[2])
                self.code.append(f'{L}:')
            else:
                Lelse = self.new_label(); Lend = self.new_label()
                self.code.append(f'beq {cond}, $zero, {Lelse}')
                self.generate(node.children[2])
                self.code.append(f'j {Lend}')
                self.code.append(f'{Lelse}:')
                self.generate(node.children[3])
                self.code.append(f'{Lend}:')
            return

        # while
        if node.type == 'while':
            L0 = self.new_label(); L1 = self.new_label()
            self.code.append(f'{L0}:')
            a = self.generate(node.children[0])
            b = self.generate(node.children[1])
            cond = self.get_temp_reg()
            self.code.append(f'slt {cond}, {b}, {a}')
            self.code.append(f'beq {cond}, $zero, {L1}')
            self.generate(node.children[2])
            self.code.append(f'j {L0}')
            self.code.append(f'{L1}:')
            return

    def get_code(self):
        return '\n'.join(self.code)

def compile_to_mips(src):
    ast = parser.parse(src)
    gen = CodeGenerator()
    gen.generate(ast)
    return gen.get_code()
