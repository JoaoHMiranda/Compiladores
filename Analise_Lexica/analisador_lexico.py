# João Henrique Silva de Miranda

# =====================================================
# Analisador Léxico em Python para a linguagem fictícia
# Lê 6 arquivos de código-fonte:
#   fonte_entrada1.txt,
#   fonte_entrada2.txt,
#   fonte_entrada3.txt
#   fonte_entrada4.txt
#   fonte_entrada5.txt
#   fonte_entrada6.txt
# e gera 6 arquivos de saída correspondentes:
#   fonte_saida1.txt,
#   fonte_saida2.txt,
#   fonte_saida3.txt
#   fonte_saida4.txt
#   fonte_saida5.txt
#   fonte_saida6.txt
# Também imprime as listas de tokens no console.
# =====================================================

# REGRAS DA LINGUAGEM (resumo):
# - Palavras-chave: if, else, while, int, float
# - Identificadores: Sequências de letras e dígitos (0-9), começando com letra
# - Operadores: +, -, *, /, =, !=, <=, >=
# - Pontuação: (, ), {, }, ;
# - Literais:
#    * Inteiros (ex.: 10, 42)
#    * Ponto flutuante (ex.: 3.14, 0.0)
#    * Strings entre aspas duplas (ex.: "texto")
# - Comentários: texto após // até o final da linha (ignorado)
# - Espaços e tabulações são ignorados

# -----------------------------
# ARQUIVOS DE ENTRADA E SAÍDA
# -----------------------------
input_files = [
    "fonte_entrada1.txt",
    "fonte_entrada2.txt",
    "fonte_entrada3.txt",
    #"fonte_entrada4.txt",
    #"fonte_entrada5.txt",
    #"fonte_entrada6.txt"
]

output_files = [
    "fonte_saida1.txt",
    "fonte_saida2.txt",
    "fonte_saida3.txt",
    #"fonte_saida4.txt",
    #"fonte_saida5.txt",
    #"fonte_saida6.txt"
]

# -----------------------------
# TABELAS DE TOKENS RECONHECIDOS
# -----------------------------
KEYWORDS = {"if", "else", "while", "int", "float"}
OPERATORS = {"+", "-", "*", "/", "=", "!=", "<=", ">="}
PUNCTUATION = {"(", ")", "{", "}", ";"}

def tokenize(code):
    """
    Recebe uma string 'code' e retorna uma lista de tokens
    no formato (lexema, tipo).
    """
    tokens = []
    i = 0
    length = len(code)

    while i < length:
        char = code[i]

        # Ignorar espaços, tabulações e quebras de linha
        if char in [' ', '\t', '\n', '\r']:
            i += 1
            continue

        # Ignorar comentários que começam com //
        if char == '/' and i + 1 < length and code[i + 1] == '/':
            # Avança até o fim da linha ou do código
            i += 2
            while i < length and code[i] != '\n':
                i += 1
            continue

        # Strings: tudo entre aspas duplas
        if char == '"':
            string_literal = '"'
            i += 1
            while i < length and code[i] != '"':
                string_literal += code[i]
                i += 1
            if i < length:
                # inclui a aspa de fechamento
                string_literal += '"'
                i += 1
            tokens.append((string_literal, "literal string"))
            continue

        # Operadores de dois caracteres ( !=, <=, >= )
        if char in ['!', '<', '>'] and i + 1 < length:
            possible_op = char + code[i + 1]
            if possible_op in OPERATORS:
                tokens.append((possible_op, "operador"))
                i += 2
                continue

        # Operadores de um caractere ( +, -, *, /, = )
        if char in ['+', '-', '*', '/', '=']:
            if char in OPERATORS:
                tokens.append((char, "operador"))
                i += 1
                continue

        # Pontuação: (, ), {, }, ;
        if char in PUNCTUATION:
            tokens.append((char, "pontuacao"))
            i += 1
            continue

        # Verificar se é letra ou underline (início de identificador/palavra-chave)
        if char.isalpha() or char == '_':
            lexeme = char
            i += 1
            # Continua enquanto for letra, dígito ou underline
            while i < length and (code[i].isalnum() or code[i] == '_'):
                lexeme += code[i]
                i += 1
            if lexeme in KEYWORDS:
                tokens.append((lexeme, "palavra-chave"))
            else:
                tokens.append((lexeme, "identificador"))
            continue

        # Verificar se é dígito (início de número inteiro ou float)
        if char.isdigit():
            lexeme = char
            i += 1
            has_dot = False
            while i < length and (code[i].isdigit() or code[i] == '.'):
                if code[i] == '.':
                    if has_dot:
                        # Segundo ponto decimal (não tratado neste exercício)
                        pass
                    has_dot = True
                lexeme += code[i]
                i += 1
            if has_dot:
                tokens.append((lexeme, "literal float"))
            else:
                tokens.append((lexeme, "literal inteiro"))
            continue

        # Caractere não reconhecido
        tokens.append((char, "desconhecido"))
        i += 1

    return tokens


if __name__ == "__main__":
    # Para cada arquivo de entrada, processamos e geramos a saída correspondente
    for inp_file, out_file in zip(input_files, output_files):
        # 1) Ler o conteúdo do arquivo de entrada
        with open(inp_file, 'r', encoding='utf-8') as f:
            code_content = f.read()

        # 2) Tokenizar o código-fonte
        tokens = tokenize(code_content)

        # 3) Salvar os tokens em out_file
        with open(out_file, 'w', encoding='utf-8') as out:
            for tk in tokens:
                out.write(f"{tk}\n")

        # 4) Imprimir no console
        print(f"=== TOKENS DE {inp_file} ===")
        for tk in tokens:
            print(tk)
        print(f"\nTokens gravados em '{out_file}'.\n{'-'*40}\n")
