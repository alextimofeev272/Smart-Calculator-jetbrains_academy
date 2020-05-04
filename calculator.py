import re
from string import ascii_letters


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_latin_string(st):
    for i in st:
        if i not in ascii_letters:
            return False
    return True


def postfix_translate(infix):
    priority = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "(": 3,
        ")": 3
    }
    qeque = []
    stack = []
    for i in infix:
        if is_number(i):
            qeque.append(i)
        elif i in ("+", "-", "*", "/"):
            if stack == [] or stack[-1] == "(":
                stack.append(i)
            elif priority[i] > priority[stack[-1]]:
                stack.append(i)
            else:
                for op in reversed(range(len(stack))):
                    if priority[i] > priority[stack[op]] or stack[op] == "(":
                        stack.append(i)
                        break
                    else:
                        qeque.append(stack.pop(op))
                        if not stack:
                            stack.append(i)
        elif i == "(":
            stack.append(i)
        elif i == ")":
            for op in reversed(range(len(stack))):
                if stack[op] == "(":
                    stack.pop(op)
                    break
                else:
                    qeque.append(stack.pop(op))
    for i in reversed(range(len(stack))):
        qeque.append(stack.pop(i))
    return qeque


def calculate(qeque):
    stack = []
    for i in qeque:
        if is_number(i):
            try:
                stack.append(int(i))
            except ValueError:
                stack.append(float(i))
        elif i in '+':
            stack.append(stack.pop(-2) + stack.pop(-1))
        elif i in '-':
            stack.append(stack.pop(-2) - stack.pop(-1))
        elif i in '*':
            stack.append(stack.pop(-2) * stack.pop(-1))
        elif i in '/':
            try:
                stack.append(stack.pop(-2) / stack.pop(-1))
            except ZeroDivisionError:
                return "Indefinitely. Division by zero."
    return stack[0]


def check(expression_):
    for i in range(len(expression)):
        if expression_[i] in ('*', '/') and not (is_number(expression_[i + 1]) or expression_[i + 1] == "("):
            return False
        elif expression_[i] == "(" and ")" not in expression_[i:]:
            return False
        elif expression_[i] == ")" and "(" not in expression_[:i]:
            return False
    return True


def delete_minus(a):
    b = []
    c = []
    for i in range(len(a)):
        if a[i] == "+" and a[i + 1] == "+":
            b.append(i)
        if "-" in a[i] and len(a[i]) > 1:
            c.append(i)
    for i in c:
        if len(a[i]) % 2 == 0:
            a[i] = '+'
        else:
            a[i] = "-"
    for i in reversed(b):
        a.pop(i)
    return a


memory = {}
while True:
    operation = input()
    if operation == "":
        continue
    elif is_number(operation):
        print(operation)
    elif operation[0] == "/":
        if operation == "/exit":
            print("Bye!")
            break
        elif operation == "/help":
            print("The program calculates the sum of numbers")
        else:
            print("Unknown command")
    elif '=' in operation:
        if operation.count("=") == 1:
            operation = operation.replace(' ', '')
            identifier, assignment = operation.split('=')
            if not is_latin_string(identifier):
                print('Invalid identifier')
            elif is_number(assignment):
                memory[identifier] = assignment
            elif not assignment:
                print('Invalid assignment')
            elif assignment not in memory:
                print("Unknown variable")
            elif assignment in memory:
                memory[identifier] = memory[assignment]
            else:
                print('Invalid identifier')
        else:
            print('Invalid assignment')
    else:
        expression = delete_minus([i for i in re.split("([^0-9a-zA-Z.-])", operation) if i != '' and i != " "])
        if check(expression):
            for i in range(len(expression)):
                if expression[i] in memory:
                    expression[i] = memory[expression[i]]
            print(calculate(postfix_translate(expression)))
        else:
            print("Invalid expression")
