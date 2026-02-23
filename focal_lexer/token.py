from enum import Enum, auto

class TokenType(Enum):
    # Специальные
    EOF = auto()          # Конец файла
    UNKNOWN = auto()      # Неизвестный символ (ошибка)
    
    # Номера строк (например, 1.10)
    LINE_NUMBER = auto()
    
    # Ключевые слова (однобуквенные и многосимвольные)
    KEYWORD_COMMENT = auto()   # C
    KEYWORD_ASK = auto()       # A
    KEYWORD_TYPE = auto()      # T
    KEYWORD_SET = auto()       # S
    KEYWORD_IF = auto()        # I
    KEYWORD_FOR = auto()       # FOR
    KEYWORD_DO = auto()        # DO
    KEYWORD_RETURN = auto()    # RETURN
    KEYWORD_GO = auto()        # G или GO
    KEYWORD_QUIT = auto()      # Q или QUIT
    KEYWORD_ERASE = auto()     # ERASE
    
    # Встроенные функции (можно выделить отдельно или считать идентификаторами)
    FUNCTION_FSIN = auto()
    FUNCTION_FCOS = auto()
    FUNCTION_FATN = auto()
    FUNCTION_FEXP = auto()
    FUNCTION_FLOG = auto()
    FUNCTION_FSQT = auto()
    FUNCTION_FITR = auto()
    FUNCTION_FRAN = auto()
    FUNCTION_FABS = auto()
    FUNCTION_FSGN = auto()
    
    # Идентификаторы (имена переменных)
    IDENTIFIER = auto()
    
    # Константы
    NUMBER = auto()        # Числовая константа (целая или вещественная)
    STRING = auto()        # Текстовая константа в кавычках
    
    # Операторы
    OPERATOR_PLUS = auto()      # +
    OPERATOR_MINUS = auto()     # -
    OPERATOR_MULTIPLY = auto()  # *
    OPERATOR_DIVIDE = auto()    # /
    OPERATOR_POWER = auto()     # ^
    OPERATOR_ASSIGN = auto()    # =
    
    # Разделители
    DELIMITER_COMMA = auto()    # ,
    DELIMITER_SEMICOLON = auto() # ;
    DELIMITER_LPAREN = auto()   # (
    DELIMITER_RPAREN = auto()   # )
    DELIMITER_EXCLAM = auto()   # ! (перевод строки)
    
    # Специальные для IF с тремя метками (сами метки — числа, но разделители уже есть)
    # Тут ничего дополнительно не нужно.

class Token:
    """Представляет лексему с типом, значением и позицией в исходном коде."""
    def __init__(self, token_type: TokenType, value: str, line: int, column: int):
        self.type = token_type
        self.value = value      # Строковое представление (например, "1.10", "A", "+")
        self.line = line        # Номер строки (начиная с 1)
        self.column = column    # Позиция в строке (начиная с 1)

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})"