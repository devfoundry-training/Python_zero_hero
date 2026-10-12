# ============================================================
# Task 09 - Loans with due dates (starter)
# ============================================================
# Session 9: dates and times. Builds on task 08 (library.py and
# storage.py are the task 08 solution plus the Loan record).
# "Today" is an input, never the real clock, so the output is the
# same whenever and wherever it runs.
#
# Run from the repo root:
#   python tasks/09_due_dates/starter/main.py tasks/data [TODAY]
# Check it:
#   python tasks/check/check.py 09 -- python tasks/09_due_dates/starter/main.py tasks/data
# ============================================================

import sys
from datetime import date
from pathlib import Path
from typing import Final

from library import Library
from storage import load_all

DEFAULT_TODAY: Final[date] = date(2026, 10, 12)


def loans_table(library: Library, today: date) -> None:
    raise NotImplementedError("not implemented: loans_table")


def overdue_report(library: Library, today: date) -> None:
    raise NotImplementedError("not implemented: overdue_report")


def fines_report(library: Library, today: date) -> None:
    raise NotImplementedError("not implemented: fines_report")


def new_loans(library: Library, today: date) -> None:
    """105 borrows 15, 105 borrows 16, 102 returns 14, on today's date."""
    raise NotImplementedError("not implemented: new_loans")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    data = Path(args[0]) if len(args) > 0 else Path("tasks/data")
    today = date.fromisoformat(args[1]) if len(args) > 1 else DEFAULT_TODAY

    print(f"Today is {today.isoformat()}")
    library = load_all(data)
    loans_table(library, today)
    overdue_report(library, today)
    fines_report(library, today)
    new_loans(library, today)


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as error:
        print(error)  # the first piece still to write
