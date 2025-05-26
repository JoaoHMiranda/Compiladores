import ply.lex as lex

tokens = (
    'NUMBER', 'ID',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'EQUALS', 'SEMICOLON', 'COMMA',
    'GT', 'LT',
    'IF', 'ELSE', 'WHILE',
    'FUNCTION', 'RETURN'
)

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_EQUALS    = r'='
t_SEMICOLON = r';'
t_COMMA     = r','
t_GT        = r'>'
t_LT        = r'<'
t_ignore    = ' \t\n'

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'function': 'FUNCTION',
    'return': 'RETURN'
}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
