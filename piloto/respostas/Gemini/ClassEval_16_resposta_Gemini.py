class Calculator:
    """ This is a class for a calculator, capable of performing basic arithmetic calculations on numerical expressions using the operators +, -, *, /, and ^ (exponentiation)."""

    def __init__(self):
        """
        Initialize the operations performed by the five operators'+','-','*','/','^'
        """
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: x ** y
        }

    def calculate(self, expression):
        """
        Calculate the value of a given expression
        :param expression: string, given expression
        :return:If successful, returns the value of the expression; otherwise, returns None
        >>> calculator = Calculator()
        >>> calculator.calculate('1+2-3')
        0.0
        """
        if not isinstance(expression, str):
            return None

        expr = expression.replace(' ', '')
        if not expr:
            return None

        operand_stack = []
        operator_stack = []
        i = 0
        n = len(expr)
        expect_operand = True

        try:
            while i < n:
                ch = expr[i]

                if ch == '(':
                    if not expect_operand:
                        return None
                    operator_stack.append(ch)
                    i += 1
                elif ch == ')':
                    if expect_operand:
                        return None
                    while operator_stack and operator_stack[-1] != '(':
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                    if not operator_stack or operator_stack[-1] != '(':
                        return None
                    operator_stack.pop()
                    expect_operand = False
                    i += 1
                elif expect_operand and (ch.isdigit() or ch == '.' or ch in ('+', '-')):
                    start = i
                    if ch in ('+', '-'):
                        i += 1
                        if i >= n or (not expr[i].isdigit() and expr[i] != '.'):
                            return None
                    has_digit = False
                    has_dot = False
                    while i < n and (expr[i].isdigit() or expr[i] == '.'):
                        if expr[i] == '.':
                            if has_dot:
                                return None
                            has_dot = True
                        else:
                            has_digit = True
                        i += 1
                    if not has_digit:
                        return None
                    num = float(expr[start:i])
                    operand_stack.append(num)
                    expect_operand = False
                elif not expect_operand and ch in self.operators:
                    while (
                        operator_stack
                        and operator_stack[-1] != '('
                        and (
                            self.precedence(operator_stack[-1]) > self.precedence(ch)
                            or (
                                self.precedence(operator_stack[-1]) == self.precedence(ch)
                                and ch != '^'
                            )
                        )
                    ):
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                    expect_operand = True
                    i += 1
                else:
                    return None

            if expect_operand:
                return None

            while operator_stack:
                if operator_stack[-1] in ('(', ')'):
                    return None
                operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)

            if len(operand_stack) != 1:
                return None

            return float(operand_stack[0])
        except Exception:
            return None

    def precedence(self, operator):
        """
        Returns the priority of the specified operator, where the higher the priority, the greater the assignment. The priority of '^' is greater than '/' and '*', and the priority of '/' and '*' is greater than '+' and '-'
        :param operator: string, given operator
        :return: int, the priority of the given operator, otherwise return 0
        >>> calculator = Calculator()
        >>> calculator.precedence('+')
        1
        >>> calculator.precedence('^')
        3
        """
        if operator in ('+', '-'):
            return 1
        elif operator in ('*', '/'):
            return 2
        elif operator == '^':
            return 3
        return 0

    def apply_operator(self, operand_stack, operator_stack):
        """
        Use the operator at the top of the operator stack to perform the operation on the two numbers at the top of the operator stack, and store the results at the top of the operator stack
        :param operand_stack:list
        :param operator_stack:list
        :return: the updated operand_stack and operator_stack
        >>> calculator = Calculator()
        >>> calculator.apply_operator([1, 2, 3], ['+', '-'])
        ([1, -1], ['-'])
        """
        operator = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        result = self.operators[operator](operand1, operand2)
        operand_stack.append(result)
        return operand_stack, operator_stack