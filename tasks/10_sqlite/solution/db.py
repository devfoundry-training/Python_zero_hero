# ============================================================
# Task 10 - db: the library in SQLite
# ============================================================
# Every query uses ? placeholders and passes the values
# separately. The database driver keeps the values apart from the
# SQL text, so a title like  x' OR '1'='1  is only ever data.
# Never build SQL by joining strings with user input.
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

    # --- setting up ---------------------------------------------

    def create(self, schema: Path) -> None:
        """Run schema.sql: it drops and recreates every table."""
        self.conn.executescript(schema.read_text(encoding="utf-8"))

    def import_rows(self, result: LoadResult) -> None:
        """Copy loaded CSV rows into the tables, in one transaction."""
        with self.conn:  # commits at the end, rolls back on an error
            self.conn.executemany(
                "INSERT INTO books (id, title, author, year, genre, copies, format, length) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [(b.id, b.title, b.author, b.year, b.genre, b.copies, b.format_name, b.length) for b in result.books])
            self.conn.executemany(
                "INSERT INTO members (id, name, email, type, joined) VALUES (?, ?, ?, ?, ?)",
                [(m.id, m.name, m.email, m.type, m.joined) for m in result.members])
            self.conn.executemany(
                "INSERT INTO loans (id, book_id, member_id, borrowed, returned) VALUES (?, ?, ?, ?, ?)",
                [(x.id, x.book_id, x.member_id, x.borrowed.isoformat(),
                  x.returned.isoformat() if x.returned else None) for x in result.loans])

    def count(self, table: str) -> int:
        # A table name cannot be a ? parameter, so it is checked
        # against a fixed list instead of trusted
        if table not in ("books", "members", "loans"):
            raise ValueError(f"unknown table {table}")
        return self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    # --- queries ---------------------------------------------------

    def genre_counts(self) -> list[tuple[str, int]]:
        return self.conn.execute(
            "SELECT genre, COUNT(*) FROM books GROUP BY genre ORDER BY genre").fetchall()

    def unavailable_books(self) -> list[tuple[int, str, int, int]]:
        """(id, title, available, copies) for books with nothing on the shelf."""
        return self.conn.execute(
            """SELECT b.id, b.title, b.copies - COUNT(l.id) AS available, b.copies
               FROM books b
               LEFT JOIN loans l ON l.book_id = b.id AND l.returned IS NULL
               GROUP BY b.id, b.title, b.copies
               HAVING b.copies - COUNT(l.id) = 0
               ORDER BY b.id""").fetchall()

    def search_titles(self, text: str) -> list[tuple[int, str, int]]:
        # The % wildcards go into the value, not into the SQL
        return self.conn.execute(
            "SELECT id, title, year FROM books WHERE LOWER(title) LIKE ? ORDER BY id",
            (f"%{text.lower()}%",)).fetchall()

    def open_loans_per_member(self) -> list[tuple[int, str, int]]:
        return self.conn.execute(
            """SELECT m.id, m.name, COUNT(l.id)
               FROM members m
               LEFT JOIN loans l ON l.member_id = m.id AND l.returned IS NULL
               GROUP BY m.id, m.name
               ORDER BY m.id""").fetchall()

    # --- loading the model and saving changes -----------------------

    def load_library(self) -> Library:
        library = Library()
        for row in self.conn.execute(
                "SELECT id, title, author, year, genre, copies, format, length FROM books ORDER BY id"):
            library.add_book(make_book([str(value) for value in row]))
        for row in self.conn.execute("SELECT id, name, email, type, joined FROM members ORDER BY id"):
            library.add_member(Member(*row))
        for loan_id, book_id, member_id, borrowed, returned in self.conn.execute(
                "SELECT id, book_id, member_id, borrowed, returned FROM loans ORDER BY id"):
            library.add_loan(Loan(loan_id, book_id, member_id, date.fromisoformat(borrowed),
                                  date.fromisoformat(returned) if returned else None))
        return library

    def insert_loan(self, loan: Loan) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO loans (id, book_id, member_id, borrowed, returned) VALUES (?, ?, ?, ?, NULL)",
                (loan.id, loan.book_id, loan.member_id, loan.borrowed.isoformat()))

    def mark_returned(self, loan: Loan) -> None:
        if loan.returned is None:
            raise ValueError("loan has not been returned")
        with self.conn:
            self.conn.execute("UPDATE loans SET returned = ? WHERE id = ?", (loan.returned.isoformat(), loan.id))

    # --- Stretch: the whole borrow inside one transaction ----------

    def borrow_in_transaction(self, member_id: int, book_id: int, today: date) -> int | None:
        """Insert the loan first, then check stock in SQL. If the check
        fails the transaction rolls back and the insert disappears.
        Returns the new loan id, or None when refused."""
        try:
            with self.conn:
                new_id = self.conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM loans").fetchone()[0]
                self.conn.execute(
                    "INSERT INTO loans (id, book_id, member_id, borrowed, returned) VALUES (?, ?, ?, ?, NULL)",
                    (new_id, book_id, member_id, today.isoformat()))
                out = self.conn.execute(
                    "SELECT COUNT(*) FROM loans WHERE book_id = ? AND returned IS NULL", (book_id,)).fetchone()[0]
                copies = self.conn.execute("SELECT copies FROM books WHERE id = ?", (book_id,)).fetchone()[0]
                if out > copies:
                    raise RuntimeError("no copies available")  # leaving the with block rolls back
                return new_id
        except RuntimeError:
            return None

    # --- Stretch 2: an index for the member lookups -----------------

    def add_member_index(self) -> None:
        """Without an index, finding one member's loans means reading
        every row of loans. The index on loans(member_id) lets SQLite
        jump straight to that member's rows: it helps the LEFT JOIN in
        open_loans_per_member() and any "loans for member N" query.
        It costs a little on every INSERT, which is fine here."""
        with self.conn:
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_loans_member ON loans (member_id)")

    def indexes_on(self, table: str) -> list[str]:
        """Names of the indexes SQLite holds for a table."""
        return [row[0] for row in self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'index' AND tbl_name = ? ORDER BY name", (table,))]
