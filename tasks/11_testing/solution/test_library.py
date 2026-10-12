# ============================================================
# Task 11 - Test the rules (solution, Core + Stretch)
# ============================================================
# Session 11: testing. Every test builds a fresh library in
# setUp, so no test depends on another one or on the order they
# run in. Dates are fixed values: nothing reads the real clock.
#
# Run from the repo root:
#   python tasks/11_testing/solution/test_library.py
#   or, inside the solution folder:
#   python -m unittest -v test_library
# ============================================================

import unittest
from datetime import date
from pathlib import Path

from library import (AlreadyReservedError, BookNotAvailableError, Library, Loan, Member,
                     MemberLimitReachedError, NotOnLoanError, ReservationNotNeededError,
                     UnknownBookError, UnknownMemberError, format_money, make_book)
from storage import load_books_csv

TODAY = date(2026, 10, 12)

# The fixture: books 1-8 of books.csv and members 101-103, no loans
FIXTURE_BOOKS = [
    "1,Pride and Prejudice,Jane Austen,1813,Classic,3,print,432",
    "2,Nineteen Eighty-Four,George Orwell,1949,Dystopian,2,print,328",
    "3,The Hobbit,J. R. R. Tolkien,1937,Fantasy,0,print,310",
    "4,Dune,Frank Herbert,1965,Science Fiction,4,print,412",
    "5,Robinson Crusoe,Daniel Defoe,1719,Adventure,1,print,320",
    "6,The Time Machine,H. G. Wells,1895,Science Fiction,2,ebook,118",
    "7,Animal Farm,George Orwell,1945,Dystopian,5,print,112",
    "8,Emma,Jane Austen,1815,Classic,1,audio,1150",
]
AMIRA, BEN, CHLOE = 101, 102, 103  # standard, student, staff


def fixture() -> Library:
    library = Library()
    for line in FIXTURE_BOOKS:
        library.add_book(make_book(line.split(",")))
    library.add_member(Member(AMIRA, "Amira Khan", "amira.khan@example.com", "standard", "2023-01-15"))
    library.add_member(Member(BEN, "Ben Taylor", "ben.taylor@example.com", "student", "2024-09-02"))
    library.add_member(Member(CHLOE, "Chloe Evans", "chloe.evans@example.com", "staff", "2019-05-20"))
    return library


class BorrowingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.library = fixture()

    def test_borrow_reduces_available(self) -> None:
        self.library.borrow(AMIRA, 4, TODAY)
        self.assertEqual(3, self.library.book(4).available)

    def test_return_restores_available(self) -> None:
        self.library.borrow(AMIRA, 4, TODAY)
        self.library.return_book(AMIRA, 4, TODAY)
        self.assertEqual(4, self.library.book(4).available)

    def test_borrow_unknown_book_raises(self) -> None:
        with self.assertRaises(UnknownBookError):
            self.library.borrow(AMIRA, 99, TODAY)

    def test_borrow_unknown_member_raises(self) -> None:
        with self.assertRaises(UnknownMemberError):
            self.library.borrow(999, 1, TODAY)

    def test_borrow_with_no_copies_raises(self) -> None:
        with self.assertRaises(BookNotAvailableError):
            self.library.borrow(AMIRA, 3, TODAY)

    def test_return_book_not_on_loan_raises(self) -> None:
        with self.assertRaises(NotOnLoanError):
            self.library.return_book(AMIRA, 4, TODAY)

    def test_standard_limit_is_three_loans(self) -> None:
        for book_id in (1, 2, 4):
            self.library.borrow(AMIRA, book_id, TODAY)
        with self.assertRaises(MemberLimitReachedError):
            self.library.borrow(AMIRA, 7, TODAY)

    def test_student_limit_is_five_loans(self) -> None:
        for book_id in (1, 2, 4, 6, 7):
            self.library.borrow(BEN, book_id, TODAY)
        with self.assertRaises(MemberLimitReachedError):
            self.library.borrow(BEN, 8, TODAY)


class DateAndFineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.library = fixture()

    def due(self, member_id: int, borrowed: date) -> date:
        return self.library.due_date(Loan(1, 1, member_id, borrowed))

    def test_due_date_standard_is_14_days(self) -> None:
        self.assertEqual(date(2026, 10, 26), self.due(AMIRA, date(2026, 10, 12)))

    def test_due_date_student_is_21_days(self) -> None:
        self.assertEqual(date(2026, 11, 2), self.due(BEN, date(2026, 10, 12)))

    def test_due_date_staff_is_28_days(self) -> None:
        self.assertEqual(date(2026, 11, 9), self.due(CHLOE, date(2026, 10, 12)))

    def test_due_date_crosses_month_and_year_end(self) -> None:
        self.assertEqual(date(2027, 1, 10), self.due(BEN, date(2026, 12, 20)))

    def test_due_date_in_leap_year(self) -> None:
        self.assertEqual(date(2028, 3, 5), self.due(AMIRA, date(2028, 2, 20)))

    def test_not_overdue_on_due_date(self) -> None:
        loan = Loan(1, 1, AMIRA, date(2026, 9, 28))  # due 2026-10-12
        self.assertEqual(0, self.library.days_late(loan, TODAY))
        self.assertEqual(0, self.library.fine(loan, TODAY))

    def test_fine_one_day_late_standard(self) -> None:
        loan = Loan(1, 1, AMIRA, date(2026, 9, 27))  # due 2026-10-11
        self.assertEqual(25, self.library.fine(loan, TODAY))

    def test_fine_ten_days_late_student(self) -> None:
        loan = Loan(1, 1, BEN, date(2026, 9, 11))  # due 2026-10-02
        self.assertEqual(100, self.library.fine(loan, TODAY))

    def test_staff_never_fined(self) -> None:
        loan = Loan(1, 1, CHLOE, date(2026, 1, 1))
        self.assertEqual(0, self.library.fine(loan, TODAY))

    def test_late_return_fine_uses_return_date(self) -> None:
        # Due 2026-10-01, back 2026-10-05: 4 days late, whatever today is
        loan = Loan(1, 1, AMIRA, date(2026, 9, 17), returned=date(2026, 10, 5))
        self.assertEqual(100, self.library.fine(loan, date(2026, 12, 25)))

    def test_format_money(self) -> None:
        self.assertEqual("£0.00", format_money(0))
        self.assertEqual("£0.05", format_money(5))
        self.assertEqual("£1.25", format_money(125))
        self.assertEqual("£10.00", format_money(1000))


class ReservationTests(unittest.TestCase):
    """Written first, watched fail, then made to pass (TDD)."""

    def setUp(self) -> None:
        self.library = fixture()
        self.library.borrow(AMIRA, 5, TODAY)  # the only copy of Robinson Crusoe

    def test_reserve_book_with_no_free_copies_joins_queue(self) -> None:
        self.assertEqual(1, self.library.reserve(BEN, 5))
        self.assertEqual(2, self.library.reserve(CHLOE, 5))

    def test_reserve_book_with_free_copies_raises(self) -> None:
        with self.assertRaises(ReservationNotNeededError):
            self.library.reserve(BEN, 1)

    def test_reserve_same_book_twice_raises(self) -> None:
        self.library.reserve(BEN, 5)
        with self.assertRaises(AlreadyReservedError):
            self.library.reserve(BEN, 5)

    def test_returned_copy_is_held_for_first_in_queue(self) -> None:
        self.library.reserve(BEN, 5)
        self.library.return_book(AMIRA, 5, TODAY)
        with self.assertRaises(BookNotAvailableError):
            self.library.borrow(CHLOE, 5, TODAY)

    def test_first_in_queue_can_borrow_held_copy(self) -> None:
        self.library.reserve(BEN, 5)
        self.library.return_book(AMIRA, 5, TODAY)
        self.library.borrow(BEN, 5, TODAY)
        self.assertEqual(0, self.library.book(5).available)
        self.assertEqual([], self.library.held_for(5))

    def test_queue_is_first_come_first_served(self) -> None:
        self.library.reserve(CHLOE, 5)
        self.library.reserve(BEN, 5)
        self.library.return_book(AMIRA, 5, TODAY)
        self.assertEqual([CHLOE], self.library.held_for(5))
        self.assertEqual([BEN], self.library.queue_for(5))


# ------------------------------------------------------------
# Stretch: the file loader, and a table of cases with subTest
# ------------------------------------------------------------

def find_data_dir() -> Path:
    """Walk up from this file to the first folder holding data/books.csv."""
    for folder in Path(__file__).resolve().parents:
        if (folder / "data" / "books.csv").exists():
            return folder / "data"
    raise FileNotFoundError("could not find the data folder")


class StretchTests(unittest.TestCase):
    def test_corrupt_csv_loads_good_lines_only(self) -> None:
        result = load_books_csv(find_data_dir() / "books_corrupt.csv")
        self.assertEqual([1, 2, 4, 6, 10], [b.id for b in result.books])
        self.assertEqual(5, result.skipped)

    def test_fines_table(self) -> None:
        library = fixture()
        cases = [  # (member, days late, expected pence)
            (AMIRA, 0, 0), (AMIRA, 1, 25), (AMIRA, 20, 500),
            (BEN, 1, 10), (BEN, 30, 300), (CHLOE, 365, 0),
        ]
        for member_id, days, pence in cases:
            with self.subTest(member=member_id, days=days):
                policy = library.member(member_id).policy
                self.assertEqual(pence, policy.fine_for(days))


if __name__ == "__main__":
    unittest.main(verbosity=2)
