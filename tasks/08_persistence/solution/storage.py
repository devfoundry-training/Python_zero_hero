# ============================================================
# Task 08 - storage: CSV and JSON in and out
# ============================================================
# Loading never crashes on bad data. A bad line is reported as
# "line N: reason" and skipped; the good lines still load.
# ============================================================

import csv
import re
import json
from pathlib import Path
from typing import Any, Final

from library import Book, Library, Member, make_book

BOOK_FIELDS: Final[list[str]] = ["id", "title", "author", "year", "genre", "copies", "format", "length"]
MEMBER_FIELDS: Final[list[str]] = ["id", "name", "email", "type", "joined"]


class LoadResult:
    """What a load produced: the good rows and the problems."""

    def __init__(self) -> None:
        self.books: list[Book] = []
        self.members: list[Member] = []
        self.loans: list[tuple[int, int]] = []  # (member id, book id) from JSON
        self.problems: list[str] = []
        self.skipped = 0

    def skip(self, line_number: int, reason: str) -> None:
        self.problems.append(f"line {line_number}: {reason}")
        self.skipped += 1


def whole_number(text: str, name: str) -> int:
    """Digits with an optional minus sign, nothing else. int() alone
    would also accept ' 4', '+4' and '4_000', which other languages
    reject, so we check the shape first."""
    if re.fullmatch(r"-?[0-9]+", text) is None:
        raise ValueError(f"{name} must be a whole number, got '{text}'")
    return int(text)


# ------------------------------------------------------------
# Reading CSV
# ------------------------------------------------------------
# newline="" is what the csv module asks for: it handles \n and
# \r\n itself. encoding="utf-8" so the same file reads the same
# on every machine.

def load_books_csv(path: Path) -> LoadResult:
    """Raises FileNotFoundError when the file is missing."""
    result = LoadResult()
    seen: set[int] = set()
    with path.open(encoding="utf-8", newline="") as file:
        for line_number, row in enumerate(csv.reader(file), start=1):
            if line_number == 1 or not row:  # header, or a blank line
                continue
            if len(row) != len(BOOK_FIELDS):
                result.skip(line_number, f"expected {len(BOOK_FIELDS)} fields, found {len(row)}")
                continue
            try:
                for index, name in ((0, "id"), (3, "year"), (5, "copies"), (7, "length")):
                    whole_number(row[index], name)
                book = make_book(row)
            except ValueError as error:
                result.skip(line_number, str(error))
                continue
            if book.id in seen:
                result.skip(line_number, f"duplicate book id {book.id}")
                continue
            seen.add(book.id)
            result.books.append(book)
    return result


def load_members_csv(path: Path) -> LoadResult:
    result = LoadResult()
    seen: set[int] = set()
    with path.open(encoding="utf-8", newline="") as file:
        for line_number, row in enumerate(csv.reader(file), start=1):
            if line_number == 1 or not row:
                continue
            if len(row) != len(MEMBER_FIELDS):
                result.skip(line_number, f"expected {len(MEMBER_FIELDS)} fields, found {len(row)}")
                continue
            try:
                member = Member(whole_number(row[0], "id"), row[1], row[2], row[3], row[4])
            except ValueError as error:
                result.skip(line_number, str(error))
                continue
            if member.id in seen:
                result.skip(line_number, f"duplicate member id {member.id}")
                continue
            seen.add(member.id)
            result.members.append(member)
    return result


# ------------------------------------------------------------
# Writing CSV and JSON
# ------------------------------------------------------------

def book_row(book: Book) -> list[Any]:
    return [book.id, book.title, book.author, book.year, book.genre, book.copies, book.format_name, book.length]


def book_dict(book: Book) -> dict[str, Any]:
    return dict(zip(BOOK_FIELDS, book_row(book)))


def member_dict(member: Member) -> dict[str, Any]:
    return {
        "id": member.id,
        "name": member.name,
        "email": member.email,
        "type": member.type,
        "joined": member.joined,
        "loans": list(member.loans),
    }


def save_books_csv(library: Library, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # lineterminator="\n": the same bytes on Windows, macOS and Linux
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(BOOK_FIELDS)
        for book in library.all_books():
            writer.writerow(book_row(book))


def save_json(library: Library, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "books": [book_dict(b) for b in library.all_books()],
        "members": [member_dict(m) for m in library.all_members()],
    }
    with path.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(document, file, indent=2, ensure_ascii=False)
        file.write("\n")


def load_json(path: Path) -> LoadResult:
    """Raises FileNotFoundError, or ValueError for broken JSON."""
    with path.open(encoding="utf-8") as file:
        try:
            document = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("not valid JSON") from None
    result = LoadResult()
    try:
        for item in document["books"]:
            result.books.append(make_book([str(item[name]) for name in BOOK_FIELDS]))
        for item in document["members"]:
            result.members.append(Member(item["id"], item["name"], item["email"], item["type"], item["joined"]))
            result.loans.extend((item["id"], book_id) for book_id in item.get("loans", []))
    except (KeyError, TypeError):
        raise ValueError("not a library file") from None
    return result


def build_library(result: LoadResult) -> Library:
    library = Library()
    for book in result.books:
        library.add_book(book)
    for member in result.members:
        library.add_member(member)
    # Saved loans go back through borrow(), so the copy counts and
    # the limits are checked exactly as if they were new loans
    for member_id, book_id in result.loans:
        library.borrow(member_id, book_id)
    return library
