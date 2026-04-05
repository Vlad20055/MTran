from dataclasses import dataclass, field
from typing import List, Optional, Any

from focal_lexer.lexer import LexicalAnalyzer
from focal_lexer.token import TokenType, Token


class ParseError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        super().__init__(f"Parse error at line {token.line}, col {token.column}: {message}")


@dataclass
class Program:
    lines: List['Line'] = field(default_factory=list)


@dataclass
class Line:
    label: Optional[str]
    statements: List['Statement']
    line_number: int


class Statement:
    pass


@dataclass
class CommentStatement(Statement):
    text: str


@dataclass
class AskStatement(Statement):
    items: List['PrintItem']


@dataclass
class TypeStatement(Statement):
    items: List['PrintItem']


@dataclass
class SetStatement(Statement):
    target: 'AssignmentTarget'
    expression: 'Expression'


@dataclass
class IfStatement(Statement):
    condition: 'Expression'
    true_line: str
    false_line: str
    neither_line: str


@dataclass
class ForStatement(Statement):
    variable: str
    start: 'Expression'
    step: 'Expression'
    limit: 'Expression'


@dataclass
class DoStatement(Statement):
    target_line: str


@dataclass
class GoStatement(Statement):
    target_line: str


@dataclass
class ReturnStatement(Statement):
    pass


@dataclass
class QuitStatement(Statement):
    pass


@dataclass
class EraseStatement(Statement):
    pass


@dataclass
class CommandCallStatement(Statement):
    name: str
    args: List['Expression']


@dataclass
class PrintItem:
    value: Optional['Expression']
    newline: bool = False


class AssignmentTarget:
    pass


@dataclass
class VariableTarget(AssignmentTarget):
    name: str


@dataclass
class ArrayTarget(AssignmentTarget):
    name: str
    index: 'Expression'


class Expression:
    pass


@dataclass
class NumberLiteral(Expression):
    value: str


@dataclass
class StringLiteral(Expression):
    value: str


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class CallExpression(Expression):
    name: str
    args: List[Expression]


@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression


@dataclass
class BinaryOp(Expression):
    operator: str
    left: Expression
    right: Expression


