# ============================================================
# Task 08 starter - storage: CSV and JSON in and out
# ============================================================
# Loading must never crash on bad data. A bad line is reported as
# "line N: reason" and skipped; the good lines still load.
# Every function below is yours to write (see README.md).
# ============================================================

import csv
import json
import re
from pathlib import Path
from typing import Final

from library import Book, Library, Member, make_book

BOOK_FIELDS: Final[list[str]] = ["id", "title", "author", "year", "genre", "copies", "format", "length"]
MEMBER_FIELDS: Final[list[str]] = ["id", "name", "email", "type", "joined"]


class LoadResult:
    """What a load produced: the good rows and the problems."""

    def __init__(self) -> None:
        self.books: list[Book] = []
        self.members: list[Member] = []
        self.problems: list[str] = []
        self.skipped = 0

    def skip(self, line_number: int, reason: str) -> None:
        self.problems.append(f"line {line_number}: {reason}")
        self.skipped += 1


def whole_number(text: str, name: str) -> int:
    """Digits with an optional minus sign, nothing else, or ValueError
    "NAME must be a whole number, got 'TEXT'"."""
    raise NotImplementedError("not implemented: whole_number")


# ------------------------------------------------------------
# Reading CSV (TODO)
# ------------------------------------------------------------
# Open with encoding="utf-8", newline="" and use csv.reader.

def load_books_csv(path: Path) -> LoadResult:
    """Raises FileNotFoundError when the file is missing. Checks each
    line in the order the brief gives and skips the bad ones."""
    raise NotImplementedError("not implemented: load_books_csv")


def load_members_csv(path: Path) -> LoadResult:
    raise NotImplementedError("not implemented: load_members_csv")


# ------------------------------------------------------------
# Writing CSV and JSON (TODO)
# ------------------------------------------------------------

def save_books_csv(library: Library, path: Path) -> None:
    """Same header and columns as data/books.csv, "\\n" line endings."""
    raise NotImplementedError("not implemented: save_books_csv")


def save_json(library: Library, path: Path) -> None:
    """The shape in README.md, two-space indent, keys in that order."""
    raise NotImplementedError("not implemented: save_json")


def build_library(result: LoadResult) -> Library:
    """A Library holding everything a load produced."""
    raise NotImplementedError("not implemented: build_library")
