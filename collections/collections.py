# ============================================================
# Collections and Comprehensions
# ============================================================

# ------------------------------------------------------------
# Set Operations
# ------------------------------------------------------------

set1 = {1, 2, 3}
set2 = {3, 4, 5}
print(set1 | set2)  # Union: {1, 2, 3, 4, 5}
print(set1 & set2)  # Intersection: {3}
print(set1 - set2)  # Difference: {1, 2}
print(set1 ^ set2)  # Symmetric difference: {1, 2, 4, 5}

# Dictionary operations
first_dict = {1: "value", 2: "another value", 3: "third value"}
# Print all key-value pairs in a dictionary
for key, value in first_dict.items():
    print(f"{key}: {value}")  # 1: value, 2: another value, 3: third value

# ------------------------------------------------------------
# Dictionary Operations
# ------------------------------------------------------------

# Merging dictionaries (Python 3.9+)
dict1 = {1: "A", 2: "B"}
dict2 = {3: "C", 4: "D"}
merged_dict = dict1 | dict2
print(merged_dict)  # {1: 'A', 2: 'B', 3: 'C', 4: 'D'}

# ------------------------------------------------------------
# Basic Collection Types
# ------------------------------------------------------------
first_list = [1, 2, 3]         # List: ordered, mutable, allows duplicates
first_dict = {1: "value"}      # Dictionary: key-value pairs, ordered (Python 3.7+)
first_set = {1, 2, 3}          # Set: unordered, unique elements
first_tup = (1, 2, 3)          # Tuple: ordered, immutable

# Remove duplicates from a list while keeping order
old_list = ["A", "C", "B", "C", "A", "C"]
new_list = list(dict.fromkeys(old_list))
print(new_list)  # ['A', 'C', 'B']

# Tuple unpacking
a, b, c = (1, 2, 3)
print(a, b, c)  # 1 2 3

values = (1, 2, 3, 4, 5)
first, *middle, last = values
print(first, middle, last)  # 1 [2, 3, 4] 5

# ------------------------------------------------------------
# Collections Module - Specialised Types
# ------------------------------------------------------------

# NamedTuple
from collections import namedtuple
Person = namedtuple("Person", ["name", "age"])
p = Person(name="Alice", age=25)
print(p.name, p.age)  # Alice 25

# DefaultDict - provides default values
from collections import defaultdict
d = defaultdict(int)  # Default value is 0
d["a"] += 1
print(d)  # {'a': 1}

# OrderedDict (Pre-3.7)
from collections import OrderedDict
ordered_dict = OrderedDict()
ordered_dict["one"] = 1
ordered_dict["two"] = 2
ordered_dict["three"] = 3
print(ordered_dict)  # {'one': 1, 'two': 2, 'three': 3}

# Deque for efficient insertions
from collections import deque
d = deque([1, 2, 3])
d.appendleft(0)  # Add to front
d.append(4)  # Add to back
print(d)  # deque([0, 1, 2, 3, 4])

# ------------------------------------------------------------
# Comprehensions
# ------------------------------------------------------------
new_dict = {x: x for x in range(1, 5)}
print(new_dict)  # {1: 1, 2: 2, 3: 3, 4: 4}

paired_dict = {x: [j for j in range(0, 5)] for x in range(1, 5)}
print(paired_dict)  # {1: [0,1,2,3,4], 2: [0,1,2,3,4], ...}

new_list = [x for x in range(1, 5)]
print(new_list)  # [1, 2, 3, 4]

new_set = {x for x in range(1, 5)}
print(new_set)  # {1, 2, 3, 4}

new_tup = tuple(x for x in range(1, 5))
print(new_tup)  # (1, 2, 3, 4)

# Filtering and transformation with comprehensions
squared = [x ** 2 for x in range(1, 6)]
print(squared)  # [1, 4, 9, 16, 25]

even_squared = [x ** 2 for x in range(1, 6) if x % 2 == 0]
print(even_squared)  # [4, 16]
