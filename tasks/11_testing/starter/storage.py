# ============================================================
# Task 11 - storage (unchanged from task 09, used by the Stretch tests)
# ============================================================
# The task 08 CSV loaders plus loans.csv (saving is unchanged
# from task 08 and left out here). Dates are text in the
# files (YYYY-MM-DD) and date objects in the program; the
# conversion happens here and nowhere else.
# ============================================================

import csv
import re
from datetime import date
from pathlib import Path
from typing import Final

from library import Book, Library, Loan, Member, make_book

BOOK_FIELDS: Final[list[str]] = ["id", "title", "author", "year", "genre", "copies", "format", "length"]
MEMBER_FIELDS: Final[list[str]] = ["id", "name", "email", "type", "joined"]
LOAN_FIELDS: Final[list[str]] = ["id", "book_id", "member_id", "borrowed", "returned"]


class LoadResult:
    def __init__(self) -> None:
        self.books: list[Book] = []
        self.members: list[Member] = []
        self.loans: list[Loan] = []
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


def parse_date(text: str, name: str) -> date:
    """'2026-10-12' -> date(2026, 10, 12)."""
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise ValueError(f"{name} must be a date YYYY-MM-DD, got '{text}'") from None


def read_rows(path: Path, width: int, result: LoadResult) -> list[tuple[int, list[str]]]:
    """(line number, fields) for every data row with the right width.
    Rows with the wrong width are reported and skipped."""
    rows: list[tuple[int, list[str]]] = []
    with path.open(encoding="utf-8", newline="") as file:
        for line_number, row in enumerate(csv.reader(file), start=1):
            if line_number == 1 or not row:
                continue
            if len(row) != width:
                result.skip(line_number, f"expected {width} fields, found {len(row)}")
                continue
            rows.append((line_number, row))
    return rows


def load_books_csv(path: Path, result: LoadResult | None = None) -> LoadResult:
    result = result or LoadResult()
    seen: set[int] = set()
    for line_number, row in read_rows(path, len(BOOK_FIELDS), result):
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


def load_members_csv(path: Path, result: LoadResult | None = None) -> LoadResult:
    result = result or LoadResult()
    for line_number, row in read_rows(path, len(MEMBER_FIELDS), result):
        try:
            parse_date(row[4], "joined")
            result.members.append(Member(whole_number(row[0], "id"), row[1], row[2], row[3], row[4]))
        except ValueError as error:
            result.skip(line_number, str(error))
    return result


def load_loans_csv(path: Path, result: LoadResult | None = None) -> LoadResult:
    result = result or LoadResult()
    for line_number, row in read_rows(path, len(LOAN_FIELDS), result):
        try:
            returned = parse_date(row[4], "returned") if row[4] != "" else None  # optional date
            result.loans.append(Loan(whole_number(row[0], "id"), whole_number(row[1], "book_id"),
                                     whole_number(row[2], "member_id"), parse_date(row[3], "borrowed"), returned))
        except ValueError as error:
            result.skip(line_number, str(error))
    return result


def build_library(result: LoadResult) -> Library:
    library = Library()
    for book in result.books:
        library.add_book(book)
    for member in result.members:
        library.add_member(member)
    for loan in result.loans:
        library.add_loan(loan)
    return library


def load_all(data: Path) -> Library:
    """books.csv, members.csv and loans.csv from one folder."""
    result = LoadResult()
    load_books_csv(data / "books.csv", result)
    load_members_csv(data / "members.csv", result)
    load_loans_csv(data / "loans.csv", result)
    return build_library(result)

