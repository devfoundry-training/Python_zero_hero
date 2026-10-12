# ============================================================
# Functions - Definitions, Arguments, and Scope
# ============================================================

# ------------------------------------------------------------
# Basic Function Definition
# ------------------------------------------------------------

def new_function(para, para_one):
    result = para + para_one
    return result


# ------------------------------------------------------------
# Default Arguments
# ------------------------------------------------------------

def next_function(no, first_name="bob", last_name="jones"):
    return "{0}, {1}, {2}".format(no, first_name, last_name)


print(next_function(1))  # Uses default names
print(next_function(1, first_name="Ed"))  # Pass by name


# Note: positional arguments cannot follow keyword arguments

# ------------------------------------------------------------
# Variadic Functions - *args and **kwargs
# ------------------------------------------------------------

# *args collects extra positional arguments as a tuple
def variadic_function(a, b, *z):
    return a, b, z


print(variadic_function(1, 2, 3, 4, 5, 6))


# **kwargs collects extra keyword arguments as a dictionary
def print_vat(**kwargs):
    print(kwargs)


print_vat(vatpc=15, gross=9.55, message='Summary')


# ------------------------------------------------------------
# Keyword-Only Arguments
# ------------------------------------------------------------
# Using * enforces keyword-only arguments

def force_function(*, no=0, first_name="bob", last_name="jones"):
    return "{0}, {1}, {2}".format(no, first_name, last_name)


# ------------------------------------------------------------
# Argument Unpacking
# ------------------------------------------------------------

def unpack_function(a, b, c):
    return a, b, c


new_tup = "One", "Two", "Three"
unpack_function(*new_tup)


# ------------------------------------------------------------
# Nested Functions
# ------------------------------------------------------------

def outer_func():
    print("Outer function!")

    def inner_func():
        print("Inner function!")

    inner_func()


outer_func()


# Nested function returning a value

def str_out_function(val):
    def inner():
        print(f"{val}")

    inner()


str_out_function("Str")


# ------------------------------------------------------------
# Function Annotations
# ------------------------------------------------------------

def print_vat(**kwargs: 'VAT, gross and message'):
    print(kwargs)


print(print_vat.__annotations__)

# ------------------------------------------------------------
# Scope - Global, Local, and Nonlocal
# ------------------------------------------------------------

var = 1
result = 3


def scope_test():
    global result
    result = 5


scope_test()
print(result)  # Output: 5


# nonlocal allows modification of a variable from an enclosing scope

def myfunc1():
    x = "John"

    def myfunc2():
        nonlocal x
        x = "Mike"

    myfunc2()
    return x


print(myfunc1())  # Output: Mike


# Quick *args recap

def simple_args(*args):
    print(args)


simple_args(1, 2, 3)  # Output: (1, 2, 3)
