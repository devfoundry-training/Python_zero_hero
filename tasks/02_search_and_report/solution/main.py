# ============================================================
# Task 02 - Search and report (solution, Core + Stretch)
# ============================================================
# Session 2: loops and strings. Builds on task 01 (same shelf).
#
# Run from the repo root:
#   python tasks/02_search_and_report/solution/main.py             (Core output, checked)
#   python tasks/02_search_and_report/solution/main.py --stretch   (Core, then the Stretch)
# ============================================================

import sys
from typing import Final

# ------------------------------------------------------------
# The shelf from task 01 (parallel arrays, never resized)
# ------------------------------------------------------------

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

SEARCH_TERMS: Final[list[str]] = ["the", "TIME", "zzz"]

# ------------------------------------------------------------
# Core 1: a formatted report table
# ------------------------------------------------------------
# Column widths: id 2 (right), title 30 (left), year 4,
# copies 6 (right), two spaces between columns.
# :>n pads on the left (right-aligns), :<n pads on the right.

print("Report")
print(f"{'ID':>2}  {'Title':<30}  {'Year':<4}  {'Copies':>6}")
print(f"{'-' * 2}  {'-' * 30}  {'-' * 4}  {'-' * 6}")
for i in range(SIZE):
    print(f"{ids[i]:>2}  {titles[i]:<30}  {years[i]:<4}  {copies[i]:>6}")

# ------------------------------------------------------------
# Core 2: case-insensitive search
# ------------------------------------------------------------
# Lower-case both sides, then look for the term anywhere in the
# title. A while loop collects matches into a fixed array.

for term in SEARCH_TERMS:
    found: list[str] = [""] * SIZE
    count = 0
    i = 0
    while i < SIZE:
        if term.lower() in titles[i].lower():
            found[count] = titles[i]
            count += 1
        i += 1

    if count == 0:
        print(f'Search "{term}": no matches')
    else:
        noun = "match" if count == 1 else "matches"
        print(f'Search "{term}": {count} {noun}')
        for j in range(count):
            print(f"  {found[j]}")

# ------------------------------------------------------------
# Core 3: count the words in all titles
# ------------------------------------------------------------
# A word is a run of characters between spaces. split() with no
# argument splits on any run of whitespace, so "Eighty-Four"
# stays one word.

words = 0
for title in titles:
    words += len(title.split())
print(f"Words in titles: {words}")

# ------------------------------------------------------------
# Core 4: the longest title (the first one wins a tie)
# ------------------------------------------------------------

longest = 0
for i in range(1, SIZE):
    if len(titles[i]) > len(titles[longest]):  # > not >=, so ties keep the first
        longest = i
print(f"Longest title: {titles[longest]} ({len(titles[longest])} characters)")

# ------------------------------------------------------------
# Stretch: initials, shortest title, a compact report
# ------------------------------------------------------------

if "--stretch" in sys.argv:
    print("Stretch")
    for title in titles:
        initials = ""
        for word in title.split():
            initials += word[0].upper()
        print(f"{initials:<6}{title}")

    shortest = 0
    for i in range(1, SIZE):
        if len(titles[i]) < len(titles[shortest]):
            shortest = i
    print(f"Shortest title: {titles[shortest]} ({len(titles[shortest])} characters)")

    # Titles longer than 20 characters are cut to 17 plus "..."
    for i in range(SIZE):
        short = titles[i] if len(titles[i]) <= 20 else titles[i][:17] + "..."
        print(f"{ids[i]:>2}  {short:<20}  {years[i]}")
