import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from focal_parser.parser import parse_source, ParseError
from focal_semantic.semantic import analyze_program, SemanticError
from focal_interpreter.interpreter import interpret_program


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 focal_interpreter/main.py <source.foc>')
        return
    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    try:
        program = parse_source(source)
        errors = analyze_program(program)
        if errors:
            print('Semantic errors:')
            for err in errors:
                print(f"  {err}")
            return
        print('Running program...')
        interpret_program(program)
        print('Program finished.')
    except ParseError as e:
        print(f'Parse error: {e}')
    except Exception as e:
        print(f'Runtime error: {e}')


if __name__ == '__main__':
    main()
