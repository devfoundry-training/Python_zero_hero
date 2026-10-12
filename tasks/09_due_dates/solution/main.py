# ============================================================
# Task 09 - Loans with due dates (solution, Core + Stretch)
# ============================================================
# Session 9: dates and times. Builds on task 08.
# "Today" is an input, never the real clock, so the output is the
# same whenever and wherever it runs.
#
# Run from the repo root:
#   python tasks/09_due_dates/solution/main.py DATA_DIR [TODAY]             (Core, checked)
#   python tasks/09_due_dates/solution/main.py DATA_DIR [TODAY] --stretch   (Core, then Stretch)
# DATA_DIR defaults to tasks/data, TODAY to 2026-10-12.
# ============================================================

import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Final

from library import Library, LibraryError, format_money, plural
from storage import load_all

DEFAULT_TODAY: Final[date] = date(2026, 10, 12)


def loans_table(library: Library, today: date) -> None:
    print("Loans")
    print(f"{'ID':>2}  {'Book':<30}  {'Member':<12}  {'Borrowed':<10}  {'Due':<10}  Status")
    print(f"{'-' * 2}  {'-' * 30}  {'-' * 12}  {'-' * 10}  {'-' * 10}  {'-' * 6}")
    for loan in library.all_loans():
        book = library.book(loan.book_id)
        member = library.member(loan.member_id)
        # date.isoformat() is always YYYY-MM-DD
        print(f"{loan.id:>2}  {book.title:<30}  {member.name:<12}  {loan.borrowed.isoformat()}  "
              f"{library.due_date(loan).isoformat()}  {library.status(loan, today)}")


def overdue_report(library: Library, today: date) -> None:
    overdue = library.overdue(today)
    print(f"Overdue on {today.isoformat()}: {plural(len(overdue), 'loan', 'loans')}")
    for loan in overdue:
        book = library.book(loan.book_id)
        member = library.member(loan.member_id)
        print(f"{plural(library.days_late(loan, today), 'day', 'days')}: {book.title}, {member.name} ({member.type}), "
              f"due {library.due_date(loan).isoformat()}, fine {format_money(library.fine(loan, today))}")


def fines_report(library: Library, today: date) -> None:
    on_overdue = sum(library.fine(x, today) for x in library.all_loans() if x.is_open)
    on_returns = sum(library.fine(x, today) for x in library.all_loans() if not x.is_open)
    print("Fines")
    print(f"on overdue loans: {format_money(on_overdue)}")
    print(f"on late returns: {format_money(on_returns)}")


def new_loans(library: Library, today: date) -> None:
    print(f"New loans on {today.isoformat()}")
    for action, member_id, book_id in [("borrow", 105, 15), ("borrow", 105, 16), ("return", 102, 14)]:
        try:
            if action == "borrow":
                loan = library.borrow(member_id, book_id, today)
                print(f"OK: {library.member(member_id).name} borrowed {library.book(book_id).title}, "
                      f"due {library.due_date(loan).isoformat()}")
            else:
                loan = library.return_book(member_id, book_id, today)
                late = library.days_late(loan, today)
                tail = "on time" if late == 0 else \
                    f"{plural(late, 'day', 'days')} late, fine {format_money(library.fine(loan, today))}"
                print(f"OK: {library.member(member_id).name} returned {library.book(book_id).title}, {tail}")
        except LibraryError as error:
            print(f"Error: {error}")


# ------------------------------------------------------------
# Stretch: closed on Sundays, and what is due this week
# ------------------------------------------------------------

def open_day(day: date) -> date:
    """The library is closed on Sundays: a Sunday due date moves to Monday.
    weekday() counts Monday as 0, so Sunday is 6."""
    return day + timedelta(days=1) if day.weekday() == 6 else day


def stretch(library: Library, today: date) -> None:
    print("Stretch")
    for loan in library.all_loans():
        due = library.due_date(loan)
        if open_day(due) != due:
            print(f"loan {loan.id}: due {due.isoformat()} is a Sunday, moves to {open_day(due).isoformat()}")
    week_end = today + timedelta(days=7)
    due_soon = [x for x in library.all_loans() if x.is_open and today <= library.due_date(x) <= week_end]
    print(f"Due by {week_end.isoformat()}: " + ", ".join(library.book(x.book_id).title for x in due_soon))


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    data = Path(args[0]) if len(args) > 0 else Path("tasks/data")
    today = date.fromisoformat(args[1]) if len(args) > 1 else DEFAULT_TODAY

    library = load_all(data)
    print(f"Today is {today.isoformat()}")
    loans_table(library, today)
    overdue_report(library, today)
    fines_report(library, today)
    new_loans(library, today)
    if "--stretch" in sys.argv:
        stretch(library, today)


if __name__ == "__main__":
    main()
