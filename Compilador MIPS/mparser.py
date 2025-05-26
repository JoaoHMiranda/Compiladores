import ply.yacc as yacc
from lexer import tokens

class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children or []
        self.leaf = leaf

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_program(p):
    'program : declaration_list'
    p[0] = Node('program', p[1].children)

def p_declaration_list_single(p):
    'declaration_list : declaration'
    p[0] = Node('declaration_list', [p[1]])

def p_declaration_list_multi(p):
    'declaration_list : declaration_list declaration'
    p[0] = Node('declaration_list', p[1].children + [p[2]])

def p_declaration(p):
    '''declaration : func_def
                   | statement'''
    p[0] = p[1]

def p_func_def(p):
    'func_def : FUNCTION ID LPAREN param_list RPAREN LBRACE statement_list RETURN expression SEMICOLON RBRACE'
    p[0] = Node('func_def', [p[4], p[6], p[8]], leaf=p[2])

def p_param_list_empty(p):
    'param_list : '
    p[0] = Node('param_list', [])

def p_param_list_single(p):
    'param_list : ID'
    p[0] = Node('param_list', [p[1]])

def p_param_list_multi(p):
    'param_list : param_list COMMA ID'
    p[0] = Node('param_list', p[1].children + [p[3]])

def p_expression_call(p):
    'expression : ID LPAREN arg_list RPAREN'
    p[0] = Node('call', p[3].children, leaf=p[1])

def p_arg_list_empty(p):
    'arg_list : '
    p[0] = Node('arg_list', [])

def p_arg_list_single(p):
    'arg_list : expression'
    p[0] = Node('arg_list', [p[1]])

def p_arg_list_multi(p):
    'arg_list : arg_list COMMA expression'
    p[0] = Node('arg_list', p[1].children + [p[3]])

def p_statement_list_single(p):
    'statement_list : statement'
    p[0] = Node('statement_list', [p[1]])

def p_statement_list_multi(p):
    'statement_list : statement_list statement'
    p[0] = Node('statement_list', p[1].children + [p[2]])

def p_statement(p):
    '''statement : assign
                 | if_statement
                 | if_else_statement
                 | while_statement'''
    p[0] = p[1]

def p_assign(p):
    'assign : ID EQUALS expression SEMICOLON'
    p[0] = Node('assign', [p[3]], leaf=p[1])

def p_if_statement(p):
    'if_statement : IF LPAREN expression GT expression RPAREN LBRACE statement_list RBRACE'
    p[0] = Node('if', [p[3], p[5], p[8]])

def p_if_else_statement(p):
    'if_else_statement : IF LPAREN expression GT expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE'
    p[0] = Node('if_else', [p[3], p[5], p[8], p[12]])

def p_while_statement(p):
    'while_statement : WHILE LPAREN expression GT expression RPAREN LBRACE statement_list RBRACE'
    p[0] = Node('while', [p[3], p[5], p[8]])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = Node('binop', [p[1], p[3]], leaf=p[2])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Node('number', leaf=p[1])

def p_expression_id(p):
    'expression : ID'
    p[0] = Node('id', leaf=p[1])

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

parser = yacc.yacc()
