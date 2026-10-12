# ============================================================
# Basic Data Types - Primitives and String Formatting
# ============================================================

# ------------------------------------------------------------
# Primitive Types
# ------------------------------------------------------------

my_int = 10
my_float = 10.5
my_bool = True
my_str = "Hello, World!"

print("Integer:", my_int)
print("Float:", my_float)
print("Boolean:", my_bool)
print("String:", my_str)

# ------------------------------------------------------------
# String Formatting - Three Approaches
# ------------------------------------------------------------

# Concatenation (avoid in production - hard to read)
concatenated_str = "Integer: " + str(my_int) + ", Float: " + str(my_float)
print(concatenated_str)

# .format() - older style, still common in legacy code
formatted_str = "Integer: {}, Float: {}, Boolean: {}, String: {}".format(my_int, my_float, my_bool, my_str)
print(formatted_str)

# f-string - preferred approach (Python 3.6+)
f_string = f"Integer: {my_int}, Float: {my_float}, Boolean: {my_bool}, String: {my_str}"
print(f_string)

# ------------------------------------------------------------
# Functions and Return Types
# ------------------------------------------------------------


def my_function() -> str:
    return "This is a string from a function!"


returned_str = my_function()
print("Returned String from Function:", returned_str)
print("The type of the returned value is:", type(returned_str))

# ------------------------------------------------------------
# Type Conversion
# ------------------------------------------------------------

# Narrowing: float to int - fractional part is lost
converted_int = int(my_float)
print("Converted Float to Integer:", converted_int)

# Widening: int to float - safe, no data loss
converted_float = float(my_int)
print("Converted Integer to Float:", converted_float)

# Boolean to int: True -> 1, False -> 0
converted_bool_to_int = int(my_bool)
print("Converted Boolean to Integer:", converted_bool_to_int)
