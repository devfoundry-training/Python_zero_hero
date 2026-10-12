# ============================================================
# Task 11 - Test the rules (starter)
# ============================================================
# Session 11: testing. The fixture and every test name are here;
# each test fails with "not implemented" until you write it.
# Replace the self.fail line with arrange / act / assert. Write the
# reservation tests one at a time, test first (see README.md).
#
# Run from the repo root:
#   python tasks/11_testing/starter/test_library.py
# Check it:
#   python tasks/check/check.py 11 -- python tasks/11_testing/starter/test_library.py
# ============================================================

import unittest
from datetime import date

from library import (BookNotAvailableError, Library, Loan, Member, MemberLimitReachedError,
                     NotOnLoanError, UnknownBookError, UnknownMemberError, format_money, make_book)

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
        self.fail("not implemented")

    def test_return_restores_available(self) -> None:
        self.fail("not implemented")

    def test_borrow_unknown_book_raises(self) -> None:
        self.fail("not implemented")

    def test_borrow_unknown_member_raises(self) -> None:
        self.fail("not implemented")

    def test_borrow_with_no_copies_raises(self) -> None:
        self.fail("not implemented")

    def test_return_book_not_on_loan_raises(self) -> None:
        self.fail("not implemented")

    def test_standard_limit_is_three_loans(self) -> None:
        self.fail("not implemented")

    def test_student_limit_is_five_loans(self) -> None:
        self.fail("not implemented")


class DateAndFineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.library = fixture()

    def test_due_date_standard_is_14_days(self) -> None:
        self.fail("not implemented")

    def test_due_date_student_is_21_days(self) -> None:
        self.fail("not implemented")

    def test_due_date_staff_is_28_days(self) -> None:
        self.fail("not implemented")

    def test_due_date_crosses_month_and_year_end(self) -> None:
        self.fail("not implemented")

    def test_due_date_in_leap_year(self) -> None:
        self.fail("not implemented")

    def test_not_overdue_on_due_date(self) -> None:
        self.fail("not implemented")

    def test_fine_one_day_late_standard(self) -> None:
        self.fail("not implemented")

    def test_fine_ten_days_late_student(self) -> None:
        self.fail("not implemented")

    def test_staff_never_fined(self) -> None:
        self.fail("not implemented")

    def test_late_return_fine_uses_return_date(self) -> None:
        self.fail("not implemented")

    def test_format_money(self) -> None:
        self.fail("not implemented")


class ReservationTests(unittest.TestCase):
    """Write these one at a time, test first."""

    def setUp(self) -> None:
        self.library = fixture()
        self.library.borrow(AMIRA, 5, TODAY)  # the only copy of Robinson Crusoe

    def test_reserve_book_with_no_free_copies_joins_queue(self) -> None:
        self.fail("not implemented")

    def test_reserve_book_with_free_copies_raises(self) -> None:
        self.fail("not implemented")

    def test_reserve_same_book_twice_raises(self) -> None:
        self.fail("not implemented")

    def test_returned_copy_is_held_for_first_in_queue(self) -> None:
        self.fail("not implemented")

    def test_first_in_queue_can_borrow_held_copy(self) -> None:
        self.fail("not implemented")

    def test_queue_is_first_come_first_served(self) -> None:
        self.fail("not implemented")


if __name__ == "__main__":
    unittest.main(verbosity=2)
