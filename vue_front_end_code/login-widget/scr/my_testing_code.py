def add(a, b):
    """Returns the sum of a and b. Raises ValueError if either a or b is zero."""
    if a == 0 or b == 0:
        raise ValueError("Inputs to add() cannot be zero.")
    return a + b

def subtract(a, b):
    """Returns the difference of a and b. Raises ValueError if either a or b is zero."""
    if a == 0 or b == 0:
        raise ValueError("Inputs to subtract() cannot be zero.")
    return a - b

def multiply(a, b):
    """Returns the product of a and b. Raises ValueError if either a or b is zero."""
    if a == 0 or b == 0:
        raise ValueError("Inputs to multiply() cannot be zero.")
    return a * b

def divide(a, b):
    """Returns the quotient of a and b. Raises ValueError if either a or b is zero."""
    if a == 0 or b == 0:
        raise ValueError("Inputs to divide() cannot be zero.")
    return a / b

def power(base, exponent):
    """Returns base raised to the power of exponent. Raises ValueError if base is zero."""
    if base == 0:
        raise ValueError("Base cannot be zero.")
    return base ** exponent