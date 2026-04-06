import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from focal_lexer.lexer import LexicalAnalyzer
from focal_lexer.token import TokenType
from focal_lexer.symbol_table import SymbolTable

def main():
    # Инициализируем таблицу символов
    symbol_table = SymbolTable()
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
    else:
        # Пример программы
        source = """1.10 T " Hello, Vlad "!"""
    
    lexer = LexicalAnalyzer(source)
    tokens = lexer.tokenize()
    
    # Обрабатываем токены и добавляем в таблицы
    for tok in tokens:
        if tok.type == TokenType.IDENTIFIER:
            symbol_table.add_identifier(tok.value, "Переменная с плавающей точкой")
        elif tok.type == TokenType.NUMBER:
            symbol_table.add_constant(tok.value, "Константа с плавающей точкой")
    
    # Фильтруем комментарии
    tokens = [t for t in tokens if t.type != TokenType.KEYWORD_COMMENT]
    
    print("\n" + "="*70)
    print("                    РЕЗУЛЬТАТЫ ЛЕКСИЧЕСКОГО АНАЛИЗА")
    print("="*70)
    
    print("\nПолученные токены:")
    print("─" * 70)
    for num, tok in enumerate(tokens):
        print(f"<ИД_{num + 1:<3}>  {tok}")
    
    # Выводим все таблицы символов
    symbol_table.print_all_tables()


if __name__ == "__main__":
    main()