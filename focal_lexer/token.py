from enum import Enum, auto

class TokenType(Enum):
    # Специальные
    EOF = auto()
    UNKNOWN = auto()    # Ошибка
    
    LINE_NUMBER = auto()
    
    KEYWORD_COMMENT = auto()
    KEYWORD_ASK = auto()
    KEYWORD_TYPE = auto()
    KEYWORD_SET = auto()
    KEYWORD_IF = auto()
    KEYWORD_FOR = auto()
    KEYWORD_DO = auto()
    KEYWORD_RETURN = auto()
    KEYWORD_GO = auto()
    KEYWORD_QUIT = auto()
    KEYWORD_ERASE = auto()
    
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
    
    IDENTIFIER = auto()
    
    # Константы
    NUMBER = auto()
    STRING = auto()
    
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


class Token:
    """Представляет лексему с типом, значением и позицией в исходном коде."""
    def __init__(self, token_type: TokenType, value: str, line: int, column: int, error_string: str = ""):
        self.type = token_type
        self.value = value      # Строковое представление (например, "1.10", "A", "+")
        self.line = line        # Номер строки (начиная с 1)
        self.column = column    # Позиция в строке (начиная с 1)
        self.error_string = error_string

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column}, {self.error_string})"