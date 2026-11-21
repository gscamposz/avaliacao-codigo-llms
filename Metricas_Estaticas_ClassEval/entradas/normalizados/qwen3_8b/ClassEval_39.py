def prepare(expression):
    # Step 1: Remove all spaces from the input expression
    cleaned = expression.replace(" ", "")
    
    # Step 2: Tokenize the expression
    tokens = []
    temp = ""
    for c in cleaned:
        if c.isdigit():
            temp += c
        else:
            if temp:
                tokens.append(temp)
                temp = ""
            tokens.append(c)
    if temp:
        tokens.append(temp)
    
    # Step 3: Define operator precedence and mapping
    operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]  # [ +, -, *, /, (, ), % ]
    op_to_index = {
        '+': 0,
        '-': 1,
        '*': 2,
        '/': 3,
        '(': 4,
        ')': 5,
        '%': 6
    }
    
    # Step 4: Initialize stack and output list
    stack = []
    output = []
    
    # Step 5: Apply the Shunting Yard Algorithm
    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()  # Remove the '('
        else:
            # Token is an operator
            while stack and stack[-1] != '(' and operat_priority[op_to_index[stack[-1]]] >= operat_priority[op_to_index[token]]:
                output.append(stack.pop())
            stack.append(token)
    
    # Step 6: Add remaining operators from the stack to the output
    while stack:
        output.append(stack.pop())
    
    return output


expr = "3 + 4 * 2 / (1 - 5) % 2"
postfix = prepare(expr)
print("Postfix Notation:", postfix)
