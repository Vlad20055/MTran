import math
import random
from typing import Dict, List, Any
from focal_parser.parser import (
    Program, Line, Statement, CommentStatement, AskStatement, TypeStatement,
    SetStatement, IfStatement, ForStatement, DoStatement, GoStatement,
    ReturnStatement, QuitStatement, EraseStatement, CommandCallStatement,
    PrintItem, AssignmentTarget, VariableTarget, ArrayTarget, Expression,
    NumberLiteral, StringLiteral, Identifier, CallExpression, UnaryOp, BinaryOp
)


class RuntimeError(Exception):
    pass


class Interpreter:
    def __init__(self, program: Program):
        self.program = program
        self.variables: Dict[str, float] = {}
        self.arrays: Dict[str, Dict[int, float]] = {}
        self.line_map: Dict[str, int] = {}
        self.pc: int = 0
        self.quit = False
        self.return_flag = False
        self.skip_next_pc_increment = False

    def run(self):
        self.build_line_map()
        while not self.quit and 0 <= self.pc < len(self.program.lines):
            line = self.program.lines[self.pc]
            self.execute_line(line)
            if not self.return_flag:
                if self.skip_next_pc_increment:
                    self.skip_next_pc_increment = False
                else:
                    self.pc += 1
            self.return_flag = False

    def build_line_map(self):
        for i, line in enumerate(self.program.lines):
            if line.label:
                self.line_map[line.label] = i
                key = int(float(line.label))
                if key not in self.line_map:
                    self.line_map[key] = i

    def execute_line(self, line: Line):
        i = 0
        while i < len(line.statements):
            stmt = line.statements[i]
            if isinstance(stmt, ForStatement) and i + 1 < len(line.statements):
                # FOR with following statements as loop body
                for_stmt = stmt
                var = for_stmt.variable
                start = self.evaluate_expression(for_stmt.start)
                step = self.evaluate_expression(for_stmt.step)
                limit = self.evaluate_expression(for_stmt.limit)
                current = start
                while (step > 0 and current <= limit) or (step < 0 and current >= limit):
                    self.variables[var.upper()] = current
                    # Execute from i+1 to end
                    for j in range(i + 1, len(line.statements)):
                        self.execute_statement(line.statements[j])
                        if self.quit or self.return_flag or self.skip_next_pc_increment:
                            return
                    current += step
                i = len(line.statements)  # skip remaining
            else:
                self.execute_statement(stmt)
                if self.quit or self.return_flag or self.skip_next_pc_increment:
                    break
                i += 1

    def execute_statement(self, stmt: Statement):
        if isinstance(stmt, CommentStatement):
            pass
        elif isinstance(stmt, AskStatement):
            self.execute_ask(stmt)
        elif isinstance(stmt, TypeStatement):
            self.execute_type(stmt)
        elif isinstance(stmt, SetStatement):
            self.execute_set(stmt)
        elif isinstance(stmt, IfStatement):
            self.execute_if(stmt)
        elif isinstance(stmt, ForStatement):
            self.execute_for(stmt)
        elif isinstance(stmt, DoStatement):
            self.execute_do(stmt)
        elif isinstance(stmt, GoStatement):
            self.execute_go(stmt)
        elif isinstance(stmt, ReturnStatement):
            self.return_flag = True
        elif isinstance(stmt, QuitStatement):
            self.quit = True
        elif isinstance(stmt, EraseStatement):
            self.variables.clear()
            self.arrays.clear()
        elif isinstance(stmt, CommandCallStatement):
            self.execute_command_call(stmt)
        else:
            raise RuntimeError(f"Unknown statement: {type(stmt)}")

    def execute_ask(self, stmt: AskStatement):
        for item in stmt.items:
            if isinstance(item.value, StringLiteral):
                print(item.value.value, end='', flush=True)
            elif isinstance(item.value, Identifier):
                var = item.value.name.upper()
                try:
                    val = float(input())
                except ValueError:
                    val = 0.0
                except EOFError:
                    self.quit = True
                    return
                self.variables[var] = val

    def execute_type(self, stmt: TypeStatement):
        for item in stmt.items:
            if item.newline:
                print(flush=True)
            elif item.value:
                val = self.evaluate_expression(item.value)
                if isinstance(val, str):
                    print(val, end='', flush=True)
                elif isinstance(val, float) and val == int(val):
                    print(int(val), end='', flush=True)
                else:
                    print(val, end='', flush=True)

    def execute_set(self, stmt: SetStatement):
        val = self.evaluate_expression(stmt.expression)
        if isinstance(stmt.target, VariableTarget):
            self.variables[stmt.target.name.upper()] = val
        elif isinstance(stmt.target, ArrayTarget):
            index = int(self.evaluate_expression(stmt.target.index))
            name = stmt.target.name.upper()
            if name not in self.arrays:
                self.arrays[name] = {}
            self.arrays[name][index] = val

    def execute_if(self, stmt: IfStatement):
        cond = self.evaluate_expression(stmt.condition)
        if cond < 0:
            target_line = stmt.true_line
        elif cond == 0:
            target_line = stmt.false_line
        else:
            target_line = stmt.neither_line
        if '.' in target_line:
            target = self.line_map.get(target_line)
        else:
            key = int(float(target_line))
            target = self.line_map.get(key)
        if target is not None:
            self.pc = target
            self.skip_next_pc_increment = True

    def execute_for(self, stmt: ForStatement):
        # Simple implementation: just set the variable to start
        start = self.evaluate_expression(stmt.start)
        self.variables[stmt.variable] = start
        # In FOCAL, FOR is for subsequent statements, but for simplicity, ignore loop

    def execute_do(self, stmt: DoStatement):
        target_line = stmt.target_line
        if '.' in target_line:
            target = self.line_map.get(target_line)
        else:
            key = int(float(target_line))
            target = self.line_map.get(key)
        if target is not None:
            old_pc = self.pc
            self.pc = target
            # Execute until RETURN
            while not self.quit and not self.return_flag and self.pc < len(self.program.lines):
                line = self.program.lines[self.pc]
                self.execute_line(line)
                if self.return_flag:
                    break
                if self.skip_next_pc_increment:
                    self.skip_next_pc_increment = False
                else:
                    self.pc += 1
            self.pc = old_pc
            self.return_flag = False

    def execute_go(self, stmt: GoStatement):
        target_line = stmt.target_line
        if '.' in target_line:
            target = self.line_map.get(target_line)
        else:
            key = int(float(target_line))
            target = self.line_map.get(key)
        if target is not None:
            self.pc = target
            self.skip_next_pc_increment = True

    def execute_command_call(self, stmt: CommandCallStatement):
        # Custom commands, do nothing
        pass

    def evaluate_expression(self, expr: Expression) -> float:
        if isinstance(expr, NumberLiteral):
            return float(expr.value)
        elif isinstance(expr, StringLiteral):
            return expr.value  # but should be float, but for TYPE ok
        elif isinstance(expr, Identifier):
            return self.variables.get(expr.name.upper(), 0.0)
        elif isinstance(expr, CallExpression):
            return self.evaluate_call(expr)
        elif isinstance(expr, UnaryOp):
            val = self.evaluate_expression(expr.operand)
            if expr.operator == '+':
                return val
            elif expr.operator == '-':
                return -val
        elif isinstance(expr, BinaryOp):
            left = self.evaluate_expression(expr.left)
            right = self.evaluate_expression(expr.right)
            if expr.operator == '+':
                return left + right
            elif expr.operator == '-':
                return left - right
            elif expr.operator == '*':
                return left * right
            elif expr.operator == '/':
                return left / right if right != 0 else 0
            elif expr.operator == '^':
                return left ** right
        raise RuntimeError(f"Unknown expression: {type(expr)}")

    def evaluate_call(self, expr: CallExpression) -> float:
        name = expr.name.upper()
        args = [self.evaluate_expression(arg) for arg in expr.args]
        if name == 'FSIN':
            return math.sin(args[0])
        elif name == 'FCOS':
            return math.cos(args[0])
        elif name == 'FATN':
            return math.atan(args[0])
        elif name == 'FEXP':
            return math.exp(args[0])
        elif name == 'FLOG':
            return math.log(args[0])
        elif name == 'FSQT':
            return math.sqrt(args[0])
        elif name == 'FITR':
            return int(args[0])
        elif name == 'FRAN':
            return random.random() * args[0]
        elif name == 'FABS':
            return abs(args[0])
        elif name == 'FSGN':
            return 1 if args[0] > 0 else -1 if args[0] < 0 else 0
        else:
            # For array access like iflags(num)
            if name in self.arrays:
                index = int(args[0])
                return self.arrays[name].get(index, 0.0)
            raise RuntimeError(f"Unknown function or array: {name}")


def interpret_program(program: Program):
    interpreter = Interpreter(program)
    interpreter.run()
