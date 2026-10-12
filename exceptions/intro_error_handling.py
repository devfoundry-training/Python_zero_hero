# ============================================================
# Error Handling - try/except/else/finally
# ============================================================

# ------------------------------------------------------------
# Basic Try-Except
# ------------------------------------------------------------
try:
    # Division by zero
    result = 10 / 0
except ZeroDivisionError:
    print("Error: Division by zero is not allowed!")

# Multiple exception types in one handler
try:
    num = int("Hello")  # This will raise a ValueError
except (ValueError, TypeError) as e:
    print(f"Error: {e}")

# else block - runs only if no exception was raised
try:
    value = 5
    result = value / 2
except ZeroDivisionError:
    print("Error: Division by zero.")
else:
    print(f"The result is: {result}")

# finally block - always executes regardless of outcome
try:
    file = open("non_existent_file.txt", "r")
except FileNotFoundError:
    print("Error: File not found!")
finally:
    print("This will always execute!")

# ------------------------------------------------------------
# Raising Exceptions Manually
# ------------------------------------------------------------
try:
    raise ValueError("This is a custom error!")
except ValueError as e:
    print(f"Custom Error: {e}")
