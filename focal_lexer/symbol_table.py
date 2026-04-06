"""
Модуль для управления таблицами имён в лексическом анализаторе.
Включает таблицы для ключевых слов, разделителей, операторов, функций,
идентификаторов и констант.
"""


class SymbolTable:
    """Управляет всеми таблицами символов лексера"""
    
    def __init__(self):
        # Таблица ключевых слов
        self.keywords = {
            'C': {'name': 'COMMENT', 'type': 'Ключевое слово'},
            'A': {'name': 'ASK', 'type': 'Ключевое слово'},
            'T': {'name': 'TYPE', 'type': 'Ключевое слово'},
            'S': {'name': 'SET', 'type': 'Ключевое слово'},
            'I': {'name': 'IF', 'type': 'Ключевое слово'},
            'F': {'name': 'FOR', 'type': 'Ключевое слово'},
            'D': {'name': 'DO', 'type': 'Ключевое слово'},
            'R': {'name': 'RETURN', 'type': 'Ключевое слово'},
            'G': {'name': 'GO', 'type': 'Ключевое слово'},
            'Q': {'name': 'QUIT', 'type': 'Ключевое слово'},
            'E': {'name': 'ERASE', 'type': 'Ключевое слово'},
        }
        
        # Таблица функций
        self.functions = {
            'FSIN': {'name': 'FSIN', 'type': 'Функция', 'description': 'Синус'},
            'FCOS': {'name': 'FCOS', 'type': 'Функция', 'description': 'Косинус'},
            'FATN': {'name': 'FATN', 'type': 'Функция', 'description': 'Арктангенс'},
            'FEXP': {'name': 'FEXP', 'type': 'Функция', 'description': 'Экспонента'},
            'FLOG': {'name': 'FLOG', 'type': 'Функция', 'description': 'Логарифм'},
            'FSQT': {'name': 'FSQT', 'type': 'Функция', 'description': 'Квадратный корень'},
            'FITR': {'name': 'FITR', 'type': 'Функция', 'description': 'Целая часть'},
            'FRAN': {'name': 'FRAN', 'type': 'Функция', 'description': 'Случайное число'},
            'FABS': {'name': 'FABS', 'type': 'Функция', 'description': 'Абсолютное значение'},
            'FSGN': {'name': 'FSGN', 'type': 'Функция', 'description': 'Знак числа'},
        }
        
        # Таблица разделителей
        self.delimiters = {
            ',': {'symbol': ',', 'type': 'Разделитель', 'name': 'COMMA'},
            ';': {'symbol': ';', 'type': 'Разделитель', 'name': 'SEMICOLON'},
            '(': {'symbol': '(', 'type': 'Разделитель', 'name': 'LPAREN'},
            ')': {'symbol': ')', 'type': 'Разделитель', 'name': 'RPAREN'},
            '!': {'symbol': '!', 'type': 'Разделитель', 'name': 'EXCLAM', 'description': 'Оператор перевода строки'},
        }
        
        # Таблица операторов (математических и логических)
        self.operators = {
            '+': {'symbol': '+', 'type': 'Оператор', 'name': 'PLUS', 'operation': 'Сложение'},
            '-': {'symbol': '-', 'type': 'Оператор', 'name': 'MINUS', 'operation': 'Вычитание'},
            '*': {'symbol': '*', 'type': 'Оператор', 'name': 'MULTIPLY', 'operation': 'Умножение'},
            '/': {'symbol': '/', 'type': 'Оператор', 'name': 'DIVIDE', 'operation': 'Деление'},
            '^': {'symbol': '^', 'type': 'Оператор', 'name': 'POWER', 'operation': 'Возведение в степень'},
            '=': {'symbol': '=', 'type': 'Оператор', 'name': 'ASSIGN', 'operation': 'Присваивание'},
        }
        
        # Таблица идентификаторов (заполняется динамически)
        self.identifiers = {}
        self._identifier_counter = 0
        
        # Таблица констант (заполняется динамически)
        self.constants = {}
        self._constant_counter = 0
    
    def add_identifier(self, name: str, info: str = "Переменная") -> int:
        """
        Добавляет идентификатор в таблицу.
        Возвращает номер элемента.
        """
        if name not in self.identifiers:
            self._identifier_counter += 1
            self.identifiers[name] = {
                'id': self._identifier_counter,
                'name': name,
                'info': info,
            }
        return self.identifiers[name]['id']
    
    def add_constant(self, value: str, const_type: str = "Константа с плавающей точкой") -> int:
        """
        Добавляет константу в таблицу.
        Возвращает номер элемента.
        """
        if value not in self.constants:
            self._constant_counter += 1
            self.constants[value] = {
                'id': self._constant_counter,
                'value': value,
                'type': const_type,
            }
        return self.constants[value]['id']
    
    def get_identifier(self, name: str):
        """Получает информацию об идентификаторе"""
        return self.identifiers.get(name)
    
    def get_constant(self, value: str):
        """Получает информацию о константе"""
        return self.constants.get(value)
    
    def print_keywords_table(self):
        """Выводит таблицу ключевых слов"""
        print("\n╔═══════════════════════════════════════════════════════════╗")
        print("║              ТАБЛИЦА КЛЮЧЕВЫХ СЛОВ                        ║")
        print("╠═══════════════════════════════════════════════════════════╣")
        print(f"║ {'№':<3} │ {'Ключевое слово':<20} │ {'Тип':<30} ║")
        print("╠═══════════════════════════════════════════════════════════╣")
        for idx, (key, value) in enumerate(self.keywords.items(), 1):
            print(f"║ {idx:<3} │ {key:<20} │ {value['type']:<30} ║")
        print("╚═══════════════════════════════════════════════════════════╝")
    
    def print_functions_table(self):
        """Выводит таблицу функций"""
        print("\n╔════════════════════════════════════════════════════════════════════╗")
        print("║                    ТАБЛИЦА ФУНКЦИЙ                                ║")
        print("╠════════════════════════════════════════════════════════════════════╣")
        print(f"║ {'№':<3} │ {'Функция':<10} │ {'Тип':<12} │ {'Описание':<30} ║")
        print("╠════════════════════════════════════════════════════════════════════╣")
        for idx, (key, value) in enumerate(self.functions.items(), 1):
            desc = value.get('description', '-')
            print(f"║ {idx:<3} │ {key:<10} │ {value['type']:<12} │ {desc:<30} ║")
        print("╚════════════════════════════════════════════════════════════════════╝")
    
    def print_delimiters_table(self):
        """Выводит таблицу разделителей"""
        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║               ТАБЛИЦА РАЗДЕЛИТЕЛЕЙ                           ║")
        print("╠═══════════════════════════════════════════════════════════════╣")
        print(f"║ {'№':<3} │ {'Символ':<5} │ {'Тип':<20} │ {'Описание':<25} ║")
        print("╠═══════════════════════════════════════════════════════════════╣")
        for idx, (key, value) in enumerate(self.delimiters.items(), 1):
            desc = value.get('description', '-')
            print(f"║ {idx:<3} │ {key:<5} │ {value['type']:<20} │ {desc:<25} ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
    
    def print_operators_table(self):
        """Выводит таблицу операторов"""
        print("\n╔═══════════════════════════════════════════════════════════════════════╗")
        print("║              ТАБЛИЦА МАТЕМАТИЧЕСКИХ И ЛОГИЧЕСКИХ ОПЕРАТОРОВ          ║")
        print("╠═══════════════════════════════════════════════════════════════════════╣")
        print(f"║ {'№':<3} │ {'Оператор':<5} │ {'Название':<15} │ {'Операция':<30} ║")
        print("╠═══════════════════════════════════════════════════════════════════════╣")
        for idx, (key, value) in enumerate(self.operators.items(), 1):
            op_name = value.get('name', '-')
            operation = value.get('operation', '-')
            print(f"║ {idx:<3} │ {key:<5} │ {op_name:<15} │ {operation:<30} ║")
        print("╚═══════════════════════════════════════════════════════════════════════╝")
    
    def print_identifiers_table(self):
        """Выводит таблицу идентификаторов"""
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║              ТАБЛИЦА ИДЕНТИФИКАТОРОВ                         ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print(f"║ {'№':<3} │ {'Идентификатор':<20} │ {'Информация':<25} ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        
        if not self.identifiers:
            print("║ Таблица пуста - идентификаторы еще не добавлены               ║")
        else:
            for key, value in sorted(self.identifiers.items(), key=lambda x: x[1]['id']):
                print(f"║ {value['id']:<3} │ {value['name']:<20} │ {value['info']:<25} ║")
        
        print("╚══════════════════════════════════════════════════════════════╝")
    
    def print_constants_table(self):
        """Выводит таблицу констант"""
        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║               ТАБЛИЦА КОНСТАНТ                               ║")
        print("╠═══════════════════════════════════════════════════════════════╣")
        print(f"║ {'№':<3} │ {'Значение':<20} │ {'Тип константы':<30} ║")
        print("╠═══════════════════════════════════════════════════════════════╣")
        
        if not self.constants:
            print("║ Таблица пуста - константы еще не добавлены                  ║")
        else:
            for key, value in sorted(self.constants.items(), key=lambda x: x[1]['id']):
                print(f"║ {value['id']:<3} │ {value['value']:<20} │ {value['type']:<30} ║")
        
        print("╚═══════════════════════════════════════════════════════════════╝")
    
    def print_all_tables(self):
        """Выводит все таблицы символов"""
        self.print_keywords_table()
        self.print_functions_table()
        self.print_delimiters_table()
        self.print_operators_table()
        self.print_identifiers_table()
        self.print_constants_table()
