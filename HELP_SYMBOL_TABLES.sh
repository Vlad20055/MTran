#!/bin/bash
# SCRIPTS FOR SYMBOL TABLES

# Полный список команд для работы с таблицами символов в focal_lexer

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         КОМАНДЫ ДЛЯ РАБОТЫ С ТАБЛИЦАМИ СИМВОЛОВ В focal_lexer     ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📌 ОСНОВНЫЕ КОМАНДЫ:"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "1️⃣  Анализ файла с выводом всех таблиц:"
echo "   python3 focal_lexer/main.py focal/test_symbol_table.foc"
echo ""
echo "2️⃣  Запуск расширенных примеров:"
echo "   python3 focal_lexer/example_usage.py"
echo ""
echo "3️⃣  Просмотр справочника таблиц:"
echo "   python3 focal_lexer/tables_reference.py"
echo ""

echo "📌 ДОКУМЕНТАЦИЯ:"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "📄 Полная документация:"
echo "   focal_lexer/SYMBOL_TABLE_DOC.md"
echo ""
echo "📄 Краткий README:"
echo "   focal_lexer/README_SYMBOL_TABLES.md"
echo ""
echo "📄 Итоговая сводка:"
echo "   SYMBOL_TABLES_SUMMARY.md"
echo ""

echo "📌 ПРИМЕРЫ ФАЙЛОВ:"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "📋 Тестовый файл FOCAL:"
echo "   focal/test_symbol_table.foc"
echo ""

echo "📌 СОЗДАННЫЕ ФАЙЛЫ:"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "✅ focal_lexer/symbol_table.py         - Главный модуль"
echo "✅ focal_lexer/__init__.py             - Обновленный инициализатор"
echo "✅ focal_lexer/main.py                 - Обновленный пример с таблицами"
echo "✅ focal_lexer/example_usage.py        - Расширенные примеры"
echo "✅ focal_lexer/tables_reference.py     - Справочник таблиц"
echo "✅ focal_lexer/SYMBOL_TABLE_DOC.md     - Полная документация"
echo "✅ focal_lexer/README_SYMBOL_TABLES.md - Краткий README"
echo "✅ SYMBOL_TABLES_SUMMARY.md            - Итоговая сводка"
echo ""

echo "📌 API КЛАССА SymbolTable:"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "Методы добавления:"
echo "  - add_identifier(name: str, info: str) -> int"
echo "  - add_constant(value: str, const_type: str) -> int"
echo ""
echo "Методы получения информации:"
echo "  - get_identifier(name: str) -> dict | None"
echo "  - get_constant(value: str) -> dict | None"
echo ""
echo "Методы вывода:"
echo "  - print_keywords_table()      - Таблица ключевых слов"
echo "  - print_functions_table()     - Таблица функций"
echo "  - print_delimiters_table()    - Таблица разделителей"
echo "  - print_operators_table()     - Таблица операторов"
echo "  - print_identifiers_table()   - Таблица идентификаторов"
echo "  - print_constants_table()     - Таблица констант"
echo "  - print_all_tables()          - Все таблицы"
echo ""

echo "📌 БЫСТРЫЙ ПРИМЕР В PYTHON:"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
cat << 'EOF'
from focal_lexer import SymbolTable, LexicalAnalyzer, TokenType

# Создание таблицы символов
symbol_table = SymbolTable()

# Анализ исходного кода
lexer = LexicalAnalyzer("1.10 T 'Hello'! 2.20 S X=5;")
tokens = lexer.tokenize()

# Сбор информации в таблицы
for tok in tokens:
    if tok.type == TokenType.IDENTIFIER:
        symbol_table.add_identifier(tok.value)
    elif tok.type == TokenType.NUMBER:
        symbol_table.add_constant(tok.value)

# Вывод таблиц
symbol_table.print_all_tables()
EOF

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ ВСЕ ТАБЛИЦЫ ГОТОВЫ!                          ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
