from collections import deque
from decimal import Decimal

class ExpressionCalculator:
    """
    This is a class in Python that can perform calculations with basic arithmetic operations, including addition, subtraction, multiplication, division, and modulo.
    """

    _PRECEDENCE = {
        "(": 0,
        ")": 0,
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "%": 2,
    }

    def __init__(self):
        """
        Initialize the expression calculator
        """
        self.postfix_stack = deque()
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]

    def calculate(self, expression):
        """
        Calculate the result of the given postfix expression
        :param expression: string, the postfix expression to be calculated
        :return: float, the calculated result
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.calculate("2 + 3 * 4")
        14.0

        """
        if not expression or not str(expression).strip():
            return 0.0

        expr_str = str(expression).strip()
        tokens = expr_str.split()

        if "(" not in expr_str and ")" not in expr_str and len(tokens) > 1:
            eval_stack = []
            valid_postfix = True
            for tok in tokens:
                if self.is_operator(tok) and tok not in ("(", ")"):
                    if len(eval_stack) < 2:
                        valid_postfix = False
                        break
                    b = eval_stack.pop()
                    a = eval_stack.pop()
                    eval_stack.append(self._calculate(a, b, tok))
                else:
                    try:
                        eval_stack.append(Decimal(tok))
                    except Exception:
                        valid_postfix = False
                        break
            if valid_postfix and len(eval_stack) == 1:
                return float(eval_stack[0])

        self.prepare(expr_str)
        eval_stack = []
        for token in self.postfix_stack:
            if self.is_operator(token):
                second_val = eval_stack.pop()
                first_val = eval_stack.pop()
                eval_stack.append(self._calculate(first_val, second_val, token))
            else:
                eval_stack.append(Decimal(token))

        return float(eval_stack[0]) if eval_stack else 0.0

    def prepare(self, expression):
        """
        Prepare the infix expression for conversion to postfix notation
        :param expression: string, the infix expression to be prepared
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.prepare("2+3*4")

        expression_calculator.postfix_stack = ['2', '3', '4', '*', '+']
        """
        self.postfix_stack = deque()
        transformed = self.transform(expression)
        op_stack = []
        num_buffer = []
        prev_token = None

        i = 0
        n = len(transformed)
        while i < n:
            ch = transformed[i]

            if ch.isdigit() or ch == ".":
                num_buffer.append(ch)
                prev_token = "num"
            elif ch == "-" and (prev_token is None or prev_token in ("op", "(")):
                if num_buffer:
                    self.postfix_stack.append("".join(num_buffer))
                    num_buffer.clear()
                num_buffer.append("-")
                prev_token = "num"
            elif ch == "+" and (prev_token is None or prev_token in ("op", "(")):
                if num_buffer:
                    self.postfix_stack.append("".join(num_buffer))
                    num_buffer.clear()
                prev_token = "op"
            elif self.is_operator(ch):
                if num_buffer:
                    self.postfix_stack.append("".join(num_buffer))
                    num_buffer.clear()

                if ch == "(":
                    op_stack.append(ch)
                    prev_token = "("
                elif ch == ")":
                    while op_stack and op_stack[-1] != "(":
                        self.postfix_stack.append(op_stack.pop())
                    if op_stack and op_stack[-1] == "(":
                        op_stack.pop()
                    prev_token = ")"
                else:
                    while (
                        op_stack
                        and op_stack[-1] != "("
                        and self.compare(op_stack[-1], ch)
                    ):
                        self.postfix_stack.append(op_stack.pop())
                    op_stack.append(ch)
                    prev_token = "op"
            i += 1

        if num_buffer:
            self.postfix_stack.append("".join(num_buffer))

        while op_stack:
            top = op_stack.pop()
            if top != "(":
                self.postfix_stack.append(top)

    @staticmethod
    def is_operator(c):
        """
        Check if a character is an operator in {'+', '-', '*', '/', '(', ')', '%'}
        :param c: string, the character to be checked
        :return: bool, True if the character is an operator, False otherwise
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.is_operator("+")
        True

        """
        return c in {"+", "-", "*", "/", "(", ")", "%"}

    def compare(self, cur, peek):
        """
        Compare the precedence of two operators
        :param cur: string, the current operator
        :param peek: string, the operator at the top of the operator stack
        :return: bool, True if the current operator has higher or equal precedence, False otherwise
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.compare("+", "-")
        True

        """
        cur_prio = self._PRECEDENCE.get(cur, 0)
        peek_prio = self._PRECEDENCE.get(peek, 0)
        return cur_prio >= peek_prio

    @staticmethod
    def _calculate(first_value, second_value, current_op):
        """
        Perform the mathematical calculation based on the given operands and operator
        :param first_value: string, the first operand
        :param second_value: string, the second operand
        :param current_op: string, the operator
        :return: decimal.Decimal, the calculated result
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator._calculate("2", "3", "+")
        5.0

        """
        a = first_value if isinstance(first_value, Decimal) else Decimal(str(first_value))
        b = second_value if isinstance(second_value, Decimal) else Decimal(str(second_value))

        if current_op == "+":
            return a + b
        if current_op == "-":
            return a - b
        if current_op == "*":
            return a * b
        if current_op == "/":
            return a / b
        if current_op == "%":
            return a % b
        raise ValueError(f"Unsupported operator: {current_op}")

    @staticmethod
    def transform(expression):
        """
        Transform the infix expression to a format suitable for conversion
        :param expression: string, the infix expression to be transformed
        :return: string, the transformed expression
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.transform("2 + 3 * 4")
        "2+3*4"

        """
        return "".join(str(expression).split())