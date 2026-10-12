# ============================================================
# Doctests - Testing via Docstring Examples
# ============================================================
# Doctests embed test cases inside docstrings using >>> syntax.
# Run with: python -m doctest intro_doctesting.py -v
#
# If output doesn't match the expected value, the test fails.
# Doctests serve as both documentation and lightweight tests.
# ============================================================


def add(a, b):
    """
    Adds two numbers together and returns the result.

    This function takes two arguments and returns their sum. It also works for negative numbers and zero.

    Example usage:

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    >>> add(0, 0)
    0
    >>> add(100, -50)
    50
    >>> add(0, -10)
    -10

    The function handles both integers and floating-point numbers:

    >>> add(3.5, 2.5)
    6.0
    >>> add(1.1, 2.2)
    3.3

    Args:
        a (int, float): The first number to be added.
        b (int, float): The second number to be added.

    Returns:
        int, float: The sum of the two numbers.
    """
    return a + b


if __name__ == "__main__":
    import doctest

    doctest.testmod()

# To run doctests manually, use the following command in your terminal:
# python -m doctest my_script.py -v
