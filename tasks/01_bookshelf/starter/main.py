# ============================================================
# Task 01 - Bookshelf (starter)
# ============================================================
# Session 1: data types, operators, conditionals, match, arrays.
# The data is here already. Replace each "not implemented" line
# with your code, one Core step at a time (see README.md).
#
# Run from the repo root:
#   python tasks/01_bookshelf/starter/main.py
# Check it:
#   python tasks/check/check.py 01 -- python tasks/01_bookshelf/starter/main.py
# ============================================================

from typing import Final

# ------------------------------------------------------------
# Core 1: the shelf, four parallel "arrays", one per field
# ------------------------------------------------------------
# Python lists stand in for fixed arrays: never append or remove.
# Position i in every list describes the same book.

SIZE: Final[int] = 10

ids: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
titles: list[str] = [
    "Pride and Prejudice",
    "Nineteen Eighty-Four",
    "The Hobbit",
    "Dune",
    "Robinson Crusoe",
    "The Time Machine",
    "Animal Farm",
    "Emma",
    "The Left Hand of Darkness",
    "Murder on the Orient Express",
]
years: list[int] = [1813, 1949, 1937, 1965, 1719, 1895, 1945, 1815, 1969, 1934]
copies: list[int] = [3, 2, 0, 4, 1, 2, 5, 1, 0, 2]


def era_of(year: int) -> str:
    """Core 4: match on year // 100 (17 is '18th century' ... 20 is '21st century')."""
    # TODO: use match / case on year // 100
    return "not implemented"


def copies_text(count: int) -> str:
    """Core 3: 'out of stock', '1 copy' or 'N copies'."""
    # TODO: use if / elif / else
    return "not implemented"


# ------------------------------------------------------------
# Core 2 to 5: the catalogue, with copies, era and pre-1950 flag
# ------------------------------------------------------------
# TODO: print "Catalogue (10 books)", then one line per book:
#   id | title | year | copies text | century [| pre-1950]
print("Catalogue: not implemented")

# ------------------------------------------------------------
# Core 6: "remove" the even ids
# ------------------------------------------------------------
# TODO: copy the odd-id books into a second pair of lists of the
# same size, count the slots used, then print them
print("Odd ids only: not implemented")

# ------------------------------------------------------------
# Core 7: the totals
# ------------------------------------------------------------
# TODO: books, copies, out of stock, pre-1950, average year (//)
print("Totals: not implemented")
