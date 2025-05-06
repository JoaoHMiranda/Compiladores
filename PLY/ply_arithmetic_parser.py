import math
import ply.lex as lex
import ply.yacc as yacc

# ---- LEXER ----
reserved = {'sin': 'SIN', 'cos': 'COS', 'sqrt': 'SQRT', 'print': 'PRINT'}
tokens = [
    'INTEGER', 'FLOAT',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'ASSIGN', 'ID',
] + list(reserved.values())

t_PLUS    = r"\+"
t_MINUS   = r"-"
t_TIMES   = r"\*"
t_DIVIDE  = r"/"
t_POWER   = r"\^"
t_LPAREN  = r"\("
t_RPAREN  = r"\)"
t_ASSIGN  = r"="
t_ignore  = ' \t'

states = (('comment', 'exclusive'),)
t_comment_ignore = ''  # evita warning

def t_comment_start(t):
    r'/\*'
    t.lexer.comment_count = 1
    t.lexer.begin('comment')

def t_comment_end(t):
    r'\*/'
    t.lexer.comment_count -= 1
    if t.lexer.comment_count == 0:
        t.lexer.begin('INITIAL')

def t_comment_start_nested(t):
    r'/\*'
    t.lexer.comment_count += 1

def t_comment_content(t):
    r'[^*/]+'
    pass

def t_comment_any(t):
    r'[*/]'
    pass

def t_comment_error(t):
    t.lexer.skip(1)

def t_comment_single(t):
    r'//.*'
    pass

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal: '{t.value[0]}' na posição {t.lexer.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

# ---- PARSER ----
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),
)

variables = {}

def remove_comments(s: str) -> str:
    out, i, depth, n = '', 0, 0, len(s)
    while i < n:
        if depth == 0 and s[i:i+2] == '//':
            i += 2
            while i < n and s[i] != '\n':
                i += 1
        elif s[i:i+2] == '/*':
            depth += 1
            i += 2
        elif depth > 0 and s[i:i+2] == '*/':
            depth -= 1
            i += 2
        else:
            if depth == 0:
                out += s[i]
            i += 1
    return out

def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]

def p_statement_assign(p):
    'statement : ID ASSIGN expression'
    variables[p[1]] = p[3]
    p[0] = p[3]

def p_statement_print(p):
    'statement : PRINT expression'
    p[0] = p[2]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression'''
    if p[2] == '+':      p[0] = p[1] + p[3]
    elif p[2] == '-':    p[0] = p[1] - p[3]
    elif p[2] == '*':    p[0] = p[1] * p[3]
    elif p[2] == '/':    p[0] = p[1] / p[3]
    elif p[2] == '^':    p[0] = p[1] ** p[3]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    '''expression : INTEGER
                  | FLOAT'''
    p[0] = p[1]

def p_expression_variable(p):
    'expression : ID'
    try:
        p[0] = variables[p[1]]
    except KeyError:
        print(f"Variável não definida: '{p[1]}'")
        p[0] = 0

def p_expression_func(p):
    '''expression : SIN LPAREN expression RPAREN
                  | COS LPAREN expression RPAREN
                  | SQRT LPAREN expression RPAREN'''
    func, arg = p[1], p[3]
    if func == 'sin':    p[0] = math.sin(arg)
    elif func == 'cos':  p[0] = math.cos(arg)
    elif func == 'sqrt': p[0] = math.sqrt(arg)

parser = yacc.yacc()

# Flag para erro sintático único por entrada
parser.error_reported = False
_orig_parse = parser.parse

def _parse_with_reset(s, **k):
    parser.error_reported = False
    return _orig_parse(remove_comments(s), **k)

parser.parse = _parse_with_reset

def p_error(p):
    if not parser.error_reported:
        if not p:
            print("Erro sintático: entrada incompleta")
        else:
            print(f"Erro sintático no token '{p.value}'")
        parser.error_reported = True
    parser.errok()

# ---- REPL ----
if __name__ == '__main__':
    print("Calc > (digite 'exit' para sair)")
    while True:
        try:
            raw = input('> ')
        except EOFError:
            break
        if raw.strip().lower() == 'exit':
            break
        clean = remove_comments(raw)
        if not clean.strip():
            continue
        try:
            result = parser.parse(raw)
            if result is not None:
                print(result)
        except ZeroDivisionError:
            print("Erro: divisão por zero")
