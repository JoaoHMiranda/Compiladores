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

## 🏛️ Arquitetura do Interpretador

O arquivo minilang.py é autocontido e dividido em três componentes principais, seguindo o design clássico de um interpretador:

Lexer (Analisador Léxico):
Responsável por ler o código-fonte como texto puro e convertê-lo em uma sequência de tokens (números, operadores, palavras-chave, etc.).

Parser (Analisador Sintático):
Recebe a sequência de tokens do Lexer e a organiza em uma estrutura de árvore chamada AST (Árvore de Sintaxe Abstrata – Abstract Syntax Tree). A AST representa a estrutura hierárquica do código. Se a sintaxe estiver incorreta, o Parser levanta um erro.

Interpreter (Avaliador):
Percorre a AST gerada pelo Parser. Para cada nó da árvore, executa a operação correspondente, manipulando variáveis, chamando funções e produzindo o resultado final do script.

## 🔧 Requisitos
Python 3.6 ou superior

(Opcional) Ambiente virtual para instalação isolada de dependências