class Parser:
    def __init__(self, source: str):
        lexer = LexicalAnalyzer(source)
        self.tokens = lexer.tokenize()
        self.pos = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.current
        if self.current.type != TokenType.EOF:
            self.pos += 1
        return tok

    def expect(self, *types: TokenType) -> Token:
        if self.current.type in types:
            return self.advance()
        raise ParseError(self.current, f"Expected {', '.join(t.name for t in types)}, got {self.current.type.name}")

    def match(self, *types: TokenType) -> bool:
        if self.current.type in types:
            self.advance()
            return True
        return False

    def parse(self) -> Program:
        program = Program()
        while self.current.type != TokenType.EOF:
            if self.current.type == TokenType.EOF:
                break
            program.lines.append(self.parse_line())
        return program

    def parse_line(self) -> Line:
        label = None
        start_line = self.current.line
        if self.current.type == TokenType.NUMBER and self.current.column == 1:
            label = self.current.value
            self.advance()
        statements = self.parse_statement_list(start_line)
        return Line(label, statements, start_line)

    def parse_statement_list(self, line_number: int) -> List[Statement]:
        statements: List[Statement] = []
        while self.current.type != TokenType.EOF and self.current.line == line_number:
            if self.current.type == TokenType.DELIMITER_SEMICOLON:
                self.advance()
                continue
            statements.append(self.parse_statement(line_number))
            if self.current.type == TokenType.DELIMITER_SEMICOLON:
                self.advance()
                continue
            break
        return statements

    def parse_statement(self, line_number: int) -> Statement:
        t = self.current.type
        if t == TokenType.KEYWORD_COMMENT:
            return self.parse_comment(line_number)
        if t == TokenType.KEYWORD_ASK:
            self.advance()
            return AskStatement(self.parse_print_items(line_number))
        if t == TokenType.KEYWORD_TYPE:
            self.advance()
            return TypeStatement(self.parse_print_items(line_number))
        if t == TokenType.KEYWORD_SET:
            self.advance()
            return self.parse_set()
        if t == TokenType.KEYWORD_IF:
            self.advance()
            return self.parse_if()
        if t == TokenType.KEYWORD_FOR:
            self.advance()
            return self.parse_for()
        if t == TokenType.KEYWORD_DO:
            self.advance()
            return DoStatement(self.parse_line_number())
        if t == TokenType.KEYWORD_GO:
            self.advance()
            return GoStatement(self.parse_line_number())
        if t == TokenType.KEYWORD_RETURN:
            self.advance()
            return ReturnStatement()
        if t == TokenType.KEYWORD_QUIT:
            self.advance()
            return QuitStatement()
        if t == TokenType.KEYWORD_ERASE:
            self.advance()
            return EraseStatement()
        if t == TokenType.IDENTIFIER or self.is_function_token(t):
            return self.parse_command_call(line_number)
        raise ParseError(self.current, f"Unexpected token {self.current.type.name}")

    def parse_comment(self, line_number: int) -> CommentStatement:
        self.advance()
        parts = []
        while self.current.type != TokenType.EOF and self.current.line == line_number and self.current.type != TokenType.DELIMITER_SEMICOLON:
            parts.append(self.current.value)
            self.advance()
        return CommentStatement(' '.join(parts).strip())

    def parse_print_items(self, line_number: int) -> List[PrintItem]:
        items: List[PrintItem] = []
        while self.current.type != TokenType.EOF and self.current.line == line_number:
            if self.current.type == TokenType.DELIMITER_EXCLAM:
                self.advance()
                items.append(PrintItem(value=None, newline=True))
            else:
                items.append(PrintItem(value=self.parse_expression()))
            if self.current.type == TokenType.DELIMITER_COMMA:
                self.advance()
                continue
            if self.current.type == TokenType.DELIMITER_EXCLAM:
                continue
            break
        return items

    def parse_set(self) -> SetStatement:
        target = self.parse_assignment_target()
        self.expect(TokenType.OPERATOR_ASSIGN)
        expr = self.parse_expression()
        return SetStatement(target, expr)

    def parse_assignment_target(self) -> AssignmentTarget:
        if self.current.type != TokenType.IDENTIFIER:
            raise ParseError(self.current, 'Expected variable name or array reference')
        name = self.current.value
        self.advance()
        if self.match(TokenType.DELIMITER_LPAREN):
            index = self.parse_expression()
            self.expect(TokenType.DELIMITER_RPAREN)
            return ArrayTarget(name, index)
        return VariableTarget(name)

    def parse_if(self) -> IfStatement:
        self.expect(TokenType.DELIMITER_LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.DELIMITER_RPAREN)
        true_line = self.parse_line_number()
        self.expect(TokenType.DELIMITER_COMMA)
        false_line = self.parse_line_number()
        self.expect(TokenType.DELIMITER_COMMA)
        neither_line = self.parse_line_number()
        return IfStatement(condition, true_line, false_line, neither_line)

    def parse_for(self) -> ForStatement:
        if self.current.type != TokenType.IDENTIFIER:
            raise ParseError(self.current, 'Expected loop variable')
        variable = self.current.value
        self.advance()
        self.expect(TokenType.OPERATOR_ASSIGN)
        start = self.parse_expression()
        self.expect(TokenType.DELIMITER_COMMA)
        step = self.parse_expression()
        self.expect(TokenType.DELIMITER_COMMA)
        limit = self.parse_expression()
        return ForStatement(variable, start, step, limit)

    def parse_command_call(self, line_number: int) -> CommandCallStatement:
        name = self.current.value
        self.advance()
        args: List[Expression] = []
        if self.match(TokenType.DELIMITER_LPAREN):
            if self.current.type != TokenType.DELIMITER_RPAREN:
                args.append(self.parse_expression())
                while self.match(TokenType.DELIMITER_COMMA):
                    args.append(self.parse_expression())
            self.expect(TokenType.DELIMITER_RPAREN)
        while self.current.type != TokenType.EOF and self.current.line == line_number and self.current.type != TokenType.DELIMITER_SEMICOLON:
            if self.current.type == TokenType.DELIMITER_COMMA:
                self.advance()
                continue
            args.append(self.parse_expression())
        return CommandCallStatement(name, args)

    def parse_line_number(self) -> str:
        if self.current.type != TokenType.NUMBER:
            raise ParseError(self.current, 'Expected line number')
        value = self.current.value
        self.advance()
        return value

    def parse_expression(self) -> Expression:
        return self.parse_additive()

    def parse_additive(self) -> Expression:
        node = self.parse_multiplicative()
        while self.current.type in (TokenType.OPERATOR_PLUS, TokenType.OPERATOR_MINUS):
            operator = self.current.value
            self.advance()
            right = self.parse_multiplicative()
            node = BinaryOp(operator, node, right)
        return node

    def parse_multiplicative(self) -> Expression:
        node = self.parse_power()
        while self.current.type in (TokenType.OPERATOR_MULTIPLY, TokenType.OPERATOR_DIVIDE):
            operator = self.current.value
            self.advance()
            right = self.parse_power()
            node = BinaryOp(operator, node, right)
        return node

    def parse_power(self) -> Expression:
        node = self.parse_unary()
        if self.current.type == TokenType.OPERATOR_POWER:
            operator = self.current.value
            self.advance()
            right = self.parse_power()
            node = BinaryOp(operator, node, right)
        return node

    def parse_unary(self) -> Expression:
        if self.current.type == TokenType.OPERATOR_PLUS:
            self.advance()
            return UnaryOp('+', self.parse_unary())
        if self.current.type == TokenType.OPERATOR_MINUS:
            self.advance()
            return UnaryOp('-', self.parse_unary())
        return self.parse_primary()

    def parse_primary(self) -> Expression:
        if self.current.type == TokenType.NUMBER:
            value = self.current.value
            self.advance()
            return NumberLiteral(value)
        if self.current.type == TokenType.STRING:
            value = self.current.value
            self.advance()
            return StringLiteral(value)
        if self.current.type == TokenType.DELIMITER_LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.DELIMITER_RPAREN)
            return expr
        if self.current.type == TokenType.IDENTIFIER or self.is_function_token(self.current.type):
            name = self.current.value
            self.advance()
            if self.match(TokenType.DELIMITER_LPAREN):
                args: List[Expression] = []
                if self.current.type != TokenType.DELIMITER_RPAREN:
                    args.append(self.parse_expression())
                    while self.match(TokenType.DELIMITER_COMMA):
                        args.append(self.parse_expression())
                self.expect(TokenType.DELIMITER_RPAREN)
                return CallExpression(name, args)
            return Identifier(name)
        raise ParseError(self.current, f"Unexpected expression token {self.current.type.name}")

    def is_function_token(self, token_type: TokenType) -> bool:
        return token_type in {
            TokenType.FUNCTION_FSIN,
            TokenType.FUNCTION_FCOS,
            TokenType.FUNCTION_FATN,
            TokenType.FUNCTION_FEXP,
            TokenType.FUNCTION_FLOG,
            TokenType.FUNCTION_FSQT,
            TokenType.FUNCTION_FITR,
            TokenType.FUNCTION_FRAN,
            TokenType.FUNCTION_FABS,
            TokenType.FUNCTION_FSGN,
        }


def dump_ast(node: Any, indent: int = 0) -> str:
    prefix = '  ' * indent
    if node is None:
        return prefix + 'None\n'
    if isinstance(node, list):
        if not node:
            return prefix + '[]\n'
        text = prefix + '[\n'
        for item in node:
            text += dump_ast(item, indent + 1)
        text += prefix + ']\n'
        return text
    if isinstance(node, (str, int, float)):
        return prefix + repr(node) + '\n'
    if isinstance(node, PrintItem):
        if node.newline:
            return prefix + 'PrintItem(newline=True)\n'
        return prefix + 'PrintItem(value=\n' + dump_ast(node.value, indent + 2) + prefix + ')\n'
    if isinstance(node, Token):
        return prefix + f'Token({node.type.name},{node.value})\n'
    if hasattr(node, '__dataclass_fields__'):
        parts = []
        text = prefix + f"{node.__class__.__name__}(\n"
        for field_name in node.__dataclass_fields__:
            value = getattr(node, field_name)
            text += prefix + '  ' + field_name + '=\n' + dump_ast(value, indent + 2)
        text += prefix + ')\n'
        return text
    return prefix + repr(node) + '\n'


def parse_source(source: str) -> Program:
    parser = Parser(source)
    return parser.parse()
