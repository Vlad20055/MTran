import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from focal_lexer.lexer import LexicalAnalyzer
from focal_lexer.token import TokenType

from collections import OrderedDict
from enum import Enum, auto

def build_tables(tokens):
    """
    Собирает таблицы из списка токенов.
    Возвращает словарь с таблицами: 'identifiers', 'constants', 'keywords', 'delimiters', 'operators'.
    Каждая таблица – список кортежей (номер, лексема, информация).
    Номер присваивается в порядке первого появления.
    """
    tables = {
        'identifiers': [],      # (index, name, info)
        'constants': [],        # (index, value, info)
        'keywords': [],         # (index, word, info)
        'delimiters': [],       # (index, symbol, info)
        'operators': []         # (index, symbol, info)
    }
    
    seen = {
        'identifiers': set(),
        'constants': set(),
        'keywords': set(),
        'delimiters': set(),
        'operators': set()
    }
    
    for tok in tokens:
        # --- Идентификаторы ---
        if tok.type == TokenType.IDENTIFIER:
            if tok.value not in seen['identifiers']:
                seen['identifiers'].add(tok.value)
                tables['identifiers'].append((len(tables['identifiers']) + 1, tok.value, "Переменная (идентификатор)"))
        
        # --- Константы (числа и строки) ---
        elif tok.type == TokenType.NUMBER:
            if tok.value not in seen['constants']:
                seen['constants'].add(tok.value)
                tables['constants'].append((len(tables['constants']) + 1, tok.value, "Числовая константа"))
        elif tok.type == TokenType.STRING:
            if tok.value not in seen['constants']:
                seen['constants'].add(tok.value)
                tables['constants'].append((len(tables['constants']) + 1, tok.value, "Строковая константа"))
        
        # --- Ключевые слова (все KEYWORD_*, кроме COMMENT) ---
        elif tok.type.name.startswith('KEYWORD_') and tok.type != TokenType.KEYWORD_COMMENT:
            if tok.value not in seen['keywords']:
                seen['keywords'].add(tok.value)
                tables['keywords'].append((len(tables['keywords']) + 1, tok.value, "Ключевое слово"))
        
        # --- Встроенные функции (тоже ключевые слова) ---
        elif tok.type.name.startswith('FUNCTION_'):
            func_name = tok.value
            if func_name not in seen['keywords']:
                seen['keywords'].add(func_name)
                tables['keywords'].append((len(tables['keywords']) + 1, func_name, "Встроенная функция"))

        # --- Разделители (все DELIMITER_*) ---
        elif tok.type.name.startswith('DELIMITER_'):
            # Исключаем ! (восклицательный знак в Focal – разделитель строк)
            if tok.value not in seen['delimiters']:
                seen['delimiters'].add(tok.value)
                tables['delimiters'].append((len(tables['delimiters']) + 1, tok.value, "Разделитель"))
        
        # --- Операторы (все OPERATOR_*) ---
        elif tok.type.name.startswith('OPERATOR_'):
            if tok.value not in seen['operators']:
                seen['operators'].add(tok.value)
                tables['operators'].append((len(tables['operators']) + 1, tok.value, "Оператор"))
    
    return tables

def print_table(title, rows, col_names=("№", "Лексема", "Информация")):
    """Выводит таблицу с заголовком и колонками."""
    print(f"\n{title}")
    print("-" * 50)
    # Заголовки
    print(f"{col_names[0]:<5} {col_names[1]:<20} {col_names[2]}")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]}")
    print("-" * 50)

