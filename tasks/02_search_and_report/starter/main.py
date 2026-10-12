# ============================================================
# Task 02 - Search and report (starter)
# ============================================================
# Session 2: loops and strings. Builds on task 01: the same shelf
# of ten books in the same parallel lists. Replace each "not
# implemented" line with your code (see README.md).
#
# Run from the repo root:
#   python tasks/02_search_and_report/starter/main.py
# Check it:
#   python tasks/check/check.py 02 -- python tasks/02_search_and_report/starter/main.py
# ============================================================

from typing import Final

# ------------------------------------------------------------
# The shelf from task 01 (parallel lists, never resized)
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
# Core 1: the report table
# ------------------------------------------------------------
# TODO: "Report", a header row, a row of dashes, one row per book.
# Widths: ID 2 (right), Title 30 (left), Year 4, Copies 6 (right).
print("Report: not implemented")

# ------------------------------------------------------------
# Core 2: case-insensitive search
# ------------------------------------------------------------
# TODO: for each term, collect the matching titles with a while
# loop into a fixed list plus a count, then print them
for term in SEARCH_TERMS:
    print(f'Search "{term}": not implemented')

# ------------------------------------------------------------
# Core 3 and 4: words in titles, the longest title
# ------------------------------------------------------------
# TODO: count the words in all ten titles (split on spaces)
print("Words in titles: not implemented")
# TODO: the longest title; the first one wins a tie
print("Longest title: not implemented")
