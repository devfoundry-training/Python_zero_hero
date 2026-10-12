# ============================================================
# Task 10 - SQLite storage (solution, Core + Stretch)
# ============================================================
# Session 10: databases. Builds on task 09: the CSV files are
# imported once into out/library.db (rebuilt on every run from
# data/schema.sql), and from then on the database is the store.
#
# Run from the repo root:
#   python tasks/10_sqlite/solution/main.py DATA_DIR [TODAY]             (Core, checked)
#   python tasks/10_sqlite/solution/main.py DATA_DIR [TODAY] --stretch   (Core, then Stretch)
# ============================================================

import sys
from datetime import date
from pathlib import Path
from typing import Final

from db import LibraryDb
from library import Library, LibraryError, format_money, plural
from storage import LoadResult, load_books_csv, load_loans_csv, load_members_csv

DEFAULT_TODAY: Final[date] = date(2026, 10, 12)
DB_PATH: Final[Path] = Path("out") / "library.db"


def overdue_report(library: Library, today: date) -> None:
    """Exactly the task 09 report, now fed from the database."""
    overdue = library.overdue(today)
    print(f"Overdue on {today.isoformat()}: {plural(len(overdue), 'loan', 'loans')}")
    for loan in overdue:
        book = library.book(loan.book_id)
        member = library.member(loan.member_id)
        print(f"{plural(library.days_late(loan, today), 'day', 'days')}: {book.title}, {member.name} ({member.type}), "
              f"due {library.due_date(loan).isoformat()}, fine {format_money(library.fine(loan, today))}")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    data = Path(args[0]) if len(args) > 0 else Path("tasks/data")
    today = date.fromisoformat(args[1]) if len(args) > 1 else DEFAULT_TODAY

    # ------------------------------------------------------------
    # Core 1: a fresh database from schema.sql, filled from the CSVs
    # ------------------------------------------------------------
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.unlink(missing_ok=True)  # start clean so every run is the same
    db = LibraryDb(DB_PATH)
    try:
        db.create(data / "schema.sql")
        print("Created out/library.db from schema.sql")
        rows = LoadResult()
        load_books_csv(data / "books.csv", rows)
        load_members_csv(data / "members.csv", rows)
        load_loans_csv(data / "loans.csv", rows)
        db.import_rows(rows)
        print(f"Imported {db.count('books')} books, {db.count('members')} members, {db.count('loans')} loans")

        # ------------------------------------------------------------
        # Core 2: questions answered in SQL
        # ------------------------------------------------------------
        print("Books per genre")
        for genre, count in db.genre_counts():
            print(f"{genre}: {count}")

        print("Nothing on the shelf")
        for book_id, title, available, copies in db.unavailable_books():
            print(f"#{book_id} {title}: {available} of {copies} available")

        for text in ("the", "x' OR '1'='1"):
            found = db.search_titles(text)
            print(f'Search "{text}": {plural(len(found), "book", "books")}')
            for book_id, title, year in found:
                print(f"  #{book_id} {title} ({year})")

        print("Open loans per member")
        for member_id, name, count in db.open_loans_per_member():
            print(f"#{member_id} {name}: {count}")

        # ------------------------------------------------------------
        # Core 3: the task 09 rules decide, the database remembers
        # ------------------------------------------------------------
        library = db.load_library()
        print(f"New loans on {today.isoformat()}")
        for action, member_id, book_id in [("borrow", 105, 15), ("borrow", 105, 16), ("return", 102, 14)]:
            try:
                if action == "borrow":
                    loan = library.borrow(member_id, book_id, today)
                    db.insert_loan(loan)
                    print(f"OK: {library.member(member_id).name} borrowed {library.book(book_id).title}, "
                          f"due {library.due_date(loan).isoformat()}, saved as loan {loan.id}")
                else:
                    loan = library.return_book(member_id, book_id, today)
                    db.mark_returned(loan)
                    print(f"OK: {library.member(member_id).name} returned {library.book(book_id).title}, "
                          f"fine {format_money(library.fine(loan, today))}, saved")
            except LibraryError as error:
                print(f"Error: {error}")

        # Read everything back from the database to prove it was saved
        reloaded = db.load_library()
        open_loans = sum(1 for x in reloaded.all_loans() if x.is_open)
        print(f"Reloaded: {reloaded.book_count} books, {reloaded.member_count} members, "
              f"{reloaded.loan_count} loans ({open_loans} open)")
        overdue_report(reloaded, today)

        # ------------------------------------------------------------
        # Stretch: a borrow that rolls back
        # ------------------------------------------------------------
        if "--stretch" in sys.argv:
            print("Stretch")
            before = db.count("loans")
            refused = db.borrow_in_transaction(101, 3, today)
            print(f"borrow 101 3 in a transaction: {'refused, rolled back' if refused is None else 'OK'}")
            print(f"loans before {before}, after {db.count('loans')}")
            new_id = db.borrow_in_transaction(101, 4, today)
            print(f"borrow 101 4 in a transaction: saved as loan {new_id}")
            db.add_member_index()
            print(f"indexes on loans: {', '.join(db.indexes_on('loans'))}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
