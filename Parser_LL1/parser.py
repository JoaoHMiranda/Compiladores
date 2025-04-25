#Joao Henrique Silva de Miranda


def ll1_parser(entrada):
    """
    Parser LL(1) para a gramática:
      S → if E then S else S | a
      E → b | c
    Exibe os passos do parsing e retorna o log final.
    """
    log_lines = []  # Armazena as linhas de log
    def add_line(line):
        log_lines.append(line)
    
    # Tabela de parsing: (não-terminal, token) → produção
    tabela = {
        ("S", "if"): ["if", "E", "then", "S", "else", "S"],
        ("S", "a"): ["a"],
        ("E", "b"): ["b"],
        ("E", "c"): ["c"],
    }
    
    pilha = ["$", "S"]         # Inicializa a pilha com o símbolo inicial e o marcador de fim
    tokens = entrada.split()   # Divide a entrada em tokens (assumindo separação por espaço)
    i = 0                      # Índice do token atual

    add_line("{:<25s} {:<40s} {:<30s}".format("Pilha", "Entrada", "Ação"))
    add_line("-" * 95)
    
    while pilha:
        topo = pilha[-1]  # Obtém o topo da pilha
        token_atual = tokens[i] if i < len(tokens) else None
        current_line = "{:<25s} {:<40s}".format(" ".join(pilha), " ".join(tokens[i:]))
        
        # Se o topo é terminal ou o marcador '$'
        if topo in ["if", "then", "else", "a", "b", "c", "$"]:
            if topo == token_atual:
                pilha.pop()      # Consome o terminal
                i += 1           # Avança para o próximo token
                current_line += " => Match '{}'".format(token_atual)
                add_line(current_line)
            else:
                current_line += " => Erro: esperado '{}', encontrado '{}'".format(topo, token_atual)
                add_line(current_line)
                add_line("Parsing abortado.")
                return "\n".join(log_lines)
        else:
            # Se o topo é não-terminal, procura produção na tabela
            chave = (topo, token_atual)
            if chave in tabela:
                producao = tabela[chave]
                pilha.pop()      # Remove o não-terminal
                # Empilha os símbolos da produção em ordem inversa
                for simbolo in reversed(producao):
                    pilha.append(simbolo)
                current_line += " => Aplicar produção: {} -> {}".format(topo, " ".join(producao))
                add_line(current_line)
            else:
                current_line += " => Erro: não há produção para ({}, {})".format(topo, token_atual)
                add_line(current_line)
                add_line("Parsing abortado.")
                return "\n".join(log_lines)
    
    # Verifica se todos os tokens foram consumidos
    if i == len(tokens):
        add_line("Entrada aceita!")
    else:
        add_line("Erro: entrada não foi completamente consumida.")
    
    return "\n".join(log_lines)

def process_files(input_files):
    """
    Lê cada arquivo de entrada, processa com o parser e grava a saída no arquivo correspondente.
    """
    for input_file in input_files:
        try:
            with open(input_file, "r") as f:
                entrada = f.read().strip()
                tokens = entrada.split()
                if not tokens:
                    print(f"Arquivo {input_file} está vazio. Pulando.")
                    continue
                # Adiciona o marcador '$' se não estiver presente
                if tokens[-1] != "$":
                    entrada += " $"
        except FileNotFoundError:
            print(f"Arquivo '{input_file}' não encontrado. Pulando.")
            continue
        
        print(f"Processando {input_file}...")
        log = ll1_parser(entrada)
        print("Resultado do Parsing:")
        print(log)
        print("\n" + "=" * 80 + "\n")
        
        # Gera o nome do arquivo de saída e grava o log
        output_file = input_file.replace("entrada", "saida")
        with open(output_file, "w") as f:
            f.write(log)
        print(f"Saída escrita em '{output_file}'.\n")

if __name__ == '__main__':
    # Lista dos arquivos de entrada a serem processados
    input_files = ["entrada1.txt", "entrada2.txt", "entrada3.txt", "entrada4.txt", "entrada5.txt", "entrada6.txt"]
    process_files(input_files)
