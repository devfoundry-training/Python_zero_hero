# ============================================================
# Task 10 starter - db: the library in SQLite
# ============================================================
# Every query uses ? placeholders and passes the values
# separately. Never build SQL by joining strings with values.
# Every method that raises NotImplementedError is yours to write.
# ============================================================

import sqlite3
from datetime import date
from pathlib import Path

from library import Library, Loan, Member, make_book
from storage import LoadResult


class LibraryDb:
    def __init__(self, path: Path) -> None:
        self.conn = sqlite3.connect(path)
        # SQLite ignores FOREIGN KEY rules unless this is switched on
        self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self) -> None:
        self.conn.close()

    # --- setting up (Core 2 and 3) -----------------------------------

    def create(self, schema: Path) -> None:
        """Run schema.sql (conn.executescript runs the whole file)."""
        raise NotImplementedError("not implemented: LibraryDb.create")

    def import_rows(self, result: LoadResult) -> None:
        """Insert the loaded CSV rows in one transaction (with self.conn:)."""
        raise NotImplementedError("not implemented: LibraryDb.import_rows")

    def count(self, table: str) -> int:
        """SELECT COUNT(*) for books, members or loans."""
        raise NotImplementedError("not implemented: LibraryDb.count")

    # --- queries (Core 4), one SQL statement each ---------------------

    def genre_counts(self) -> list[tuple[str, int]]:
        raise NotImplementedError("not implemented: LibraryDb.genre_counts")

    def unavailable_books(self) -> list[tuple[int, str, int, int]]:
        """(id, title, available, copies) for books with nothing on the shelf."""
        raise NotImplementedError("not implemented: LibraryDb.unavailable_books")

    def search_titles(self, text: str) -> list[tuple[int, str, int]]:
        """(id, title, year): LOWER(title) LIKE ?, with the % inside the value."""
        raise NotImplementedError("not implemented: LibraryDb.search_titles")

    def open_loans_per_member(self) -> list[tuple[int, str, int]]:
        raise NotImplementedError("not implemented: LibraryDb.open_loans_per_member")

    # --- the model in and out (Core 5 and 6) --------------------------

    def load_library(self) -> Library:
        """Build the task 09 model from the tables (not from the CSV files)."""
        raise NotImplementedError("not implemented: LibraryDb.load_library")

    def insert_loan(self, loan: Loan) -> None:
        raise NotImplementedError("not implemented: LibraryDb.insert_loan")

    def mark_returned(self, loan: Loan) -> None:
        raise NotImplementedError("not implemented: LibraryDb.mark_returned")
