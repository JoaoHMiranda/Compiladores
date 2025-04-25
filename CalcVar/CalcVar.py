import io
import contextlib

# ----------------------------
# DEFINIÇÃO DOS COMPONENTES DO COMPILADOR
# ----------------------------

# 1. Token e Analisador Léxico
class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo  # Exemplos: "INT", "IDENT", "NUMERO", "IGUAL", "MAIS", "MENOS", "PONTO_VIRGULA", "EOF"
        self.valor = valor

    def __str__(self):
        return f"[{self.tipo}: {self.valor}]"

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.atual = self.texto[self.pos] if self.texto else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.texto):
            self.atual = self.texto[self.pos]
        else:
            self.atual = None

    def skip_whitespace(self):
        while self.atual is not None and self.atual.isspace():
            self.advance()

    def skip_comment(self):
        # Pula todos os caracteres até o final da linha ou fim do texto
        while self.atual is not None and self.atual != "\n":
            self.advance()

    def integer(self):
        """Reconhece números inteiros."""
        resultado = ""
        while self.atual is not None and self.atual.isdigit():
            resultado += self.atual
            self.advance()
        return int(resultado)

    def identifier(self):
        """Reconhece identificadores e palavras-chave."""
        resultado = ""
        while self.atual is not None and (self.atual.isalnum() or self.atual == '_'):
            resultado += self.atual
            self.advance()
        return resultado

    def get_next_token(self):
        while self.atual is not None:
            if self.atual.isspace():
                self.skip_whitespace()
                continue

            # Verifica se inicia um comentário com "//"
            if self.atual == '/':
                self.advance()
                if self.atual == '/':
                    self.advance()
                    self.skip_comment()
                    continue
                else:
                    raise Exception(f"Caractere inválido: /")

            if self.atual.isalpha():
                id_str = self.identifier()
                if id_str == "int":
                    return Token("INT", id_str)
                else:
                    return Token("IDENT", id_str)

            if self.atual.isdigit():
                num = self.integer()
                return Token("NUMERO", num)

            if self.atual == '=':
                self.advance()
                return Token("IGUAL", '=')

            if self.atual == '+':
                self.advance()
                return Token("MAIS", '+')

            if self.atual == '-':
                self.advance()
                return Token("MENOS", '-')

            if self.atual == ';':
                self.advance()
                return Token("PONTO_VIRGULA", ';')

            # Se encontrar um caractere não reconhecido
            raise Exception(f"Caractere inválido: {self.atual}")

        return Token("EOF", None)

# 2. Nós da Árvore Sintática Abstrata (AST)
class AST:
    pass

class DeclarationNode(AST):
    def __init__(self, var_nome, expr):
        self.var_nome = var_nome  # Nome da variável declarada
        self.expr = expr          # Expressão associada

    def __str__(self):
        return f"Declaracao: {self.var_nome} = {self.expr}"

    def __repr__(self):
        return self.__str__()

class AssignmentNode(AST):
    def __init__(self, var_nome, expr):
        self.var_nome = var_nome  # Nome da variável para atribuição
        self.expr = expr          # Expressão da atribuição

    def __str__(self):
        return f"Atribuicao: {self.var_nome} = {self.expr}"

    def __repr__(self):
        return self.__str__()

class NumberNode(AST):
    def __init__(self, valor):
        self.valor = valor  # Valor numérico

    def __str__(self):
        return f"{self.valor}"

    def __repr__(self):
        return self.__str__()

class VariableNode(AST):
    def __init__(self, var_nome):
        self.var_nome = var_nome  # Nome da variável

    def __str__(self):
        return self.var_nome

    def __repr__(self):
        return self.__str__()

class OperationNode(AST):
    def __init__(self, operador, esquerdo, direito):
        self.operador = operador  # Operador: '+' ou '-'
        self.esquerdo = esquerdo
        self.direito = direito

    def __str__(self):
        return f"({self.esquerdo} {self.operador} {self.direito})"

    def __repr__(self):
        return self.__str__()

# 3. Analisador Sintático (Parser)
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.atual = self.lexer.get_next_token()

    def error(self, msg="Erro de sintaxe"):
        raise Exception(msg)

    def eat(self, token_tipo):
        if self.atual.tipo == token_tipo:
            self.atual = self.lexer.get_next_token()
        else:
            self.error(f"Token inesperado: Esperado {token_tipo}, mas encontrou {self.atual.tipo}")

    def parse(self):
        """Retorna uma lista de nós da AST representando o programa."""
        nodes = []
        while self.atual.tipo != "EOF":
            node = self.statement()
            nodes.append(node)
        return nodes

    def statement(self):
        """
        Reconhece:
         - Declaração: int <ident> = <expressao> ;
         - Atribuição: <ident> = <expressao> ;
        """
        if self.atual.tipo == "INT":
            self.eat("INT")
            if self.atual.tipo != "IDENT":
                self.error("Esperado identificador após 'int'")
            var_nome = self.atual.valor
            self.eat("IDENT")
            self.eat("IGUAL")
            expr = self.expression()
            self.eat("PONTO_VIRGULA")
            return DeclarationNode(var_nome, expr)
        elif self.atual.tipo == "IDENT":
            var_nome = self.atual.valor
            self.eat("IDENT")
            self.eat("IGUAL")
            expr = self.expression()
            self.eat("PONTO_VIRGULA")
            return AssignmentNode(var_nome, expr)
        else:
            self.error("Declaração ou atribuição esperada")

    def expression(self):
        """Processa expressões com '+' e '-' (da esquerda para a direita)."""
        node = self.term()
        while self.atual.tipo in ("MAIS", "MENOS"):
            token = self.atual
            if token.tipo == "MAIS":
                self.eat("MAIS")
            elif token.tipo == "MENOS":
                self.eat("MENOS")
            direito = self.term()
            node = OperationNode(token.valor, node, direito)
        return node

    def term(self):
        """Processa um termo: número ou identificador."""
        token = self.atual
        if token.tipo == "NUMERO":
            self.eat("NUMERO")
            return NumberNode(token.valor)
        elif token.tipo == "IDENT":
            self.eat("IDENT")
            return VariableNode(token.valor)
        else:
            self.error("Esperado número ou identificador")

