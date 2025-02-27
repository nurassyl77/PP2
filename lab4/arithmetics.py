def add(a, b):
    return a + b
def subtract(a, b):
    return abs(a - b)
def divide(a, b):
    if a > b and b != 0:
        return a // b
    elif b > a and a != 0:
        return b // a
def multiply(a, b):
    return a * b
def mod(a, b):
    return a % b