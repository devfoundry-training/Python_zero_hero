# ============================================================
# Task 07 starter - library module: the task 06 model
# ============================================================
# This is the task 06 solution, moved into its own module so the
# command loop in main.py can import it. Your changes (README.md):
#   * the exceptions at the bottom of this file (Core 1)
#   * borrow() and return_book() raise them instead of returning
#     False, checking in the order the brief gives (Core 2)
# ============================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Final


def plural(count: int, singular: str, many: str) -> str:
    return f"{count} {singular if count == 1 else many}"


def format_money(pence: int) -> str:
    """Whole pence to pounds: 125 -> '£1.25'. Integer maths only."""
    return f"£{pence // 100}.{pence % 100:02d}"


# ------------------------------------------------------------
# Loan policies: one interface, three (plus one) implementations
# ------------------------------------------------------------

class LoanPolicy(ABC):
    """What every policy must answer. Library code only talks to
    this interface, never to a concrete policy class."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def loan_days(self) -> int: ...

    @abstractmethod
    def fine_per_day(self) -> int:
        """Pence charged for each day late."""

    @abstractmethod
    def max_loans(self) -> int: ...

    def fine_for(self, days_late: int) -> int:
        """Shared behaviour: inherited by every policy."""
        return max(0, days_late) * self.fine_per_day()

    def describe(self) -> str:
        fine = "no fines" if self.fine_per_day() == 0 else f"{format_money(self.fine_per_day())} a day"
        return f"{self.name}: {self.loan_days()} days, {fine}, up to {plural(self.max_loans(), 'loan', 'loans')}"


class StandardPolicy(LoanPolicy):
    name = "standard"

    def loan_days(self) -> int:
        return 14

    def fine_per_day(self) -> int:
        return 25

    def max_loans(self) -> int:
        return 3


class StudentPolicy(LoanPolicy):
    name = "student"

    def loan_days(self) -> int:
        return 21

    def fine_per_day(self) -> int:
        return 10

    def max_loans(self) -> int:
        return 5


class StaffPolicy(LoanPolicy):
    name = "staff"

    def loan_days(self) -> int:
        return 28

    def fine_per_day(self) -> int:
        return 0

    def max_loans(self) -> int:
        return 10


class GuestPolicy(LoanPolicy):
    """Stretch 1: a new policy, added without touching Library."""

    name = "guest"

    def loan_days(self) -> int:
        return 7

    def fine_per_day(self) -> int:
        return 50

    def max_loans(self) -> int:
        return 1


POLICIES: Final[dict[str, LoanPolicy]] = {
    "standard": StandardPolicy(),
    "student": StudentPolicy(),
    "staff": StaffPolicy(),
}


def policy_for(member_type: str) -> LoanPolicy:
    policy = POLICIES.get(member_type)
    if policy is None:
        raise ValueError("member type must be standard, student or staff")
    return policy


# ------------------------------------------------------------
# Books: an abstract base and three concrete types
# ------------------------------------------------------------

@dataclass(eq=False)
class Book(ABC):
    id: int
    title: str
    author: str
    year: int
    genre: str
    copies: int
    length: int
    _on_loan: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("book id must be positive")
        if self.title.strip() == "":
            raise ValueError("title must not be blank")
        if not 1450 <= self.year <= 2100:
            raise ValueError("year must be between 1450 and 2100")
        if self.copies < 0:
            raise ValueError("copies must not be negative")
        if self.length <= 0:
            raise ValueError("length must be positive")

    @property
    @abstractmethod
    def format_name(self) -> str: ...

    @abstractmethod
    def length_text(self) -> str:
        """Each type says how long it is in its own way."""

    def describe(self) -> str:
        # Polymorphism: the same call works for every book type
        return f"#{self.id} {self.title}: {self.format_name}, {self.length_text()}"

    @property
    def available(self) -> int:
        return self.copies - self._on_loan

    def lend(self) -> bool:
        if self.available == 0:
            return False
        self._on_loan += 1
        return True

    def take_back(self) -> bool:
        if self._on_loan == 0:
            return False
        self._on_loan -= 1
        return True

    def __str__(self) -> str:
        return f"#{self.id} {self.title} by {self.author} ({self.year}), {self.available} of {self.copies} available"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Book) and other.id == self.id

    def __hash__(self) -> int:
        return hash(self.id)


class PrintBook(Book):
    format_name = "print"

    def length_text(self) -> str:
        return f"{self.length} pages"


class EBook(Book):
    format_name = "ebook"

    def length_text(self) -> str:
        return f"{self.length} pages"


class AudioBook(Book):
    format_name = "audio"

    def length_text(self) -> str:
        # length is in minutes: 1150 -> 19h 10m
        return f"{self.length // 60}h {self.length % 60:02d}m"


BOOK_TYPES: Final[dict[str, type[Book]]] = {"print": PrintBook, "ebook": EBook, "audio": AudioBook}


def make_book(fields: list[str]) -> Book:
    """Factory: the format column decides which class to build."""
    book_type = BOOK_TYPES.get(fields[6])
    if book_type is None:
        raise ValueError(f"format must be print, ebook or audio, got '{fields[6]}'")
    return book_type(int(fields[0]), fields[1], fields[2], int(fields[3]), fields[4], int(fields[5]), int(fields[7]))


@dataclass(eq=False)
class Member:
    id: int
    name: str
    email: str
    type: str
    joined: str
    policy: LoanPolicy = field(init=False)
    loans: list[int] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("member id must be positive")
        if self.name.strip() == "":
            raise ValueError("name must not be blank")
        self.policy = policy_for(self.type)

    def can_borrow_more(self) -> bool:
        return len(self.loans) < self.policy.max_loans()

    def __str__(self) -> str:
        return f"#{self.id} {self.name} ({self.type}), {plural(len(self.loans), 'loan', 'loans')}"


class Library:
    def __init__(self) -> None:
        self._books: dict[int, Book] = {}
        self._members: dict[int, Member] = {}

    def add_book(self, book: Book) -> None:
        self._books[book.id] = book

    def add_member(self, member: Member) -> None:
        self._members[member.id] = member

    def find_by_id(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def find_member(self, member_id: int) -> Member | None:
        return self._members.get(member_id)

    def all_books(self) -> list[Book]:
        return sorted(self._books.values(), key=lambda b: b.id)

    def borrow(self, member_id: int, book_id: int) -> bool:
        member = self.find_member(member_id)
        book = self.find_by_id(book_id)
        if member is None or book is None:
            return False
        if not member.can_borrow_more():  # the policy decides the limit
            return False
        if not book.lend():
            return False
        member.loans.append(book_id)
        return True

    def return_book(self, member_id: int, book_id: int) -> bool:
        member = self.find_member(member_id)
        book = self.find_by_id(book_id)
        if member is None or book is None or book_id not in member.loans:
            return False
        member.loans.remove(book_id)
        book.take_back()
        return True


# ------------------------------------------------------------
# Our own exceptions (TODO Core 1)
# ------------------------------------------------------------

class LibraryError(Exception):
    """Base class for every rule the library can refuse."""


# TODO: UnknownBookError, UnknownMemberError, BookNotAvailableError,
# MemberLimitReachedError and NotOnLoanError, each building its own
# message from the brief, and CommandError (the message passed in)
