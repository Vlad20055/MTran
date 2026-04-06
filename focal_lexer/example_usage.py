"""
Расширенный пример использования таблиц символов (Symbol Tables)

This example demonstrates:
1. Как использовать SymbolTable с LexicalAnalyzer
2. Как добавлять и извлекать информацию из таблиц
3. Как фильтровать и анализировать данные таблиц
"""

import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from focal_lexer import LexicalAnalyzer, SymbolTable, TokenType


def example_1_basic_usage():
    """Пример 1: Базовое использование"""
    print("\n" + "="*70)
    print("ПРИМЕР 1: Базовое использование таблиц символов")
    print("="*70)
    
    symbol_table = SymbolTable()
    
    # Добавляем идентификаторы
    print("\n1. Добавляем идентификаторы:")
    id1 = symbol_table.add_identifier('COST', 'Переменная с плавающей точкой')
    print(f"   COST → ID #{id1}")
    
    id2 = symbol_table.add_identifier('PRICE', 'Переменная с плавающей точкой')
    print(f"   PRICE → ID #{id2}")
    
    id3 = symbol_table.add_identifier('TAX', 'Переменная с плавающей точкой')
    print(f"   TAX → ID #{id3}")
    
    # Добавляем константы
    print("\n2. Добавляем константы:")
    c1 = symbol_table.add_constant('0.98', 'Константа с плавающей точкой')
    print(f"   0.98 → ID #{c1}")
    
    c2 = symbol_table.add_constant('10.5', 'Константа с плавающей точкой')
    print(f"   10.5 → ID #{c2}")
    
    # Проверяем, что при повторном добавлении возвращается существующий ID
    print("\n3. Проверяем повторное добавление (должны вернуться существующие ID):")
    id_cost_again = symbol_table.add_identifier('COST')
    print(f"   COST (повторно) → ID #{id_cost_again} (был {id1}, совпадает: {id_cost_again == id1})")
    
    const_098_again = symbol_table.add_constant('0.98')
    print(f"   0.98 (повторно) → ID #{const_098_again} (был {c1}, совпадает: {const_098_again == c1})")
    
    # Получаем информацию
    print("\n4. Получаем информацию об элементах:")
    cost_info = symbol_table.get_identifier('COST')
    print(f"   COST: {cost_info}")
    
    const_info = symbol_table.get_constant('0.98')
    print(f"   0.98: {const_info}")


def example_2_keyword_operations():
    """Пример 2: Работа с ключевыми словами и функциями"""
    print("\n" + "="*70)
    print("ПРИМЕР 2: Ключевые слова и функции")
    print("="*70)
    
    symbol_table = SymbolTable()
    
    print("\n1. Проверка ключевых слов:")
    commands = ['C', 'A', 'T', 'S', 'I', 'F', 'D', 'R', 'G', 'Q', 'E']
    for cmd in commands:
        kw = symbol_table.keywords.get(cmd)
        if kw:
            print(f"   '{cmd}' → {kw['name']}")
    
    print("\n2. Проверка функций:")
    functions = ['FSIN', 'FCOS', 'FABS', 'FSGN']
    for func in functions:
        f = symbol_table.functions.get(func)
        if f:
            print(f"   {func} → {f['description']}")
    
    print("\n3. Проверка операторов:")
    operators = ['+', '-', '*', '/', '^', '=']
    for op in operators:
        o = symbol_table.operators.get(op)
        if o:
            print(f"   '{op}' → {o['operation']}")


def example_3_lexer_integration():
    """Пример 3: Интеграция с лексером"""
    print("\n" + "="*70)
    print("ПРИМЕР 3: Интеграция с лексером")
    print("="*70)
    
    symbol_table = SymbolTable()
    
    # Пример исходного кода
    source_code = """
1.10 T "Пример программы"!
2.20 S X = 5.5;
3.30 S Y = 10;
4.40 S Z = X * Y;
5.50 T Z;
6.60 Q;
"""
    
    print("\n1. Исходный код:")
    print(source_code)
    
    # Запускаем лексический анализ
    print("\n2. Выполняем лексический анализ...")
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()
    
    # Собираем информацию в таблицы
    print("\n3. Собираем информацию в таблицы:")
    for tok in tokens:
        if tok.type == TokenType.IDENTIFIER:
            symbol_table.add_identifier(tok.value, "Переменная с плавающей точкой")
            print(f"   Найден идентификатор: {tok.value}")
        elif tok.type == TokenType.NUMBER:
            symbol_table.add_constant(tok.value, "Константа с плавающей точкой")
    
    # Выводим статистику
    print(f"\n4. Статистика:")
    print(f"   Уникальных идентификаторов: {len(symbol_table.identifiers)}")
    print(f"   Уникальных констант: {len(symbol_table.constants)}")
    print(f"   Всего токенов: {len(tokens)}")
    
    # Выводим заполненные таблицы
    print("\n5. Таблицы идентификаторов и констант:")
    symbol_table.print_identifiers_table()
    symbol_table.print_constants_table()


def example_4_detailed_print():
    """Пример 4: Подробный вывод всех таблиц"""
    print("\n" + "="*70)
    print("ПРИМЕР 4: Полный вывод всех таблиц")
    print("="*70)
    
    symbol_table = SymbolTable()
    
    # Добавляем примеры идентификаторов и констант
    symbol_table.add_identifier('COST', 'Переменная')
    symbol_table.add_identifier('PRICE', 'Переменная')
    symbol_table.add_constant('0.98', 'Константа')
    symbol_table.add_constant('100', 'Константа')
    
    # Выводим все таблицы
    symbol_table.print_all_tables()


def main():
    """Запуск всех примеров"""
    example_1_basic_usage()
    example_2_keyword_operations()
    example_3_lexer_integration()
    example_4_detailed_print()
    
    print("\n" + "="*70)
    print("Все примеры выполнены успешно!")
    print("="*70)


if __name__ == "__main__":
    main()