def format_token_sequence(tokens, tables):
    """Превращает поток токенов в строку вида:
       <ИД1>=(<ИД2>+<ИД3>)*<К1>
       с сохранением переводов строк (по номерам строк токенов).
    """
    # Словари для быстрого поиска индекса по значению
    id_map = {name: idx for idx, name, _ in tables['identifiers']}
    const_map = {value: idx for idx, value, _ in tables['constants']}

    parts = []
    last_line = None

    for tok in tokens:
        if tok.type == TokenType.KEYWORD_COMMENT:
            continue

        # Вставляем перевод строки, если номер строки изменился
        if last_line is not None and tok.line != last_line:
            parts.append('\n')
        last_line = tok.line

        if tok.type == TokenType.IDENTIFIER:
            idx = id_map.get(tok.value)
            parts.append(f"<ИД{idx}>" if idx else tok.value)

        elif tok.type in (TokenType.NUMBER, TokenType.STRING):
            idx = const_map.get(tok.value)
            parts.append(f"<К{idx}>" if idx else tok.value)

        elif tok.type.name.startswith('KEYWORD_') or tok.type.name.startswith('FUNCTION_'):
            parts.append(tok.value)

        elif tok.type.name.startswith('OPERATOR_'):
            parts.append(tok.value)

        elif tok.type.name.startswith('DELIMITER_'):
            parts.append(tok.value)

        else:
            parts.append(f"[ERR:{tok.value}]")

    # Возвращаем единую строку
    return ''.join(parts)

def print_errors_table(tokens):
    """Выводит таблицу лексических ошибок (токены UNKNOWN)."""
    errors = [tok for tok in tokens if tok.type == TokenType.UNKNOWN]
    if not errors:
        print("\nЛЕКСИЧЕСКИХ ОШИБОК НЕ ОБНАРУЖЕНО")
        return

    print("\nТАБЛИЦА ЛЕКСИЧЕСКИХ ОШИБОК")
    print("-" * 60)
    print(f"{'№':<5} {'Строка':<7} {'Позиция':<9} {'Ошибочная лексема':<20} {'Описание'}")
    print("-" * 60)
    for i, err in enumerate(errors, start=1):
        # Значение может быть длинным – обрезаем для читаемости
        value_repr = repr(err.value) if '\n' not in err.value else err.value[:20] + '…'
        print(f"{i:<5} {err.line:<7} {err.column:<9} {value_repr:<20} {err.error_string}")
    print("-" * 60)

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
    else:
        source = """1.10 T " Hello, Vlad "!"""
    
    lexer = LexicalAnalyzer(source)
    tokens = lexer.tokenize()
    # Убираем комментарии, если они есть
    tokens = [t for t in tokens if t.type != TokenType.KEYWORD_COMMENT]
    
    tables = build_tables(tokens)
    print_table("ТАБЛИЦА ИМЁН (ИДЕНТИФИКАТОРЫ)", tables['identifiers'])
    print_table("ТАБЛИЦА КОНСТАНТ", tables['constants'])
    print_table("ТАБЛИЦА КЛЮЧЕВЫХ СЛОВ", tables['keywords'])
    print_table("ТАБЛИЦА РАЗДЕЛИТЕЛЕЙ", tables['delimiters'])
    print_table("ТАБЛИЦА ОПЕРАТОРОВ", tables['operators'])

    
    print("\n" + "="*60)
    print("ПОСЛЕДОВАТЕЛЬНОСТЬ ЛЕКСЕМ (в формате лабораторной работы):")
    sequence = format_token_sequence(tokens, tables)
    print(sequence)


    print_errors_table(tokens)


# def main():
#     if len(sys.argv) > 1:
#         with open(sys.argv[1], 'r') as f:
#             source = f.read()
#     else:
#         # Пример программы
#         source = """1.10 T " Hello, Vlad "!"""
#     lexer = LexicalAnalyzer(source)
#     tokens = lexer.tokenize()
#     # Фильтруем комментарии
#     tokens = [t for t in tokens if t.type != TokenType.KEYWORD_COMMENT]
#     for num, tok in enumerate(tokens):
#         # print(f"<ИД_{num + 1}>  {tok.value:<15}   {tok.type}")
#         print(f"<ИД_{num + 1:<3}>  {tok}")


if __name__ == "__main__":
    main()