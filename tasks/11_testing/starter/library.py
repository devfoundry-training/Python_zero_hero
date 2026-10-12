# ============================================================
# Task 11 starter - library module: the task 09 model
# ============================================================
# The task 10 solution's library module (the task 09 model).
# Reservations are yours to add, test first (see README.md):
# write one test in test_library.py, watch it fail, then fill in
# the stubs at the bottom of Library until it passes. You will
# also need two new exceptions: ReservationNotNeededError and
# AlreadyReservedError (subclasses of LibraryError).
# ============================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Final


def plural(count: int, singular: str, many: str) -> str:
    return f"{count} {singular if count == 1 else many}"


def format_money(pence: int) -> str:
    """Whole pence to pounds: 125 -> '£1.25'. Integer maths only."""
    return f"£{pence // 100}.{pence % 100:02d}"


# ------------------------------------------------------------
# Exceptions (from task 07)
# ------------------------------------------------------------

class LibraryError(Exception):
    """Base class for every rule the library can refuse."""


class UnknownBookError(LibraryError):
    def __init__(self, book_id: int) -> None:
        super().__init__(f"no book with id {book_id}")


class UnknownMemberError(LibraryError):
    def __init__(self, member_id: int) -> None:
        super().__init__(f"no member with id {member_id}")


class BookNotAvailableError(LibraryError):
    def __init__(self, title: str) -> None:
        super().__init__(f"{title} has no copies available")


class MemberLimitReachedError(LibraryError):
    def __init__(self, name: str, limit: int) -> None:
        super().__init__(f"{name} already has {plural(limit, 'loan', 'loans')} (limit {limit})")


class NotOnLoanError(LibraryError):
    def __init__(self, title: str, name: str) -> None:
        super().__init__(f"{title} is not on loan to {name}")


class CommandError(LibraryError):
    """The user typed something we cannot understand."""


# ------------------------------------------------------------
# Loan policies (from task 06)
# ------------------------------------------------------------

