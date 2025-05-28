#!/usr/bin/env python3
"""
minilang.py — Minilang (Final)

"""

import sys
import re
import ast
import operator

sys.setrecursionlimit(2000)

# ——————— LEXER —————————————————————————————————————————————
class Token:
    __slots__ = ('type', 'val', 'line', 'col')
    def __init__(self, typ, val, line, col):
        self.type, self.val, self.line, self.col = typ, val, line, col
    def __repr__(self):
        return f"{self.type}({self.val!r})@{self.line}:{self.col}"

class Lexer:
    token_spec = [
        ('OP',       r'\*\*=|\+=|-=|\*=|/=|%=|==|!=|<=|>=|\*\*|&&|\|\||[+\-*/%<>=!()\[\]{},:]'),
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('STRING',   r'"([^"\\]|\\.)*"'),
        ('BOOLEAN',  r'\b(true|false)\b'),
        ('ID',       r'[A-Za-z_]\w*'),
        ('NEWLINE',  r'\n'),
        ('SKIP',     r'[ \t]+'),
        ('COMMENT',  r'#.*'),
        ('MISMATCH', r'.'),
    ]
    tok_re = re.compile('|'.join(f'(?P<{n}>{p})' for n, p in token_spec))

    def __init__(self, code):
        self.code = code

    def tokenize(self):
        line, col = 1, 1
        for mo in self.tok_re.finditer(self.code):
            kind, txt = mo.lastgroup, mo.group()
            if kind == 'NEWLINE':
                line += 1
                col = 1
                continue
            if kind in ('SKIP', 'COMMENT'):
                col += len(txt)
                continue
            if kind == 'MISMATCH':
                raise SyntaxError(f"Token inesperado {txt!r} na linha {line}:{col}")
            
            val = txt
            if kind == 'NUMBER':
                val = float(txt) if '.' in txt else int(txt)
            elif kind == 'STRING':
                val = ast.literal_eval(txt)
            elif kind == 'BOOLEAN':
                val = (txt == 'true')

            tok = Token(kind, val, line, col)
            yield tok
            col += len(txt)
        yield Token('EOF', None, line, col)

# ——————— AST NODES ———————————————————————————————————————————
class Node:
    pass

class Array(Node):
    __slots__ = ('elements',)
    def __init__(self, elements):
        self.elements = elements

class Number(Node):
    __slots__ = ('v',)
    def __init__(self, v):
        self.v = v

class String(Node):
    __slots__ = ('v',)
    def __init__(self, v):
        self.v = v

class Boolean(Node):
    __slots__ = ('v',)
    def __init__(self, v):
        self.v = v

class Var(Node):
    __slots__ = ('name',)
    def __init__(self, name):
        self.name = name

class Object(Node):
    __slots__ = ('kv',)
    def __init__(self, kv):
        self.kv = kv

class BinOp(Node):
    __slots__ = ('l', 'op', 'r')
    def __init__(self, l, op, r):
        self.l, self.op, self.r = l, op, r

class UnaryOp(Node):
    __slots__ = ('op', 'e')
    def __init__(self, op, e):
        self.op, self.e = op, e

class Assign(Node):
    __slots__ = ('var', 'op', 'expr')
    def __init__(self, var, op, expr):
        self.var, self.op, self.expr = var, op, expr

class Block(Node):
    __slots__ = ('stmts',)
    def __init__(self, stmts):
        self.stmts = stmts

class If(Node):
    __slots__ = ('cond', 'then_block', 'else_block')
    def __init__(self, cond, then_block, else_block):
        self.cond, self.then_block, self.else_block = cond, then_block, else_block

class While(Node):
    __slots__ = ('cond', 'body')
    def __init__(self, cond, body):
        self.cond, self.body = cond, body

class FuncDef(Node):
    __slots__ = ('name', 'params', 'body')
    def __init__(self, name, params, body):
        self.name, self.params, self.body = name, params, body

class FuncCall(Node):
    __slots__ = ('name', 'args')
    def __init__(self, name, args):
        self.name, self.args = name, args

