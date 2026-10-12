# ============================================================
# Task 04 - Dynamic catalogue (solution, Core + Stretch)
# ============================================================
# Session 4: collections. Builds on task 03: the fixed shelf of
# 10 becomes a list of all 20 books, plus a dict and a set.
#
# Run from the repo root:
#   python tasks/04_dynamic_catalogue/solution/main.py             (Core output, checked)
#   python tasks/04_dynamic_catalogue/solution/main.py --stretch   (Core, then the Stretch)
# ============================================================

import sys
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
    """One row of books.csv. A NamedTuple is a tuple with field
    names: a record with no behaviour (classes come in task 05)."""

    id: int
    title: str
    author: str
    year: int
    genre: str
    copies: int
    format: str
    length: int


def parse_book(line: str) -> Book:
    f = line.split(",")
    return Book(int(f[0]), f[1], f[2], int(f[3]), f[4], int(f[5]), f[6], int(f[7]))


def by_name(text: str) -> str:
    """Sort key for A-Z ignoring case, compared character by character."""
    return text.lower()


# ------------------------------------------------------------
# Core 1: load every line into a list
# ------------------------------------------------------------

books: list[Book] = []
for line in BOOK_LINES[1:]:  # [1:] skips the header row
    books.append(parse_book(line))
print(f"Loaded {len(books)} books")

# ------------------------------------------------------------
# Core 2: index by genre (dict of genre -> list of titles)
# ------------------------------------------------------------

by_genre: dict[str, list[str]] = {}
for book in books:
    by_genre.setdefault(book.genre, []).append(book.title)

print(f"Genres ({len(by_genre)})")
for genre in sorted(by_genre, key=by_name):
    titles = by_genre[genre]
    print(f"{genre} ({len(titles)}): {', '.join(titles)}")

# ------------------------------------------------------------
# Core 3: unique authors (a set drops the duplicates for us)
# ------------------------------------------------------------

authors: set[str] = {book.author for book in books}
print(f"Authors ({len(authors)} unique across {len(books)} books)")
for author in sorted(authors, key=by_name):
    print(author)

# ------------------------------------------------------------
# Core 4: borrow and return, counted in dicts keyed by book id
# ------------------------------------------------------------

catalogue: dict[int, Book] = {book.id: book for book in books}
on_loan: dict[int, int] = {}
borrowed_count: dict[int, int] = {}
returned_count: dict[int, int] = {}
borrows = returns = refused = 0

print("Borrowing")
for action, book_id in ACTIONS:
    book = catalogue[book_id]
    out = on_loan.get(book_id, 0)
    if action == "borrow":
        if out < book.copies:
            on_loan[book_id] = out + 1
            borrowed_count[book_id] = borrowed_count.get(book_id, 0) + 1
            borrows += 1
            print(f"borrow {book_id}: OK, {book.copies - out - 1} left")
        else:
            refused += 1
            print(f"borrow {book_id}: refused, none available")
    else:
        if out > 0:
            on_loan[book_id] = out - 1
            returned_count[book_id] = returned_count.get(book_id, 0) + 1
            returns += 1
            print(f"return {book_id}: OK, {book.copies - out + 1} left")
        else:
            refused += 1
            print(f"return {book_id}: refused, none on loan")

print("Counts")
print(f"borrows: {borrows}")
print(f"returns: {returns}")
print(f"refused: {refused}")
for book_id in sorted(borrowed_count):
    print(f"book {book_id}: borrowed {borrowed_count[book_id]}, returned {returned_count.get(book_id, 0)}")

# ------------------------------------------------------------
# Stretch: busy authors, books per decade, the biggest genre
# ------------------------------------------------------------

if "--stretch" in sys.argv:
    print("Stretch")

    per_author: dict[str, int] = {}
    for book in books:
        per_author[book.author] = per_author.get(book.author, 0) + 1
    busy = [a for a in sorted(per_author, key=by_name) if per_author[a] > 1]
    print(f"Authors with more than one book: {', '.join(busy)}")

    per_decade: dict[int, int] = {}
    for book in books:
        decade = book.year // 10 * 10  # 1813 -> 1810
        per_decade[decade] = per_decade.get(decade, 0) + 1
    for decade in sorted(per_decade):
        print(f"{decade}s: {per_decade[decade]}")

    # Most books wins; a tie goes to the genre first in A-Z order
    biggest = ""
    for genre in sorted(by_genre, key=by_name):
        if biggest == "" or len(by_genre[genre]) > len(by_genre[biggest]):
            biggest = genre
    print(f"Biggest genre: {biggest} ({len(by_genre[biggest])} books)")
