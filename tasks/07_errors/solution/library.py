# ============================================================
# Task 07 - library module: the task 06 model, now with exceptions
# ============================================================
# What changed from task 06:
#   * borrow() and return_book() raise a LibraryError subclass
#     instead of returning False, so the caller learns WHY
#   * every message is written once, here, in the exception
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
# Our own exceptions: one base class, one subclass per problem
# ------------------------------------------------------------
# Catch LibraryError to handle every library problem in one place;
# catch a subclass when one problem needs special handling.

class LibraryError(Exception):
    """Base class for every rule the library can refuse."""


class UnknownBookError(LibraryError):
    def __init__(self, book_id: int) -> None:
        super().__init__(f"no book with id {book_id}")
        self.book_id = book_id


class UnknownMemberError(LibraryError):
    def __init__(self, member_id: int) -> None:
        super().__init__(f"no member with id {member_id}")
        self.member_id = member_id


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
# Loan policies (unchanged from task 06)
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
# Books and members (unchanged from task 06)
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
    loans: list[int] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("member id must be positive")
        if self.name.strip() == "":
            raise ValueError("name must not be blank")
        self.policy = policy_for(self.type)

    def __str__(self) -> str:
        return f"#{self.id} {self.name} ({self.type}), {plural(len(self.loans), 'loan', 'loans')}"


# ------------------------------------------------------------
# Library: the rules, now raising instead of returning False
# ------------------------------------------------------------

class Library:
    def __init__(self) -> None:
        self._books: dict[int, Book] = {}
        self._members: dict[int, Member] = {}

    def add_book(self, book: Book) -> None:
        self._books[book.id] = book

    def add_member(self, member: Member) -> None:
        self._members[member.id] = member

    @property
    def book_count(self) -> int:
        return len(self._books)

    @property
    def member_count(self) -> int:
        return len(self._members)

    def all_books(self) -> list[Book]:
        return sorted(self._books.values(), key=lambda b: b.id)

    def all_members(self) -> list[Member]:
        return sorted(self._members.values(), key=lambda m: m.id)

    def find_by_id(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def find_member(self, member_id: int) -> Member | None:
        return self._members.get(member_id)

    def book(self, book_id: int) -> Book:
        """Like find_by_id, but a missing book is an error."""
        found = self._books.get(book_id)
        if found is None:
            raise UnknownBookError(book_id)
        return found

    def member(self, member_id: int) -> Member:
        found = self._members.get(member_id)
        if found is None:
            raise UnknownMemberError(member_id)
        return found

    def borrow(self, member_id: int, book_id: int) -> tuple[Member, Book]:
        # The order of the checks is part of the brief
        member = self.member(member_id)
        book = self.book(book_id)
        limit = member.policy.max_loans()
        if len(member.loans) >= limit:
            raise MemberLimitReachedError(member.name, limit)
        book.lend()  # raises BookNotAvailableError
        member.loans.append(book_id)
        return member, book

    def return_book(self, member_id: int, book_id: int) -> tuple[Member, Book]:
        member = self.member(member_id)
        book = self.book(book_id)
        if book_id not in member.loans:
            raise NotOnLoanError(book.title, member.name)
        member.loans.remove(book_id)
        book.take_back()
        return member, book
