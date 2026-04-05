from typing import List, Set, Dict, Any
from focal_parser.parser import (
    Program, Line, Statement, CommentStatement, AskStatement, TypeStatement,
    SetStatement, IfStatement, ForStatement, DoStatement, GoStatement,
    ReturnStatement, QuitStatement, EraseStatement, CommandCallStatement,
    PrintItem, AssignmentTarget, VariableTarget, ArrayTarget, Expression,
    NumberLiteral, StringLiteral, Identifier, CallExpression, UnaryOp, BinaryOp
)


class SemanticError(Exception):
    def __init__(self, message: str, line: int):
        self.message = message
        self.line = line
        super().__init__(f"Semantic error at line {line}: {message}")


class SemanticAnalyzer:
    def __init__(self):
        self.line_numbers: Set[str] = set()
        self.errors: List[SemanticError] = []
        self.variables: Set[str] = set()
        self.arrays: Set[str] = set()

    def analyze(self, program: Program) -> List[SemanticError]:
        # First pass: collect line numbers
        for line in program.lines:
            if line.label:
                self.line_numbers.add(line.label)
                key = int(float(line.label))
                self.line_numbers.add(key)

        # Second pass: analyze statements
        for line in program.lines:
            self.analyze_line(line)

        return self.errors

    def analyze_line(self, line: Line):
        for stmt in line.statements:
            self.analyze_statement(stmt, line.line_number)

    def analyze_statement(self, stmt: Statement, line_num: int):
        if isinstance(stmt, (CommentStatement, AskStatement, TypeStatement, ReturnStatement, QuitStatement, EraseStatement)):
            pass  # No semantic checks
        elif isinstance(stmt, SetStatement):
            self.analyze_set(stmt, line_num)
        elif isinstance(stmt, IfStatement):
            self.analyze_if(stmt, line_num)
        elif isinstance(stmt, ForStatement):
            self.analyze_for(stmt, line_num)
        elif isinstance(stmt, DoStatement):
            self.analyze_do(stmt, line_num)
        elif isinstance(stmt, GoStatement):
            self.analyze_go(stmt, line_num)
        elif isinstance(stmt, CommandCallStatement):
            self.analyze_command_call(stmt, line_num)
        else:
            self.errors.append(SemanticError(f"Unknown statement type: {type(stmt)}", line_num))

    def analyze_set(self, stmt: SetStatement, line_num: int):
        # Check target
        if isinstance(stmt.target, VariableTarget):
            self.variables.add(stmt.target.name)
        elif isinstance(stmt.target, ArrayTarget):
            self.arrays.add(stmt.target.name)
            self.analyze_expression(stmt.target.index, line_num)
        # Check expression
        self.analyze_expression(stmt.expression, line_num)

    def analyze_if(self, stmt: IfStatement, line_num: int):
        self.analyze_expression(stmt.condition, line_num)
        self.check_line_exists(stmt.true_line, line_num)
        self.check_line_exists(stmt.false_line, line_num)
        self.check_line_exists(stmt.neither_line, line_num)

    def analyze_for(self, stmt: ForStatement, line_num: int):
        self.variables.add(stmt.variable)
        self.analyze_expression(stmt.start, line_num)
        self.analyze_expression(stmt.step, line_num)
        self.analyze_expression(stmt.limit, line_num)

    def analyze_do(self, stmt: DoStatement, line_num: int):
        self.check_line_exists(stmt.target_line, line_num)

    def analyze_go(self, stmt: GoStatement, line_num: int):
        self.check_line_exists(stmt.target_line, line_num)

    def analyze_command_call(self, stmt: CommandCallStatement, line_num: int):
        # For now, just check arguments
        for arg in stmt.args:
            self.analyze_expression(arg, line_num)

    def analyze_expression(self, expr: Expression, line_num: int):
        if isinstance(expr, (NumberLiteral, StringLiteral)):
            pass
        elif isinstance(expr, Identifier):
            # Assume it's a variable or array without index
            self.variables.add(expr.name)
        elif isinstance(expr, CallExpression):
            self.analyze_call(expr, line_num)
        elif isinstance(expr, UnaryOp):
            self.analyze_expression(expr.operand, line_num)
        elif isinstance(expr, BinaryOp):
            self.analyze_expression(expr.left, line_num)
            self.analyze_expression(expr.right, line_num)
        else:
            self.errors.append(SemanticError(f"Unknown expression type: {type(expr)}", line_num))

    def analyze_call(self, expr: CallExpression, line_num: int):
        name = expr.name.upper()
        arg_count = len(expr.args)
        if name in ['FSIN', 'FCOS', 'FATN', 'FEXP', 'FLOG', 'FSQT', 'FITR', 'FABS', 'FSGN']:
            if arg_count != 1:
                self.errors.append(SemanticError(f"Function {name} requires 1 argument, got {arg_count}", line_num))
        elif name == 'FRAN':
            if arg_count != 1:
                self.errors.append(SemanticError(f"Function FRAN requires 1 argument, got {arg_count}", line_num))
        else:
            # Unknown function, but allow
            pass
        for arg in expr.args:
            self.analyze_expression(arg, line_num)

    def check_line_exists(self, line_label: str, current_line: int):
        if '.' in line_label:
            if line_label not in self.line_numbers:
                self.errors.append(SemanticError(f"Line {line_label} not found", current_line))
        else:
            key = int(float(line_label))
            if key not in self.line_numbers:
                self.errors.append(SemanticError(f"Line {line_label} not found", current_line))


def analyze_program(program: Program) -> List[SemanticError]:
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(program)
