# ============================================================
# Iteration Techniques
# ============================================================

# ------------------------------------------------------------
# Basic Iteration - Lists, Dicts, Sets, Tuples
# ------------------------------------------------------------

# Iterating over a List
my_list = [1, 2, 3, 4, 5]
for item in my_list:
    print(item)  # Prints each item in the list

# Iterating with enumerate() for index and value
my_list = ['a', 'b', 'c']
for index, value in enumerate(my_list):
    print(f"Index: {index}, Value: {value}")

# Iterating over a Dictionary
my_dict = {'a': 1, 'b': 2, 'c': 3}
# Iterate over both keys and values
for key, value in my_dict.items():
    print(f"Key: {key}, Value: {value}")

# Iterate over just keys
for key in my_dict.keys():
    print(f"Key: {key}")

# Iterate over just values
for value in my_dict.values():
    print(f"Value: {value}")

# Iterating over a Set
my_set = {1, 2, 3}
for item in my_set:
    print(item)  # Prints each item in the set (order is not guaranteed)

# Iterating over a Tuple
my_tuple = (10, 20, 30)
for item in my_tuple:
    print(item)  # Prints each item in the tuple

# ------------------------------------------------------------
# Generator Expressions - Memory-Efficient Iteration
# ------------------------------------------------------------
gen = (x ** 2 for x in range(1, 6))
for value in gen:
    print(value)  # Prints each square, values are computed on the fly

# ------------------------------------------------------------
# itertools - Advanced Iteration Patterns
# ------------------------------------------------------------
import itertools

# Infinite Iteration with count()
counter = itertools.count(10, 2)  # Start from 10 and increment by 2
for i in range(5):
    print(next(counter))  # Prints 10, 12, 14, 16, 18

# Iterating in Chunks with islice()
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
chunked = itertools.islice(numbers, 2, 8, 2)  # Start at index 2, stop before index 8, step 2
print(list(chunked))  # [3, 5, 7]

# Cycling through an Iterable
cycle_example = itertools.cycle(['A', 'B', 'C'])  # Will cycle through these letters indefinitely
for _ in range(6):  # Limit it to 6 cycles
    print(next(cycle_example))

# Grouping Iterables with groupby()
# Group items in a list by a function (e.g., even/odd)
items = [1, 2, 3, 4, 5, 6]
grouped = itertools.groupby(items, key=lambda x: x % 2 == 0)
for key, group in grouped:
    print(f"Group key: {key}, Group: {list(group)}")
    # Output: Group key: False, Group: [1], [3], [5]
    #         Group key: True, Group: [2], [4], [6]

# ------------------------------------------------------------
# While Loops and Nested Loops
# ------------------------------------------------------------
counter = 0
while counter < 5:
    print(counter)  # Prints numbers from 0 to 4
    counter += 1

# Iterating with Nested Loops
for i in range(3):
    for j in range(2):
        print(f"i: {i}, j: {j}")
# Prints combinations of i and j (nested loop iteration)
