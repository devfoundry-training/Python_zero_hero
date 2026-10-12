# ============================================================
# Task 10 - SQLite storage (starter)
# ============================================================
# Session 10: databases. Builds on task 09 (library.py and
# storage.py are the task 09 solution). The CSV files are
# imported once into out/library.db (rebuilt on every run from
# data/schema.sql); from then on the database is the store. The
# SQL goes in db.py; the steps of the run go here (see README.md).
#
# Run from the repo root:
#   python tasks/10_sqlite/starter/main.py tasks/data [TODAY]
# Check it:
#   python tasks/check/check.py 10 -- python tasks/10_sqlite/starter/main.py tasks/data
# ============================================================

import sys
from datetime import date
from pathlib import Path
from typing import Final

from db import LibraryDb
from storage import LoadResult, load_books_csv, load_loans_csv, load_members_csv

DEFAULT_TODAY: Final[date] = date(2026, 10, 12)
DB_PATH: Final[Path] = Path("out") / "library.db"


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    data = Path(args[0]) if len(args) > 0 else Path("tasks/data")
    today = date.fromisoformat(args[1]) if len(args) > 1 else DEFAULT_TODAY

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.unlink(missing_ok=True)  # start clean so every run is the same
    db = LibraryDb(DB_PATH)
    try:
        # Core 2: create the tables
        db.create(data / "schema.sql")
        print("Created out/library.db from schema.sql")

        # Core 3: import the CSV files
        rows = LoadResult()
        load_books_csv(data / "books.csv", rows)
        load_members_csv(data / "members.csv", rows)
        load_loans_csv(data / "loans.csv", rows)
        db.import_rows(rows)
        print(f"Imported {db.count('books')} books, {db.count('members')} members, {db.count('loans')} loans")

        # TODO Core 4: the four questions, answered in SQL
        # TODO Core 5: load the model from the database and run the
        #   task 09 actions on today's date, saving each success
        # TODO Core 6: load the model again and print the counts and
        #   the task 09 overdue report
        raise NotImplementedError(f"not implemented: the questions and new loans on {today.isoformat()}")
    finally:
        db.close()


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as error:
        print(error)  # the first piece still to write
