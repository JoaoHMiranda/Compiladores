from codegen import compile_to_mips
import sys, os

# força usar mparser.py local antes do parser interno
sys.path.insert(0, os.path.dirname(__file__))

def main():
    if len(sys.argv) > 1:
        src = open(sys.argv[1]).read()
    else:
        src = sys.stdin.read()
    out = compile_to_mips(src)
    with open('saida.txt', 'w') as f:
        f.write(out)

if __name__ == '__main__':
    main()
