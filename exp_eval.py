from stack_array import Stack


# You do not need to change this class
class PostfixFormatException(Exception):
    pass


def postfix_eval(input_str):
    '''Evaluates a postfix expression
    
    Input argument:  a string containing a postfix expression where tokens 
    are space separated.  Tokens are either operators + - * / ** >> << or numbers.
    Returns the result of the expression evaluation. 
    Raises an PostfixFormatException if the input is not well-formed
    DO NOT USE PYTHON'S EVAL FUNCTION!!!'''
    expression = input_str.split()
    stack = Stack(30)
    if len(input_str) == 0:
        raise PostfixFormatException("Empty input")
    for c in expression:
        if c.replace("-", "").isdigit():
            stack.push(int(c))
        elif c.replace(".", "").replace("-", "").isdigit():
            stack.push(float(c))
        elif c == "+":  # if operator is +
            if stack.num_items < 2:
                raise PostfixFormatException("Insufficient operands")
            x = stack.pop()
            y = stack.pop()
            stack.push(y + x)
        elif c == "-":  # if operator is -
            if stack.num_items < 2:
                raise PostfixFormatException("Insufficient operands")
            x = stack.pop()
            y = stack.pop()
            stack.push(y - x)
        elif c == "/":  # if operator is /
            if stack.num_items < 2:
                raise PostfixFormatException("Insufficient operands")
            x = stack.pop()
            y = stack.pop()
            if x == 0:
                raise ValueError
            stack.push(y / x)
        elif c == "*":  # if operator is *
            if stack.num_items < 2:
                raise PostfixFormatException("Insufficient operands")
            x = stack.pop()
            y = stack.pop()
            stack.push(y * x)
        elif c == "**":  # if operator is **
            if stack.num_items < 2:
                raise PostfixFormatException("Insufficient operands")
            x = stack.pop()
            y = stack.pop()
            stack.push(y ** x)  # associativity right
        elif c == ">>":  # if operator is >>
            if stack.num_items < 2:
                raise PostfixFormatException("Insufficient operands")
            x = stack.pop()
            y = stack.pop()
            if type(x) is float or type(y) is float:
                raise PostfixFormatException("Illegal bit shift operand")
            stack.push(int(y) >> int(x))
        elif c == "<<":  # if operator is <<
            if stack.num_items < 2:
                raise PostfixFormatException("Insufficient operands")
            x = stack.pop()
            y = stack.pop()
            if type(x) is float or type(y) is float:
                raise PostfixFormatException("Illegal bit shift operand")
            stack.push(int(y) << int(x))
        else:
            raise PostfixFormatException("Invalid token")  # Raise error invalid character
    result = stack.pop()
    if not stack.is_empty():
        raise PostfixFormatException("Too many operands")  # Raise error if stack is not empty at end
    return result


def infix_to_postfix(input_str):
    '''Converts an infix expression to an equivalent postfix expression

    Input argument:  a string containing an infix expression where tokens are 
    space separated.  Tokens are either operators + - * / ** >> << parentheses ( ) or numbers
    Returns a String containing a postfix expression '''

    op_stack = Stack(30)  # create stack
    expression = input_str.split()  # split string
    result = ""
    for c in expression:  # loop for every token
        if c.replace(".", "").replace("-", "").isdigit():  # When encounter a value append to RPN
            result += str(c + " ")
        elif c == "(":
            op_stack.push(c)
        elif c == ")":
            while op_stack.peek() != "(":
                x = op_stack.pop()
                result += str(x + " ")
            op_stack.pop()
        elif isOperator(c):
            if not op_stack.is_empty():
                o2 = op_stack.peek()
                if o2 == "(":
                    op_stack.peek()
                elif (c != "**" and precedence(c) <= precedence(o2)) or (c == "**" and precedence(c) < precedence(o2)):
                    result += str(op_stack.pop()) + " "
            op_stack.push(c)
    while not op_stack.is_empty():
        x = op_stack.pop()
        result += str(x + " ")
    result = result.rstrip()
    return result


def prefix_to_postfix(input_str):
    '''Converts a prefix expression to an equivalent postfix expression
    
    Input argument:  a string containing a prefix expression where tokens are 
    space separated.  Tokens are either operators + - * / ** >> << or numbers
    Returns a String containing a postfix expression (tokens are space separated)'''
    expression = input_str.split()
    rexpression = expression[::-1]
    stack = Stack(30)
    for c in rexpression:
        if c.replace(".", "").replace("-", "").isdigit():
            stack.push(c + " ")
        if isOperator(c):
            x = stack.pop()
            y = stack.pop()
            stack.push(x + y + c + " ")
    result = stack.pop()
    return result.rstrip()


def precedence(operator):  # Assigns numbers to different operators for precedence uses
    if operator == "+" or operator == "-":
        return 1
    if operator == "*" or operator == "/":
        return 2
    if operator == "**":
        return 3
    if operator == "<<" or operator == ">>":
        return 4


def isOperator(ch):  # Returns true if token is an operator
    if ch == "+" or ch == "-" or ch == "*" or ch == "/" or ch == "**" or ch == "<<" or ch == ">>":
        return True
    return False
