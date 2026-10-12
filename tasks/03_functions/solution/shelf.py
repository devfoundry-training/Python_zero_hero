# ============================================================
# Task 03 - shelf module: every task 01/02 feature as a function
# ============================================================
# Stretch 1: the functions live in their own module and main.py
# imports them. Nothing here prints; every function returns a
# value (a string, a number or a list of lines) and main.py
# decides what to print.
# ============================================================

from typing import Final

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
# Small helpers (task 01)
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


def is_old(year: int) -> bool:
    return year < OLD_BEFORE


def plural(count: int, singular: str, many: str) -> str:
    """'1 match' or '4 matches': the number and the right noun."""
    return f"{count} {singular if count == 1 else many}"


# ------------------------------------------------------------
# Features (tasks 01 and 02)
# ------------------------------------------------------------

def catalogue_line(i: int) -> str:
    line = f"{IDS[i]} | {TITLES[i]} | {YEARS[i]} | {copies_text(COPIES[i])} | {era_of(YEARS[i])}"
    if is_old(YEARS[i]):
        line += " | pre-1950"
    return line


def catalogue() -> list[str]:
    lines = [f"Catalogue ({SIZE} books)"]
    for i in range(SIZE):
        lines.append(catalogue_line(i))
    return lines


def search(term: str) -> list[str]:
    """Titles containing term, ignoring case, in shelf order."""
    found: list[str] = []
    for title in TITLES:
        if term.lower() in title.lower():
            found.append(title)
    return found


def search_report(term: str) -> list[str]:
    found = search(term)
    if not found:
        return [f'Search "{term}": no matches']
    lines = [f'Search "{term}": {plural(len(found), "match", "matches")}']
    for title in found:
        lines.append(f"  {title}")
    return lines


def report() -> list[str]:
    lines = [
        "Report",
        f"{'ID':>2}  {'Title':<30}  {'Year':<4}  {'Copies':>6}",
        f"{'-' * 2}  {'-' * 30}  {'-' * 4}  {'-' * 6}",
    ]
    for i in range(SIZE):
        lines.append(f"{IDS[i]:>2}  {TITLES[i]:<30}  {YEARS[i]:<4}  {COPIES[i]:>6}")
    return lines


def total_copies() -> int:
    total = 0
    for count in COPIES:
        total += count
    return total


def count_out_of_stock() -> int:
    count = 0
    for copies in COPIES:
        if copies == 0:
            count += 1
    return count


def count_old() -> int:
    count = 0
    for year in YEARS:
        if is_old(year):
            count += 1
    return count


def average_year() -> int:
    total = 0
    for year in YEARS:
        total += year
    return total // SIZE  # integer division


def word_count() -> int:
    words = 0
    for title in TITLES:
        words += len(title.split())
    return words


def longest_title() -> str:
    longest = TITLES[0]
    for title in TITLES[1:]:
        if len(title) > len(longest):
            longest = title
    return longest


def oldest_and_newest() -> tuple[int, int]:
    """Stretch 2: two results from one function (a tuple of indexes)."""
    oldest = 0
    newest = 0
    for i in range(1, SIZE):
        if YEARS[i] < YEARS[oldest]:
            oldest = i
        if YEARS[i] > YEARS[newest]:
            newest = i
    return oldest, newest


def stats(include_stretch: bool = False) -> list[str]:
    longest = longest_title()
    lines = [
        "Stats",
        f"books: {SIZE}",
        f"copies: {total_copies()}",
        f"out of stock: {count_out_of_stock()}",
        f"pre-1950: {count_old()}",
        f"average year: {average_year()}",
        f"words in titles: {word_count()}",
        f"longest title: {longest} ({len(longest)} characters)",
    ]
    if include_stretch:
        oldest, newest = oldest_and_newest()
        lines.append(f"oldest: {TITLES[oldest]} ({YEARS[oldest]})")
        lines.append(f"newest: {TITLES[newest]} ({YEARS[newest]})")
    return lines
