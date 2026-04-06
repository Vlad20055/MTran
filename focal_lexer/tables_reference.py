"""
КРАТКИЙ СПРАВОЧНИК: Таблицы символов (Symbol Tables)

После лексического анализа в focal_lexer создаются следующие таблицы:
"""

KEYWORDS_TABLE = {
    "C": "COMMENT (Комментарий)",
    "A": "ASK (Ввод)",
    "T": "TYPE (Вывод)",
    "S": "SET (Присваивание)",
    "I": "IF (Условие)",
    "F": "FOR (Цикл)",
    "D": "DO (Выполнить)",
    "R": "RETURN (Возврат)",
    "G": "GO (Переход)",
    "Q": "QUIT (Выход)",
    "E": "ERASE (Очистка)",
}

FUNCTIONS_TABLE = {
    "FSIN": "Синус",
    "FCOS": "Косинус",
    "FATN": "Арктангенс",
    "FEXP": "Экспонента",
    "FLOG": "Логарифм",
    "FSQT": "Квадратный корень",
    "FITR": "Целая часть",
    "FRAN": "Случайное число",
    "FABS": "Абсолютное значение",
    "FSGN": "Знак числа",
}

DELIMITERS_TABLE = {
    ",": "Запятая",
    ";": "Точка с запятой",
    "(": "Открывающая скобка",
    ")": "Закрывающая скобка",
    "!": "Оператор перевода строки",
}

OPERATORS_TABLE = {
    "+": "Сложение",
    "-": "Вычитание",
    "*": "Умножение",
    "/": "Деление",
    "^": "Возведение в степень",
    "=": "Присваивание",
}

# Динамические таблицы заполняются во время анализа:

IDENTIFIERS_TABLE_EXAMPLE = {
    "COST": {"id": 1, "type": "Переменная с плавающей точкой"},
    "PRICE": {"id": 2, "type": "Переменная с плавающей точкой"},
    "TAX": {"id": 3, "type": "Переменная с плавающей точкой"},
}

CONSTANTS_TABLE_EXAMPLE = {
    "0.98": {"id": 1, "type": "Константа с плавающей точкой"},
    "10.5": {"id": 2, "type": "Константа с плавающей точкой"},
    "20.75": {"id": 3, "type": "Константа с плавающей точкой"},
}

if __name__ == "__main__":
    print("ТАБЛИЦА КЛЮЧЕВЫХ СЛОВ")
    print("─" * 50)
    for k, v in KEYWORDS_TABLE.items():
        print(f"  {k:5} → {v}")
    
    print("\nТАБЛИЦА ФУНКЦИЙ")
    print("─" * 50)
    for k, v in FUNCTIONS_TABLE.items():
        print(f"  {k:10} → {v}")
    
    print("\nТАБЛИЦА РАЗДЕЛИТЕЛЕЙ")
    print("─" * 50)
    for k, v in DELIMITERS_TABLE.items():
        print(f"  '{k:1}' → {v}")
    
    print("\nТАБЛИЦА ОПЕРАТОРОВ")
    print("─" * 50)
    for k, v in OPERATORS_TABLE.items():
        print(f"  '{k:1}' → {v}")
    
    print("\nПримеры динамических таблиц:")
    print("\nТАБЛИЦА ИДЕНТИФИКАТОРОВ")
    print("─" * 50)
    print("  id | имя   | тип")
    for k, v in IDENTIFIERS_TABLE_EXAMPLE.items():
        print(f"  {v['id']:2} | {k:10} | {v['type']}")
    
    print("\nТАБЛИЦА КОНСТАНТ")
    print("─" * 50)
    print("  id | значение | тип")
    for k, v in CONSTANTS_TABLE_EXAMPLE.items():
        print(f"  {v['id']:2} | {k:15} | {v['type']}")
