# Section 3 - Q1: Calculator Function
# Atomcamp AI18 | Python Class Activity

def calculator(a, b, op):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            return "Error: Division by zero"
        return a / b
    else:
        return f"Error: Invalid operator '{op}'"


# Test
print(calculator(10, 5, "+"))   # 15
print(calculator(10, 5, "-"))   # 5
print(calculator(10, 5, "*"))   # 50
print(calculator(10, 5, "/"))   # 2.0
print(calculator(10, 0, "/"))   # Error
print(calculator(10, 5, "%"))   # Invalid operator
