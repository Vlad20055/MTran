from .token import Token, TokenType

class LexicalAnalyzer:
    def __init__(self, source: str):
        self.source = source                # Исходный код как строка
        self.pos = 0                        # Текущая позиция в строке
        self.line = 1                       # Текущая строка
        self.column = 1                     # Текущая колонка
        self.tokens = []                    # Список собранных токенов (может не хранить, если сразу выдавать)
        self.start_of_line = True           # Начало строки (после \n или начала файла)
        self.expect_command = False         # Ожидается ли команда?

    def peek(self) -> str:
        """
        Completed
        Возвращает текущий символ без продвижения вперёд, или '' если конец.
        """
        if self.pos >= len(self.source):
            return ''
        return self.source[self.pos]

    def advance(self) -> str:
        """
        Completed
        Возвращает текущий символ и продвигается на один символ вперёд.
        """
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
            self.start_of_line = True
        else:
            self.column += 1
        return ch

    def skip_whitespace(self):
        """
        Completed
        Пропускает пробелы, табуляции, но не переводы строк (они важны для !).
        """
        while self.pos < len(self.source) and self.peek() in ' \t\r':
            self.advance()

    def next_token(self) -> Token:
        """Сканирует один токен и возвращает результат."""
        # Пропускаем пробелы и обрабатываем переводы строк
        while True:
            self.skip_whitespace()
            if self.pos >= len(self.source):
                return Token(TokenType.EOF, '', self.line, self.column)
            if self.peek() == '\n':
                self.advance()  # переводим строку, start_of_line станет True
                continue
            break

        start_line = self.line
        start_col = self.column
        ch = self.peek()
        at_start = self.start_of_line
        self.start_of_line = False  # текущий токен займёт начало, сбрасываем

        # Сохраняем состояние ожидания команды (оно могло быть от предыдущего токена)
        expect_cmd = self.expect_command

        # Число
        if ch.isdigit() or (ch == '.' and len(self.source) > self.pos+1 and self.source[self.pos+1].isdigit()):
            tok = self.read_number(start_line, start_col)
            # Если число стояло в начале строки — это номер строки, после него ожидаем команду
            if at_start:
                self.expect_command = True
            else:
                self.expect_command = False
            return tok

        # Строка в кавычках
        if ch == '"' or ch == '\'':
            tok = self.read_string(start_line, start_col)
            self.expect_command = False
            return tok

        # Идентификатор (буква)
        if ch.isalpha():
            tok = self.read_identifier(start_line, start_col, expect_cmd)
            self.expect_command = False
            return tok

        # Операторы и разделители
        if ch == '+':
            self.advance()
            self.expect_command = False
            return Token(TokenType.OPERATOR_PLUS, '+', start_line, start_col)
        if ch == '-':
            self.advance()
            self.expect_command = False
            return Token(TokenType.OPERATOR_MINUS, '-', start_line, start_col)
        if ch == '*':
            self.advance()
            self.expect_command = False
            return Token(TokenType.OPERATOR_MULTIPLY, '*', start_line, start_col)
        if ch == '/':
            self.advance()
            self.expect_command = False
            return Token(TokenType.OPERATOR_DIVIDE, '/', start_line, start_col)
        if ch == '^':
            self.advance()
            self.expect_command = False
            return Token(TokenType.OPERATOR_POWER, '^', start_line, start_col)
        if ch == '=':
            self.advance()
            self.expect_command = False
            return Token(TokenType.OPERATOR_ASSIGN, '=', start_line, start_col)
        if ch == ',':
            self.advance()
            self.expect_command = False
            return Token(TokenType.DELIMITER_COMMA, ',', start_line, start_col)
        if ch == ';':
            self.advance()
            self.expect_command = True   # после точки с запятой ожидаем команду
            return Token(TokenType.DELIMITER_SEMICOLON, ';', start_line, start_col)
        if ch == '(':
            self.advance()
            self.expect_command = False
            return Token(TokenType.DELIMITER_LPAREN, '(', start_line, start_col)
        if ch == ')':
            self.advance()
            self.expect_command = False
            return Token(TokenType.DELIMITER_RPAREN, ')', start_line, start_col)
        if ch == '!':
            self.advance()
            self.expect_command = False
            return Token(TokenType.DELIMITER_EXCLAM, '!', start_line, start_col)

        # Неизвестный символ
        self.advance()
        self.expect_command = False
        return Token(TokenType.UNKNOWN, ch, start_line, start_col)

    def read_number(self, line: int, col: int) -> Token:
        """
        Completed
        Читает число (может быть как метка строки, так и константа)
        """
        num_str = ''
        dot_count = 0
        while self.pos < len(self.source):
            ch = self.peek()
            if ch.isdigit():
                num_str += self.advance()
            elif ch == '.':
                dot_count += 1
                if dot_count > 1:
                    num_str += self.advance()
                    while self.pos < len(self.source) and (self.peek().isdigit() or self.peek() == '.'):
                        num_str += self.advance()
                    break
                else:
                    num_str += self.advance()
            else:
                break
        if dot_count > 1:
            return Token(TokenType.UNKNOWN, num_str, line, col)
        return Token(TokenType.NUMBER, num_str, line, col)

    def read_string(self, line: int, col: int) -> Token:
        """
        Completed
        Читает строковую константу, заключенную в кавычки (одинарные или двойные).
        """
        quote_char = self.advance()
        value = ''
        while self.pos < len(self.source) and self.peek() != quote_char:
            value += self.advance()
        if self.pos < len(self.source):
            self.advance()  # закрывающая кавычка
            return Token(TokenType.STRING, value, line, col)
        else:
            # Ошибка: незакрытая строка
            return Token(TokenType.UNKNOWN, value, line, col)
    

    def read_identifier(self, line: int, col: int, expect_cmd: bool) -> Token:
        ident = ''
        while self.pos < len(self.source) and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        ident_up = ident.upper()

        if expect_cmd:
            cmd_type = self._get_command_type(ident_up)
            if cmd_type != TokenType.IDENTIFIER:
                return Token(cmd_type, ident, line, col)
            # Если не команда, то это идентификатор (синтаксическая ошибка, но лексер пропускает)
            return Token(TokenType.IDENTIFIER, ident, line, col)
        else:
            # Проверяем, не функция ли это
            func_type = self._get_function_type(ident_up)
            if func_type != TokenType.IDENTIFIER:
                return Token(func_type, ident, line, col)
            return Token(TokenType.IDENTIFIER, ident, line, col)
        
    def _get_command_type(self, ident_up: str) -> TokenType:
        """Возвращает тип команды по первой букве"""
        # Однобуквенные команды (по первому символу)
        first = ident_up[0] if ident_up else ''
        command_map = {
            'C': TokenType.KEYWORD_COMMENT,
            'A': TokenType.KEYWORD_ASK,
            'T': TokenType.KEYWORD_TYPE,
            'S': TokenType.KEYWORD_SET,
            'I': TokenType.KEYWORD_IF,
            'F': TokenType.KEYWORD_FOR,
            'G': TokenType.KEYWORD_GO,
            'R': TokenType.KEYWORD_RETURN,
            'Q': TokenType.KEYWORD_QUIT,
            'D': TokenType.KEYWORD_DO,
            'E': TokenType.KEYWORD_ERASE,
        }
        return command_map.get(first, TokenType.IDENTIFIER)

    def _get_function_type(self, ident_up: str) -> TokenType:
        functions = {
            'FSIN': TokenType.FUNCTION_FSIN,
            'FCOS': TokenType.FUNCTION_FCOS,
            'FATN': TokenType.FUNCTION_FATN,
            'FEXP': TokenType.FUNCTION_FEXP,
            'FLOG': TokenType.FUNCTION_FLOG,
            'FSQT': TokenType.FUNCTION_FSQT,
            'FITR': TokenType.FUNCTION_FITR,
            'FRAN': TokenType.FUNCTION_FRAN,
            'FABS': TokenType.FUNCTION_FABS,
            'FSGN': TokenType.FUNCTION_FSGN,
        }
        return functions.get(ident_up, TokenType.IDENTIFIER)

    def tokenize(self):
        """Сканирует весь исходный код и возвращает список токенов."""
        tokens = []
        while True:
            tok = self.next_token()
            tokens.append(tok)
            if tok.type == TokenType.EOF:
                break
        return tokens