# 4. Analisador Semântico
class SemanticAnalyzer:
    def __init__(self, ast_nodes):
        self.ast_nodes = ast_nodes
        self.tabela_simbolos = {}  # Mapeia as variáveis declaradas (nome -> tipo)
        self.erros = []

    def analyze(self):
        for node in self.ast_nodes:
            self.visit(node)
        if self.erros:
            for err in self.erros:
                print("Erro semântico:", err)
        else:
            print("Semântica: Programa válido")

    def visit(self, node):
        if isinstance(node, DeclarationNode):
            return self.visit_declaration(node)
        elif isinstance(node, AssignmentNode):
            return self.visit_assignment(node)
        elif isinstance(node, OperationNode):
            return self.visit_operation(node)
        elif isinstance(node, NumberNode):
            return "int"
        elif isinstance(node, VariableNode):
            return self.visit_variable(node)
        else:
            self.erros.append("Nó desconhecido na AST")

    def visit_declaration(self, node):
        tipo_expr = self.visit(node.expr)
        if tipo_expr != "int":
            self.erros.append(f"Tipo inválido na declaração da variável '{node.var_nome}'")
        self.tabela_simbolos[node.var_nome] = "int"
        return "int"

    def visit_assignment(self, node):
        if node.var_nome not in self.tabela_simbolos:
            self.erros.append(f"Variável '{node.var_nome}' não declarada")
        tipo_expr = self.visit(node.expr)
        if tipo_expr != "int":
            self.erros.append(f"Tipo inválido na atribuição da variável '{node.var_nome}'")
        return "int"

    def visit_operation(self, node):
        tipo_esq = self.visit(node.esquerdo)
        tipo_dir = self.visit(node.direito)
        if tipo_esq != "int" or tipo_dir != "int":
            self.erros.append("Operação com tipos inválidos")
        return "int"

    def visit_variable(self, node):
        if node.var_nome not in self.tabela_simbolos:
            self.erros.append(f"Variável '{node.var_nome}' não declarada")
            return None
        return self.tabela_simbolos[node.var_nome]

# Função que integra todas as fases do compilador
def run_compiler(codigo):
    print("Código:", codigo)
    
    # Fase 1: Análise Léxica
    lexer = Lexer(codigo)
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.tipo == "EOF":
            break
    print("Tokens:", tokens)
    
    # Fase 2: Análise Sintática
    parser = Parser(Lexer(codigo))
    try:
        ast = parser.parse()
        print("AST:", ast)
    except Exception as e:
        print("Erro de parsing:", e)
        return
    
    # Fase 3: Análise Semântica
    semantico = SemanticAnalyzer(ast)
    semantico.analyze()

# ----------------------------
# FUNÇÕES PARA TRABALHAR COM ARQUIVOS TXT
# ----------------------------

def run_compiler_test(input_filename, output_filename):
    # Lê o código do arquivo de entrada
    with open(input_filename, "r", encoding="utf-8") as infile:
        codigo = infile.read()
    
    # Captura toda a saída da execução
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        try:
            run_compiler(codigo)
        except Exception as e:
            print("Erro:", e)
    result = out.getvalue()
    
    # Exibe o resultado no console
    print(f"--- Resultado de {input_filename} ---")
    print(result)
    print(f"--- Fim do resultado de {input_filename} ---\n")
    
    # Grava o resultado em um arquivo de saída separado
    with open(output_filename, "w", encoding="utf-8") as outfile:
        outfile.write(result)

# ----------------------------
# FUNÇÃO PRINCIPAL
# ----------------------------
def main():
    # Executa os testes e gera arquivos de saída para cada caso
    run_compiler_test("codigo1.txt", "resultado1.txt")
    run_compiler_test("codigo2.txt", "resultado2.txt")
    run_compiler_test("codigo3.txt", "resultado3.txt")
    run_compiler_test("codigo4.txt", "resultado4.txt")
    run_compiler_test("codigo5.txt", "resultado5.txt")
    run_compiler_test("codigo6.txt", "resultado6.txt")

if __name__ == "__main__":
    main()
