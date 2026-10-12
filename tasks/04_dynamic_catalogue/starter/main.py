# ============================================================
# Task 04 - Dynamic catalogue (starter)
# ============================================================
# Session 4: collections. Builds on task 03: the fixed shelf of
# 10 becomes a list of all 20 books, plus a dict and a set. The
# data, the record type and plural() from task 03 are here; fill
# in each Core step (see README.md).
#
# Run from the repo root:
#   python tasks/04_dynamic_catalogue/starter/main.py
# Check it:
#   python tasks/check/check.py 04 -- python tasks/04_dynamic_catalogue/starter/main.py
# ============================================================

from typing import Final, NamedTuple

# ------------------------------------------------------------
# The data: the lines of data/books.csv, copied in
# ------------------------------------------------------------
# Reading files comes in task 08. Until then the program carries
# its own copy of the CSV lines, header first.

BOOK_LINES: Final[list[str]] = [
    "id,title,author,year,genre,copies,format,length",
    "1,Pride and Prejudice,Jane Austen,1813,Classic,3,print,432",
    "2,Nineteen Eighty-Four,George Orwell,1949,Dystopian,2,print,328",
    "3,The Hobbit,J. R. R. Tolkien,1937,Fantasy,0,print,310",
    "4,Dune,Frank Herbert,1965,Science Fiction,4,print,412",
    "5,Robinson Crusoe,Daniel Defoe,1719,Adventure,1,print,320",
    "6,The Time Machine,H. G. Wells,1895,Science Fiction,2,ebook,118",
    "7,Animal Farm,George Orwell,1945,Dystopian,5,print,112",
    "8,Emma,Jane Austen,1815,Classic,1,audio,1150",
    "9,The Left Hand of Darkness,Ursula K. Le Guin,1969,Science Fiction,0,print,304",
    "10,Murder on the Orient Express,Agatha Christie,1934,Crime,2,print,256",
    "11,The Murder of Roger Ackroyd,Agatha Christie,1926,Crime,1,ebook,312",
    "12,A Wizard of Earthsea,Ursula K. Le Guin,1968,Fantasy,2,print,183",
    "13,Brave New World,Aldous Huxley,1932,Dystopian,2,audio,480",
    "14,The Martian,Andy Weir,2011,Science Fiction,3,print,369",
    "15,Small Island,Andrea Levy,2004,Historical,1,print,441",
    "16,Wolf Hall,Hilary Mantel,2009,Historical,2,audio,1440",
    "17,The Remains of the Day,Kazuo Ishiguro,1989,Literary,2,print,258",
    "18,Never Let Me Go,Kazuo Ishiguro,2005,Literary,1,ebook,288",
    "19,Frankenstein,Mary Shelley,1818,Gothic,2,print,280",
    "20,The War of the Worlds,H. G. Wells,1898,Science Fiction,3,audio,410",
]

# The borrowing script: (action, book id), applied in order
ACTIONS: Final[list[tuple[str, int]]] = [
    ("borrow", 1),
    ("borrow", 1),
    ("borrow", 4),
    ("return", 1),
    ("borrow", 3),
    ("borrow", 7),
    ("return", 9),
    ("borrow", 1),
]


class Book(NamedTuple):
    """One row of books.csv: a record with field names, no behaviour."""

    id: int
    title: str
    author: str
    year: int
    genre: str
    copies: int
    format: str
    length: int


def plural(count: int, singular: str, many: str) -> str:
    """'1 book' or '4 books' (from task 03)."""
    return f"{count} {singular if count == 1 else many}"


def by_name(text: str) -> str:
    """Sort key for A-Z ignoring case, compared character by character."""
    return text.lower()


def parse_book(line: str) -> Book:
    """TODO Core 1: split the line on commas and build a Book."""
    raise NotImplementedError("not implemented: parse_book")


# ------------------------------------------------------------
# Core 1: load every line into a list
# ------------------------------------------------------------
# TODO: parse every data line (skip the header) into a list,
# then print "Loaded N books"
print("Loaded: not implemented")

# ------------------------------------------------------------
# Core 2: index by genre (dict of genre -> list of titles)
# ------------------------------------------------------------
print("Genres: not implemented")

# ------------------------------------------------------------
# Core 3: unique authors (a set)
# ------------------------------------------------------------
print("Authors: not implemented")

# ------------------------------------------------------------
# Core 4 and 5: borrow and return, counted in dicts by book id
# ------------------------------------------------------------
print("Borrowing: not implemented")
print("Counts: not implemented")
