# PLY Arithmetic Parser

Este projeto implementa um analisador léxico-sintático para expressões aritméticas em Python, usando a biblioteca **PLY (Python Lex-Yacc)**. Suporta:

* **Números**: inteiros e decimais.
* **Operadores**: `+`, `-`, `*`, `/`, `^` (potência).
* **Menos unário**: ex.: `-3`.
* **Parênteses**: agrupamento de expressões.
* **Variáveis**: atribuição com `=` e reutilização.
* **Funções**: `sin()`, `cos()`, `sqrt()`.
* **Comentários**: de linha (`// ...`) e blocos aninhados (`/* ... */`).
* **Tratamento de erros** léxicos e sintáticos.
* **Divisão por zero** capturada.
* **REPL interativo** com comando `exit` para sair.

---

## Instalação

1. **Clonar ou baixar** este repositório.
2. Instalar o PLY:

   ```bash
   pip install ply
   ```

## Arquivos Principais

* `ply_arithmetic_parser.py`: implementação do lexer, parser e REPL.
* `teste.py`: script que executa uma variedade de comandos de teste e mostra a saída.

## Uso

### 1. REPL Interativo

Execute:

```bash
python3 ply_arithmetic_parser.py
```

Você verá:

```
Calc > (digite 'exit' para sair)
```

Digite expressões como:

```
> 3 + 5
8

> x = 10
10
> x * 2
20
> sin(0)
0.0
```

Para sair, digite `exit` e pressione Enter.

### 2. Script de Demonstração (teste.py)

Para executar todos os casos de teste manual:

```bash
python3 teste.py
```

Você verá cada comando precedido de `>`, seguido da saída correspondente, incluindo:

```
> 3 + 5
8

> 2 ^ 3 * 4
32

> (3 + 5) * 2
16

> -3 + 2
-1

> sin(0)
0.0

> sqrt(16)
4.0

> cos(3.14159)
-0.9999999999964793

> // este é um comentário

> 3 @ 5
Caractere ilegal: '@' na posição 2
3

> 3 + + 5
Erro sintático no token '+'
8

> 10 / 0
Erro: divisão por zero
```

