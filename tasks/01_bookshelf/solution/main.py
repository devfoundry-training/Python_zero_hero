# ============================================================
# Task 01 - Bookshelf (solution, Core + Stretch)
# ============================================================
# Session 1: data types, operators, conditionals, match, arrays.
#
# Run from the repo root:
#   python tasks/01_bookshelf/solution/main.py             (Core output, checked)
#   python tasks/01_bookshelf/solution/main.py --stretch   (Core, then the Stretch)
# ============================================================

import sys
from typing import Final

# ------------------------------------------------------------
# The shelf: four parallel "arrays", one per field
# ------------------------------------------------------------
# Python has no fixed-size array in the core language, so we
# use lists and agree never to grow or shrink them. Position i
# in every list describes the same book.

SIZE: Final[int] = 10
OLD_BEFORE: Final[int] = 1950

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
    """Name the century a year belongs to, using match on year // 100."""
    # // is integer division: 1813 // 100 is 18, never 18.13
    match year // 100:
        case 17:
            return "18th century"
        case 18:
            return "19th century"
        case 19:
            return "20th century"
        case 20:
            return "21st century"
        case _:
            return "unknown era"


def copies_text(count: int) -> str:
    """'out of stock', '1 copy' or 'N copies'."""
    if count == 0:
        return "out of stock"
    elif count == 1:
        return "1 copy"
    else:
        return f"{count} copies"


# ------------------------------------------------------------
# Core 1-3: the catalogue with copies, era and the pre-1950 flag
# ------------------------------------------------------------

print(f"Catalogue ({SIZE} books)")
for i in range(SIZE):
    line = f"{ids[i]} | {titles[i]} | {years[i]} | {copies_text(copies[i])} | {era_of(years[i])}"
    if years[i] < OLD_BEFORE:
        line += " | pre-1950"
    print(line)

# ------------------------------------------------------------
# Core 4: "remove" the even ids
# ------------------------------------------------------------
# A fixed array cannot shrink, so we copy the books we keep into
# a second array of the same size and count the slots we use.

kept_ids: list[int] = [0] * SIZE
kept_titles: list[str] = [""] * SIZE
kept = 0
for i in range(SIZE):
    if ids[i] % 2 != 0:  # % is the remainder: odd ids leave 1
        kept_ids[kept] = ids[i]
        kept_titles[kept] = titles[i]
        kept += 1

print(f"Odd ids only ({kept} books)")
for i in range(kept):
    print(f"{kept_ids[i]} | {kept_titles[i]}")

# ------------------------------------------------------------
# Core 5: totals with arithmetic and comparison operators
# ------------------------------------------------------------

total_copies = 0
out_of_stock = 0
old_books = 0
year_sum = 0
for i in range(SIZE):
    total_copies += copies[i]
    year_sum += years[i]
    if copies[i] == 0:
        out_of_stock += 1
    if years[i] < OLD_BEFORE:
        old_books += 1

print("Totals")
print(f"books: {SIZE}")
print(f"copies: {total_copies}")
print(f"out of stock: {out_of_stock}")
print(f"pre-1950: {old_books}")
print(f"average year: {year_sum // SIZE}")  # integer division, rounds down

# ------------------------------------------------------------
# Stretch: oldest and newest, and a count per era
# ------------------------------------------------------------

if "--stretch" in sys.argv:
    oldest = 0
    newest = 0
    for i in range(1, SIZE):
        if years[i] < years[oldest]:
            oldest = i
        if years[i] > years[newest]:
            newest = i
    print("Stretch")
    print(f"oldest: {titles[oldest]} ({years[oldest]})")
    print(f"newest: {titles[newest]} ({years[newest]})")

    # One counter per era, in a fixed order
    era_names: list[str] = ["18th century", "19th century", "20th century", "21st century"]
    era_counts: list[int] = [0, 0, 0, 0]
    for i in range(SIZE):
        for e in range(len(era_names)):
            if era_of(years[i]) == era_names[e]:
                era_counts[e] += 1
    for e in range(len(era_names)):
        print(f"{era_names[e]}: {era_counts[e]}")
