import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from focal_parser.parser import parse_source, dump_ast, ParseError


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 focal_parser/main.py <source.foc>')
        return
    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    try:
        program = parse_source(source)
        print('Parsed program successfully.')
        print(dump_ast(program))
    except ParseError as e:
        print(e)


if __name__ == '__main__':
    main()
