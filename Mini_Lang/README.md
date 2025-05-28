# MiniLang – Interpretador em Python

Este repositório contém o código-fonte de um interpretador para uma linguagem de script simples e dinâmica, apelidada de **MiniLang**. O interpretador foi escrito em Python como projeto de estudo para explorar os conceitos de análise léxica (lexing), análise sintática (parsing) e avaliação (interpretação) de uma linguagem de programação.

## ✨ Funcionalidades

A MiniLang suporta um conjunto robusto de funcionalidades essenciais para uma linguagem de script moderna:

- **Tipos de Dados:**
  - `Number` (inteiros e ponto-flutuante)
  - `String` (delimitadas por aspas duplas)
  - `Boolean` (`true` e `false`)
- **Estruturas de Dados:**
  - `Array` (listas, ex.: `[1, "dois", 3]`)
  - `Object` (dicionários chave-valor, ex.: `{"chave": "valor"}`)
- **Variáveis:** Atribuição simples (`=`) e composta (`+=`, `-=`, `*=`, etc.)
- **Operadores:**
  - **Aritméticos:** `+`, `-`, `*`, `/`, `%`, `**` (potência)
  - **Relacionais:** `==`, `!=`, `<`, `>`, `<=`, `>=`
  - **Lógicos:** `&&` (e), `||` (ou), `!` (não)
- **Estruturas de Controle:**
  - Condicionais: `if` / `else` / `end`
  - Laços de repetição: `while` / `end`
- **Funções:**
  - Definição e chamada de funções com parâmetros
  - Suporte completo a **recursão**
  - Comando `return` para retornar valores
- **Funções Nativas:**
  - `print(...)` — imprime um ou mais valores na saída padrão
  - `input()` — lê uma linha da entrada padrão
- **Comentários:** Linhas iniciadas com `#` são ignoradas pelo interpretador

## 🚀 Como Executar

Para rodar um script em MiniLang, use o interpretador `minilang.py` passando o caminho do arquivo:

```bash
python3 minilang.py <caminho_do_arquivo>.minilang

```

## 📚 Sintaxe da Linguagem (Exemplos)
Abaixo estão exemplos que demonstram a sintaxe da MiniLang.

1. Variáveis e Tipos de Dados

```bash
# Declaração de variáveis
nome = "Mundo"
idade = 10
pi = 3.14
ativo = true

print("Olá,", nome) # Saída: Olá, Mundo

```

2. Arrays e Objetos

```bash
# Array (lista)
numeros = [10, 20, 30, 40]
print("O primeiro número é:", numeros[0]) # Saída: O primeiro número é: 10
numeros[1] = 25 # Modifica um elemento

# Object (dicionário)
pessoa = {"nome": "Ana", "idade": 32}
print(pessoa["nome"], "tem", pessoa["idade"], "anos.") # Saída: Ana tem 32 anos.
```

3. Estruturas de Controle

```bash
# if/else
x = 20
if x > 15
    print("x é maior que 15")
else
    print("x não é maior que 15")
end if

# while
i = 0
sum = 0
while i <= 5
    sum += i
    i += 1
end while
print("A soma de 0 a 5 é:", sum) # Saída: A soma de 0 a 5 é: 15

```
4. Funções e Recursão

```bash
# Função para calcular o fatorial de forma recursiva
func fatorial(n)
    # Caso base
    if n < 2
        return 1
    end if

    # Passo recursivo
    return n * fatorial(n - 1)
end func

resultado = fatorial(5)
print("Fatorial de 5 é:", resultado) # Saída: Fatorial de 5 é: 120
```

## 📂 Arquivos de Exemplo
O projeto inclui scripts de exemplo para demonstrar as funcionalidades da linguagem:

`soma_array.minilang`: Demonstra a criação de arrays e a iteração com um laço `while`.
`fatorial_recursivo.minilang`: Demonstra a definição e chamada de uma função recursiva.

## 🏛️ Arquitetura do Interpretador

O arquivo `minilang.py` é autocontido e dividido em três componentes principais, seguindo o design clássico de um interpretador:

Lexer (Analisador Léxico):
Responsável por ler o código-fonte como texto puro e convertê-lo em uma sequência de tokens (números, operadores, palavras-chave, etc.).

Parser (Analisador Sintático):
Recebe a sequência de tokens do Lexer e a organiza em uma estrutura de árvore chamada AST (Árvore de Sintaxe Abstrata – Abstract Syntax Tree). A AST representa a estrutura hierárquica do código. Se a sintaxe estiver incorreta, o Parser levanta um erro.

Interpreter (Avaliador):
Percorre a AST gerada pelo Parser. Para cada nó da árvore, executa a operação correspondente, manipulando variáveis, chamando funções e produzindo o resultado final do script.

## 🔧 Requisitos
Python 3.6 ou superior

(Opcional) Ambiente virtual para instalação isolada de dependências

## 👨‍💻 Autor
**João H. (joaoh)** 