class BalancedBrackets:
    """
    This class is used to check if the brackets in a given string are balanced.
    """

    def __init__(self, expr):
        """
        Initializes the class with an expression.
        
        :param expr: The input string to be analyzed.
        """
        self.expr = expr
        self.left_brackets = ['(', '{', '[']
        self.right_brackets = [')', '}', ']']

    def clear_expr(self):
        """
        Clears the expression by removing all non-bracket characters.
        """
        self.expr = ''.join([c for c in self.expr if c in self.left_brackets or c in self.right_brackets])

    def check_balanced_brackets(self):
        """
        Checks if the brackets in the expression are balanced.
        
        :return: True if the brackets are balanced, False otherwise.
        """
        # First, clear the expression to get only brackets
        cleared_expr = ''.join([c for c in self.expr if c in self.left_brackets or c in self.right_brackets])

        stack = []
        for char in cleared_expr:
            if char in self.left_brackets:
                stack.append(char)
            else:
                if not stack:
                    return False
                top = stack.pop()
                if (top == '(' and char != ')') or (top == '{' and char != '}') or (top == '[' and char != ']'):
                    return False
        return len(stack) == 0


# Example 1: Balanced brackets
bb = BalancedBrackets("a(b)c")
bb.clear_expr()
print(bb.check_balanced_brackets())  # Output: True

# Example 2: Unbalanced brackets
bb = BalancedBrackets("(()")
bb.clear_expr()
print(bb.check_balanced_brackets())  # Output: False

# Example 3: Nested brackets
bb = BalancedBrackets("({[]})")
bb.clear_expr()
print(bb.check_balanced_brackets())  # Output: True