class Return(Node):
    __slots__ = ('expr',)
    def __init__(self, expr):
        self.expr = expr
# ——————— PARSER ——————————————————————————————————————————————
class Parser:
    def __init__(self, toks):
        self.tokens = iter(toks)
        self.cur = None
        self.next()

    def next(self):
        self.cur = next(self.tokens)

    def eat(self, tt, val=None):
        if self.cur.type != tt or (val is not None and self.cur.val != val):
            expected = f"{tt}{'='+val if val else ''}"
            raise SyntaxError(f"Esperado {expected}, mas encontrou {self.cur.type}({self.cur.val!r}) na linha {self.cur.line}:{self.cur.col}")
        v = self.cur.val
        self.next()
        return v

    def parse(self):
        stmts = []
        while self.cur.type != 'EOF':
            stmts.append(self.stmt())
        return Block(stmts)

    def stmt(self):
        if self.cur.type == 'ID':
            kw = self.cur.val
            if kw == 'func': return self.parse_func()
            if kw == 'if': return self.parse_if()
            if kw == 'while': return self.parse_while()
            if kw == 'return': return self.parse_return()
        
        node = self.expr()
        if isinstance(node, Var) and self.cur.type == 'OP' and self.cur.val in ('=', '+=', '-=', '*=', '/=', '%=', '**='):
            op = self.eat('OP')
            rhs = self.expr()
            return Assign(node, op, rhs)
        
        if isinstance(node, FuncCall):
            return node
        
        raise SyntaxError(f"Statement inválido na linha {self.cur.line}:{self.cur.col}. Expressões soltas não são permitidas.")

    def parse_block(self, *end_keywords):
        stmts = []
        while not (self.cur.type == 'ID' and self.cur.val in end_keywords) and self.cur.type != 'EOF':
            stmts.append(self.stmt())
        return Block(stmts)

    def parse_func(self):
        self.eat('ID', 'func'); name = self.eat('ID'); self.eat('OP', '(')
        params = []
        if self.cur.val != ')':
            while True:
                params.append(self.eat('ID'))
                if self.cur.val == ')': break
                self.eat('OP', ',')
        self.eat('OP', ')')
        body = self.parse_block('end')
        self.eat('ID', 'end'); self.eat('ID', 'func')
        return FuncDef(name, params, body)

    def parse_if(self):
        self.eat('ID', 'if'); cond = self.expr()
        then_block = self.parse_block('else', 'end')
        else_block = None
        if self.cur.val == 'else':
            self.next()
            else_block = self.parse_block('end')
        self.eat('ID', 'end'); self.eat('ID', 'if')
        return If(cond, then_block, else_block)

    def parse_while(self):
        self.eat('ID', 'while'); cond = self.expr()
        body = self.parse_block('end')
        self.eat('ID', 'end'); self.eat('ID', 'while')
        return While(cond, body)

    def parse_return(self):
        self.eat('ID', 'return')
        return Return(self.expr())
    
    def expr(self): return self.logical()
    def logical(self):
        node = self.rel();
        while (self.cur.type == 'OP' and self.cur.val in ('&&', '||')) or (self.cur.type == 'ID' and self.cur.val in ('and', 'or')):
            op = self.eat(self.cur.type); node = BinOp(node, op, self.rel())
        return node
    def rel(self):
        node = self.add();
        while self.cur.type == 'OP' and self.cur.val in ('==', '!=', '<', '>', '<=', '>='):
            op = self.eat('OP'); node = BinOp(node, op, self.add())
        return node
    def add(self):
        node = self.mul();
        while self.cur.type == 'OP' and self.cur.val in ('+', '-'):
            op = self.eat('OP'); node = BinOp(node, op, self.mul())
        return node
    def mul(self):
        node = self.pow();
        while self.cur.type == 'OP' and self.cur.val in ('*', '/', '%'):
            op = self.eat('OP'); node = BinOp(node, op, self.pow())
        return node
    def pow(self):
        node = self.unary();
        if self.cur.type == 'OP' and self.cur.val == '**':
            op = self.eat('OP'); return BinOp(node, op, self.pow())
        return node
    def unary(self):
        if (self.cur.type == 'OP' and self.cur.val in ('!', '-')) or (self.cur.type == 'ID' and self.cur.val == 'not'):
            op = self.eat(self.cur.type); return UnaryOp(op, self.unary())
        return self.primary()
        
    def primary(self):
        t, v = self.cur.type, self.cur.val
        if t == 'NUMBER': self.next(); return Number(v)
        if t == 'STRING': self.next(); return String(v)
        if t == 'BOOLEAN': self.next(); return Boolean(v)
        if t == 'OP' and v == '(': self.next(); n = self.expr(); self.eat('OP', ')'); return n
        
        if t == 'OP' and v == '[':
            self.next()
            elements = []
            if self.cur.val != ']':
                while True:
                    elements.append(self.expr())
                    if self.cur.val == ']':
                        break
                    self.eat('OP', ',')
            self.eat('OP', ']')
            return Array(elements)
        
        if t == 'OP' and v == '{':
            self.next(); kv = []
            if self.cur.val != '}':
                while True:
                    if self.cur.type in ('STRING', 'ID'):
                        key = self.eat(self.cur.type)
                    else:
                        raise SyntaxError(f"Esperada uma chave como STRING ou ID, mas encontrou {self.cur.type}")
                    self.eat('OP', ':'); valn = self.expr(); kv.append((key, valn))
                    if self.cur.val == '}': break
                    self.eat('OP', ',')
            self.eat('OP', '}'); return Object(kv)
            
        if t == 'ID':
            name = self.eat('ID')
            node = Var(name)

            if self.cur.type == 'OP' and self.cur.val == '(':
                self.next(); args = []
                if self.cur.val != ')':
                    while True:
                        args.append(self.expr())
                        if self.cur.val == ')': break
                        self.eat('OP', ',')
                self.eat('OP', ')'); return FuncCall(name, args)

            while self.cur.type == 'OP' and self.cur.val == '[':
                self.next(); idx_expr = self.expr(); self.eat('OP', ']')
                node = BinOp(node, '[]', idx_expr)
            
            return node

        raise SyntaxError(f"Expressão inválida na linha {self.cur.line}:{self.cur.col}")

