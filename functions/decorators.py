# ============================================================
# Decorators - Practical Examples
# ============================================================
# A decorator wraps a function to modify its behaviour without
# changing its source code. Common uses: logging, timing,
# access control, memoization.
# ============================================================

import time
import functools

# ------------------------------------------------------------
# Example 1: Execution Timing
# ------------------------------------------------------------


def func_time(func):
    def wrapper():
        pre_execution_stamp = time.time()
        func()
        elapsed = time.time() - pre_execution_stamp
        print(f"{func.__name__} executed in: {elapsed:.4f} seconds")

    return wrapper


@func_time
def sleep_for_three():
    time.sleep(3)


sleep_for_three()

# ------------------------------------------------------------
# Example 2: Argument and Return Value Logging
# ------------------------------------------------------------


def log_function_call(func):
    """Decorator to log function calls, arguments, and return values."""

    @functools.wraps(func)  # Preserves original function name and docstring
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__} with arguments: {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


@log_function_call
def add(a, b):
    """Returns the sum of two numbers."""
    return a + b


# Example usage
sum_result = add(3, 5)
