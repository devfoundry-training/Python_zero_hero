# ============================================================
# Task 03 - Functions and a menu (starter)
# ============================================================
# Session 3: functions. Builds on tasks 01 and 02: every feature
# becomes a function that RETURNS its result, and only the menu
# prints. era_of and copies_text come from task 01 already done;
# fill in the rest (see README.md).
#
# Run from the repo root (type the choices, or pipe the file in):
#   python tasks/03_functions/starter/main.py < tasks/data/input_03.txt
# Check it:
#   python tasks/check/check.py 03 -- python tasks/03_functions/starter/main.py
# ============================================================

import sys
from typing import Final

MENU: Final[str] = "Menu: 1 catalogue | 2 search | 3 report | 4 stats | 0 quit"

SIZE: Final[int] = 10
OLD_BEFORE: Final[int] = 1950

IDS: Final[list[int]] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
TITLES: Final[list[str]] = [
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
YEARS: Final[list[int]] = [1813, 1949, 1937, 1965, 1719, 1895, 1945, 1815, 1969, 1934]
COPIES: Final[list[int]] = [3, 2, 0, 4, 1, 2, 5, 1, 0, 2]


# ------------------------------------------------------------
# From task 01 (done)
# ------------------------------------------------------------

def era_of(year: int) -> str:
    """The century a year belongs to, from year // 100."""
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
    if count == 1:
        return "1 copy"
    return f"{count} copies"


# ------------------------------------------------------------
# Core 1: every task 01/02 feature as a function (TODO)
# ------------------------------------------------------------
# Each one takes what it needs as parameters and returns a value
# or a list of lines. None of them prints.

def catalogue_line(index: int) -> str:
    """The task 01 catalogue line for the book at this index."""
    return "not implemented"


def search(term: str) -> list[str]:
    """Titles containing term, ignoring case, in shelf order."""
    return ["not implemented"]


def report() -> list[str]:
    """The task 02 report table, starting with 'Report'."""
    return ["Report: not implemented"]


def word_count() -> int:
    return 0  # not implemented


def longest_title() -> str:
    return "not implemented"


def total_copies() -> int:
    return 0  # not implemented


def average_year() -> int:
    return 0  # not implemented


# ------------------------------------------------------------
# Core 2 to 5: the menu loop (TODO)
# ------------------------------------------------------------

def read_line() -> str | None:
    """Read one line, echo it as '> TEXT' and return it trimmed.
    sys.stdin.readline() returns "" only at the end of the input:
    return None then."""
    return None  # not implemented


def run_menu() -> None:
    print("Library Manager")
    # TODO: print MENU, read a choice, act on it, until "0" or the
    # end of the input. Compare the choice as text.
    print("Menu loop: not implemented")
    print("Goodbye")


if __name__ == "__main__":
    run_menu()
