import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from focal_lexer.lexer import LexicalAnalyzer
from focal_lexer.token import TokenType

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
    else:
        # Пример программы
        source = """1.10 T " Hello, Vlad "!"""
    lexer = LexicalAnalyzer(source)
    tokens = lexer.tokenize()
    # Фильтруем комментарии
    tokens = [t for t in tokens if t.type != TokenType.KEYWORD_COMMENT]
    for num, tok in enumerate(tokens):
        # print(f"<ИД_{num + 1}>  {tok.value:<15}   {tok.type}")
        print(f"<ИД_{num + 1:<3}>  {tok}")


if __name__ == "__main__":
    main()