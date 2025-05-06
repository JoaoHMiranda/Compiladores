from ply_arithmetic_parser import parser, remove_comments

# Lista completa de casos de teste
commands = [
    "10",
    # Atribuição
    "x = 10",
    "x + 5",
    "x = 10 + 5 * 2",
    "x = x - x",
    # Operações básicas
    "3 + 5",
    "2 ^ 3 * 4",
    "(3 + 5) * 2",
    "-3 + 2",
    # Funções matemáticas
    "sin(0)",
    "sqrt(16)",
    "cos(3.14159)",
    # Comentários e linhas vazias
    "// este é um comentário",
    "",
    "/* bloco */ 2 * 2",
    "/* a /* aninhado */ fim */ 4 - 1",
    # Erro léxico
    "3 @ 5",
    # Erro sintático / recuperação
    "3 + + 5",
    # Divisão por zero
    "10 / 0",
]

for cmd in commands:
    print(f"> {cmd}")
    # Remover comentários para decidir se deve pular
    clean = remove_comments(cmd)
    if not clean.strip():  # linha vazia ou só comentário
        print()
        continue
    try:
        result = parser.parse(cmd)
        if result is not None:
            print(result)
    except ZeroDivisionError:
        print("Erro: divisão por zero")
    print()  # quebra de linha para legibilidade