# ——————— INTERPRETER ———————————————————————————————————————
class Environment(dict):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()
    def get(self, key):
        if key in self: return self[key]
        if self.parent: return self.parent.get(key)
        raise NameError(f"Variável '{key}' não definida.")
    def set(self, key, value): self[key] = value

class ReturnValue(Exception):
    def __init__(self, value): self.value = value

def try_convert(v):
    if isinstance(v, str):
        if v.isdigit(): return int(v)
        try: return float(v)
        except ValueError: pass
    return v

def eval_node(node, env, funcs):
    nt = type(node).__name__
    
    if nt in ('Number', 'String', 'Boolean'): return node.v
    if nt == 'Var': return env.get(node.name)
    if nt == 'Object': return {k: eval_node(v, env, funcs) for k, v in node.kv}
    if nt == 'Array': return [eval_node(elem, env, funcs) for elem in node.elements]

    if nt == 'BinOp':
        # Acesso a propriedade/índice
        if node.op == '[]':
            obj = eval_node(node.l, env, funcs)
            idx = eval_node(node.r, env, funcs)
            try:
                return obj[idx]
            except (KeyError, IndexError):
                raise RuntimeError(f"Erro de acesso: chave ou índice '{idx}' não encontrado.")
        
        # Operadores lógicos com curto-circuito
        if node.op in ('&&', 'and'): return eval_node(node.l, env, funcs) and eval_node(node.r, env, funcs)
        if node.op in ('||', 'or'): return eval_node(node.l, env, funcs) or eval_node(node.r, env, funcs)
        
        # Outros operadores binários
        l, r = eval_node(node.l, env, funcs), eval_node(node.r, env, funcs)
        if node.op == '+' and (isinstance(l, str) or isinstance(r, str)): return str(l) + str(r)
        ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '%': operator.mod, '**': operator.pow, '==': operator.eq, '!=': operator.ne, '<': operator.lt, '>': operator.gt, '<=': operator.le, '>=': operator.ge}
        if node.op == '/':
            if r == 0: raise ZeroDivisionError("Divisão por zero.")
            return operator.truediv(l, r) if isinstance(l, float) or isinstance(r, float) else operator.floordiv(l, r)
        if node.op in ops: return ops[node.op](l, r)
        raise RuntimeError(f"Operador binário desconhecido: '{node.op}'")

    if nt == 'UnaryOp':
        v = eval_node(node.e, env, funcs)
        if node.op in ('!', 'not'): return not v
        if node.op == '-': return -v
        raise RuntimeError(f"Operador unário desconhecido: '{node.op}'")

    if nt == 'Assign':
        # Atribuição a propriedade de objeto (ex: person["age"] = 31)
        if isinstance(node.var, BinOp) and node.var.op == '[]':
            obj = eval_node(node.var.l, env, funcs)
            idx = eval_node(node.var.r, env, funcs)
            val = eval_node(node.expr, env, funcs)
            obj[idx] = val
            return None

        # Atribuição a variável normal
        name = node.var.name
        val = eval_node(node.expr, env, funcs)
        if node.op != '=':
            base = env.get(name)
            op_map = {'+=': '+', '-=': '-', '*=': '*', '/=': '/', '%=': '%', '**=': '**'}
            val = eval_node(BinOp(Var(name), op_map[node.op], node.expr), env, funcs)
        env.set(name, val)
        return None

    if nt == 'Block':
        for s in node.stmts:
            eval_node(s, env, funcs)
        return None

    if nt == 'If':
        if eval_node(node.cond, env, funcs): eval_node(node.then_block, env, funcs)
        elif node.else_block: eval_node(node.else_block, env, funcs)
        return None

    if nt == 'While':
        while eval_node(node.cond, env, funcs): eval_node(node.body, env, funcs)
        return None

    if nt == 'FuncDef':
        funcs[node.name] = (node.params, node.body)
        return None

    if nt == 'FuncCall':
        name = node.name
        if name == 'input':
            if node.args: raise TypeError("A função 'input' não aceita argumentos.")
            return try_convert(input())
        if name == 'print':
            vals = [eval_node(a, env, funcs) for a in node.args]
            print(*vals)
            return None
        if name not in funcs:
            raise NameError(f"Função '{name}' não definida.")
        params, body = funcs[name]
        if len(params) != len(node.args):
            raise TypeError(f"Função '{name}' espera {len(params)} argumentos, mas recebeu {len(node.args)}.")
        call_env = Environment(parent=env)
        for p, a in zip(params, node.args):
            call_env.set(p, eval_node(a, env, funcs))
        try:
            eval_node(body, call_env, funcs)
        except ReturnValue as ret:
            return ret.value
        return None

    if nt == 'Return':
        raise ReturnValue(eval_node(node.expr, env, funcs))

    raise RuntimeError(f"Nó AST desconhecido: {nt}")

# ——————— REPL & MAIN —————————————————————————————————————————
def run(code):
    try:
        toks = list(Lexer(code).tokenize())
        tree = Parser(toks).parse()
        global_env = Environment()
        functions = {}
        eval_node(tree, global_env, functions)
    except (SyntaxError, NameError, TypeError, ZeroDivisionError, RuntimeError) as e:
        print(f"Erro: {e}", file=sys.stderr)
    except ReturnValue:
        print("Erro: 'return' encontrado fora de uma função.", file=sys.stderr)

def main():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                code = f.read()
            run(code)
        except FileNotFoundError:
            print(f"Erro: Arquivo '{sys.argv[1]}' não encontrado.", file=sys.stderr)
    else:
        print("Uso: python3 minilang.py <arquivo.ml>")

if __name__ == '__main__':
    main()