
from collections import deque
from decimal import Decimal
import re


class ExpressionCalculator:
    """
    This is a class in Python that can perform calculations with basic
    arithmetic operations, including addition, subtraction, multiplication,
    division, and modulo.
    """

    def __init__(self):
        """
        Initialize the expression calculator
        """
        self.postfix_stack = deque()
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]

    def calculate(self, expression):
        """
        Calculate the result of the given expression.
        :param expression: string, the expression to be calculated
        :return: float, the calculated result
        """
        self.prepare(expression)
        stack = []

        for token in self.postfix_stack:
            if self.is_operator(token):
                if len(stack) < 2:
                    raise ValueError("Invalid expression")

                second_value = stack.pop()
                first_value = stack.pop()

                result = self._calculate(
                    first_value, second_value, token
                )
                stack.append(result)
            else:
                stack.append(Decimal(token))

        if len(stack) != 1:
            raise ValueError("Invalid expression")

        return float(stack[0])

    def prepare(self, expression):
        """
        Prepare the infix expression for conversion to postfix notation.
        :param expression: string, the infix expression to be prepared
        """
        expression = self.transform(expression)
        self.postfix_stack = deque()
        operator_stack = []

        tokens = re.findall(
            r'\d+(?:\.\d+)?|[+\-*/()%]',
            expression
        )

        if ''.join(tokens) != expression:
            raise ValueError("Invalid expression")

        previous = None

        for token in tokens:
            if token == '-' and (
                previous is None
                or previous in ('+', '-', '*', '/', '%', '(')
            ):
                if previous is None or previous == '(':
                    self.postfix_stack.append('0')
                else:
                    self.postfix_stack.append('0')

                operator_stack.append('(')
                operator_stack.append('-')
                previous = token
                continue

            if not self.is_operator(token):
                self.postfix_stack.append(token)

                if (
                    len(operator_stack) >= 2
                    and operator_stack[-1] == '-'
                    and operator_stack[-2] == '('
                    and previous == '-'
                ):
                    operator_stack.pop()
                    operator_stack.pop()
                    self.postfix_stack.append('-')

            elif token == '(':
                operator_stack.append(token)

            elif token == ')':
                while (
                    operator_stack
                    and operator_stack[-1] != '('
                ):
                    self.postfix_stack.append(
                        operator_stack.pop()
                    )

                if not operator_stack:
                    raise ValueError("Mismatched parentheses")

                operator_stack.pop()

            else:
                while (
                    operator_stack
                    and operator_stack[-1] != '('
                    and self.compare(
                        operator_stack[-1], token
                    )
                ):
                    self.postfix_stack.append(
                        operator_stack.pop()
                    )

                operator_stack.append(token)

            previous = token

        while operator_stack:
            operator = operator_stack.pop()

            if operator in ('(', ')'):
                raise ValueError("Mismatched parentheses")

            self.postfix_stack.append(operator)

    @staticmethod
    def is_operator(c):
        """
        Check if a character is an operator.
        :param c: string, the character to be checked
        :return: bool
        """
        return c in {'+', '-', '*', '/', '(', ')', '%'} if c else False

    def compare(self, cur, peek):
        """
        Compare the precedence of two operators.
        :param cur: string, the current operator
        :param peek: string, the operator at the top
        :return: bool
        """
        priorities = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '%': 2,
            '(': 0,
            ')': 0
        }

        if cur not in priorities or peek not in priorities:
            raise ValueError("Invalid operator")

        return priorities[cur] >= priorities[peek]

    @staticmethod
    def _calculate(first_value, second_value, current_op):
        """
        Perform the mathematical calculation based on the operands
        and operator.
        :param first_value: string, the first operand
        :param second_value: string, the second operand
        :param current_op: string, the operator
        :return: decimal.Decimal, the calculated result
        """
        first_value = Decimal(str(first_value))
        second_value = Decimal(str(second_value))

        if current_op == '+':
            return first_value + second_value

        elif current_op == '-':
            return first_value - second_value

        elif current_op == '*':
            return first_value * second_value

        elif current_op == '/':
            if second_value == 0:
                raise ZeroDivisionError("Division by zero")
            return first_value / second_value

        elif current_op == '%':
            if second_value == 0:
                raise ZeroDivisionError("Modulo by zero")
            return first_value % second_value

        else:
            raise ValueError("Invalid operator")

    @staticmethod
    def transform(expression):
        """
        Transform the infix expression to a format suitable
        for conversion.
        :param expression: string, the infix expression
        :return: string, the transformed expression
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string")

        return re.sub(r'\s+', '', expression)