class LoanPolicy(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def loan_days(self) -> int: ...

    @abstractmethod
    def fine_per_day(self) -> int: ...

    @abstractmethod
    def max_loans(self) -> int: ...

    def fine_for(self, days_late: int) -> int:
        return max(0, days_late) * self.fine_per_day()


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
# Books and members (from task 06)
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
    def length_text(self) -> str: ...

    def describe(self) -> str:
        return f"#{self.id} {self.title}: {self.format_name}, {self.length_text()}"

    @property
    def available(self) -> int:
        return self.copies - self._on_loan

    def lend(self) -> None:
        if self.available == 0:
            raise BookNotAvailableError(self.title)
        self._on_loan += 1

    def take_back(self) -> None:
        self._on_loan -= 1

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
        return f"{self.length // 60}h {self.length % 60:02d}m"


BOOK_TYPES: Final[dict[str, type[Book]]] = {"print": PrintBook, "ebook": EBook, "audio": AudioBook}


def make_book(fields: list[str]) -> Book:
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
    loans: list[int] = field(default_factory=list, init=False)  # book ids still out

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("member id must be positive")
        if self.name.strip() == "":
            raise ValueError("name must not be blank")
        self.policy = policy_for(self.type)

    def __str__(self) -> str:
        return f"#{self.id} {self.name} ({self.type}), {plural(len(self.loans), 'loan', 'loans')}"


# ------------------------------------------------------------
# Loan: new in task 09
# ------------------------------------------------------------
# date is a calendar day with no time and no time zone, which is
# exactly what a library loan needs. date + timedelta(days=n)
# moves across month and year ends (and leap days) correctly, and
# date - date gives a timedelta whose .days is a whole number.

@dataclass
class Loan:
    id: int
    book_id: int
    member_id: int
    borrowed: date
    returned: date | None = None  # None while the book is still out

    @property
    def is_open(self) -> bool:
        return self.returned is None


class Library:
    def __init__(self) -> None:
        self._books: dict[int, Book] = {}
        self._members: dict[int, Member] = {}
        self._loans: dict[int, Loan] = {}

    # --- adding and finding ------------------------------------

    def add_book(self, book: Book) -> None:
        self._books[book.id] = book

    def add_member(self, member: Member) -> None:
        self._members[member.id] = member

    def add_loan(self, loan: Loan) -> None:
        """Add a loan from the records. Open loans take a copy off the
        shelf; limits are not checked (history is what it is)."""
        self._loans[loan.id] = loan
        if loan.is_open:
            self.book(loan.book_id).lend()
            self.member(loan.member_id).loans.append(loan.book_id)

    @property
    def book_count(self) -> int:
        return len(self._books)

    @property
    def member_count(self) -> int:
        return len(self._members)

    @property
    def loan_count(self) -> int:
        return len(self._loans)

    def all_books(self) -> list[Book]:
        return sorted(self._books.values(), key=lambda b: b.id)

    def all_members(self) -> list[Member]:
        return sorted(self._members.values(), key=lambda m: m.id)

    def all_loans(self) -> list[Loan]:
        return sorted(self._loans.values(), key=lambda x: x.id)

    def find_by_id(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def find_member(self, member_id: int) -> Member | None:
        return self._members.get(member_id)

    def find_by_title(self, text: str) -> list[Book]:
        wanted = text.lower()
        return [b for b in self.all_books() if wanted in b.title.lower()]

    def book(self, book_id: int) -> Book:
        found = self._books.get(book_id)
        if found is None:
            raise UnknownBookError(book_id)
        return found

    def member(self, member_id: int) -> Member:
        found = self._members.get(member_id)
        if found is None:
            raise UnknownMemberError(member_id)
        return found

    # --- dates and money ---------------------------------------

    def due_date(self, loan: Loan) -> date:
        return loan.borrowed + timedelta(days=self.member(loan.member_id).policy.loan_days())

    def days_late(self, loan: Loan, today: date) -> int:
        """Whole days past the due date: on the return date if the book
        is back, otherwise today. Never negative."""
        end = loan.returned if loan.returned is not None else today
        return max(0, (end - self.due_date(loan)).days)

    def fine(self, loan: Loan, today: date) -> int:
        """The fine in pence."""
        return self.member(loan.member_id).policy.fine_for(self.days_late(loan, today))

    def status(self, loan: Loan, today: date) -> str:
        due = self.due_date(loan)
        if loan.returned is not None:
            late = self.days_late(loan, today)
            return "returned on time" if late == 0 else f"returned {plural(late, 'day', 'days')} late"
        if today < due:
            return f"on loan, {plural((due - today).days, 'day', 'days')} left"
        if today == due:
            return "due today"
        return f"overdue by {plural((today - due).days, 'day', 'days')}"

    def overdue(self, today: date) -> list[Loan]:
        """Open loans past their due date: most days late first, then by id."""
        late = [x for x in self._loans.values() if x.is_open and self.days_late(x, today) > 0]
        return sorted(late, key=lambda x: (-self.days_late(x, today), x.id))

    # --- the rules -----------------------------------------------

    def borrow(self, member_id: int, book_id: int, today: date) -> Loan:
        member = self.member(member_id)
        book = self.book(book_id)
        limit = member.policy.max_loans()
        if len(member.loans) >= limit:
            raise MemberLimitReachedError(member.name, limit)
        book.lend()
        member.loans.append(book_id)
        loan = Loan(max(self._loans, default=0) + 1, book_id, member_id, today)
        self._loans[loan.id] = loan
        return loan

    def return_book(self, member_id: int, book_id: int, today: date) -> Loan:
        member = self.member(member_id)
        book = self.book(book_id)
        loan = next((x for x in self.all_loans()
                     if x.is_open and x.member_id == member_id and x.book_id == book_id), None)
        if loan is None:
            raise NotOnLoanError(book.title, member.name)
        loan.returned = today
        member.loans.remove(book_id)
        book.take_back()
        return loan

    # --- reservations (TODO, test first) ---------------------------

    def reserve(self, member_id: int, book_id: int) -> int:
        """Join the queue for a book. Returns the place in the queue (1 = next)."""
        raise NotImplementedError("not implemented: Library.reserve")

    def queue_for(self, book_id: int) -> list[int]:
        """Member ids waiting for this book, first in the queue first."""
        raise NotImplementedError("not implemented: Library.queue_for")

    def held_for(self, book_id: int) -> list[int]:
        """Member ids with a returned copy of this book held for them."""
        raise NotImplementedError("not implemented: Library.held_for")
