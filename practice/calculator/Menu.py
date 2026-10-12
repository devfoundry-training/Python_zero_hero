# Menu console
from calculator.Calculator import Calculator


def show_menu():
    """
    Displays the available mathematical operations to the user.
    """
    menu_text = (
        "\nChoose an operation:\n"
        "+ for addition\n"
        "- for subtraction\n"
        "* for multiplication\n"
        "/ for division\n"
        "Type 'quit' to exit."
    )
    print(menu_text)


def get_operation():
    """
    Prompts the user to input a mathematical operation.

    Returns:
        str: The chosen operation in lowercase ('+', '-', '*', '/', or 'quit').
    """
    return input("Enter operation (+, -, *, /) or 'quit' to quit: ").strip().lower()


def get_numbers():
    """
    Prompts the user to enter two numeric values.

    Returns:
        tuple: A pair of floating-point numbers (num1, num2).

    Handles:
        ValueError: If the user enters a non-numeric value, prompts again.
    """
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            return num1, num2
        except ValueError:
            print("Invalid input. Please enter valid numbers.")


def perform_operation(operation, num1, num2):
    """
    Performs the requested mathematical operation using the Calculator class.

    Args:
        operation (str): The mathematical operation ('+', '-', '*', '/').
        num1 (float): The first operand.
        num2 (float): The second operand.

    Returns:
        float or str: The result of the operation, or an error message if invalid.
    """
    my_calc = Calculator(num1, num2)

    operations = {
        "+": my_calc.addition,
        "-": my_calc.subtraction,
        "*": my_calc.multiplication,
        "/": my_calc.division,
    }

    if operation in operations:
        return operations[operation]()

    print("Invalid operation!")
    return None


def run():
    """
    Runs the menu-driven calculator program, allowing the user to perform
    mathematical operations interactively until they choose to quit.
    """
    while True:
        show_menu()
        operation = get_operation()

        if operation == 'quit':
            print("Goodbye!")
            break

        num1, num2 = get_numbers()
        result = perform_operation(operation, num1, num2)

        if result is not None:
            print(f"Result: {result}")
