# ============================================================
# Task 06 - Book types and loan policies (solution, Core + Stretch)
# ============================================================
# Session 6: inheritance, interfaces, polymorphism. Builds on 05:
#   * Book becomes abstract, with PrintBook, EBook and AudioBook
#   * LoanPolicy is an interface with three implementations, and
#     each member gets the policy for their member type
#
# Run from the repo root:
#   python tasks/06_book_types/solution/main.py             (Core output, checked)
#   python tasks/06_book_types/solution/main.py --stretch   (Core, then the Stretch)
# ============================================================

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Final

BOOK_LINES: Final[list[str]] = [
    "id,title,author,year,genre,copies,format,length",
    "1,Pride and Prejudice,Jane Austen,1813,Classic,3,print,432",
    "2,Nineteen Eighty-Four,George Orwell,1949,Dystopian,2,print,328",
    "3,The Hobbit,J. R. R. Tolkien,1937,Fantasy,0,print,310",
    "4,Dune,Frank Herbert,1965,Science Fiction,4,print,412",
    "5,Robinson Crusoe,Daniel Defoe,1719,Adventure,1,print,320",
    "6,The Time Machine,H. G. Wells,1895,Science Fiction,2,ebook,118",
    "7,Animal Farm,George Orwell,1945,Dystopian,5,print,112",
    "8,Emma,Jane Austen,1815,Classic,1,audio,1150",
    "9,The Left Hand of Darkness,Ursula K. Le Guin,1969,Science Fiction,0,print,304",
    "10,Murder on the Orient Express,Agatha Christie,1934,Crime,2,print,256",
    "11,The Murder of Roger Ackroyd,Agatha Christie,1926,Crime,1,ebook,312",
    "12,A Wizard of Earthsea,Ursula K. Le Guin,1968,Fantasy,2,print,183",
    "13,Brave New World,Aldous Huxley,1932,Dystopian,2,audio,480",
    "14,The Martian,Andy Weir,2011,Science Fiction,3,print,369",
    "15,Small Island,Andrea Levy,2004,Historical,1,print,441",
    "16,Wolf Hall,Hilary Mantel,2009,Historical,2,audio,1440",
    "17,The Remains of the Day,Kazuo Ishiguro,1989,Literary,2,print,258",
    "18,Never Let Me Go,Kazuo Ishiguro,2005,Literary,1,ebook,288",
    "19,Frankenstein,Mary Shelley,1818,Gothic,2,print,280",
    "20,The War of the Worlds,H. G. Wells,1898,Science Fiction,3,audio,410",
]

MEMBER_LINES: Final[list[str]] = [
    "id,name,email,type,joined",
    "101,Amira Khan,amira.khan@example.com,standard,2023-01-15",
    "102,Ben Taylor,ben.taylor@example.com,student,2024-09-02",
    "103,Chloe Evans,chloe.evans@example.com,staff,2019-05-20",
    "104,Dev Patel,dev.patel@example.com,student,2025-09-10",
    "105,Ella Brown,ella.brown@example.com,standard,2021-03-08",
    "106,Femi Adeyemi,femi.adeyemi@example.com,standard,2022-11-30",
    "107,Grace Wilson,grace.wilson@example.com,staff,2018-07-01",
    "108,Harry Jones,harry.jones@example.com,student,2026-01-12",
    "109,Ben Taylor,ben.taylor2@example.com,standard,2025-02-14",
]


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

# Stretch 1: the guest policy is known to policy_for, but kept out
# of POLICIES so the Core output still lists only the three above
EXTRA_POLICIES: Final[dict[str, LoanPolicy]] = {"guest": GuestPolicy()}


def policy_for(member_type: str) -> LoanPolicy:
    """The one place that maps a type name to a policy."""
    policy = POLICIES.get(member_type) or EXTRA_POLICIES.get(member_type)
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


def load_library() -> Library:
    library = Library()
    for line in BOOK_LINES[1:]:
        library.add_book(make_book(line.split(",")))
    for line in MEMBER_LINES[1:]:
        f = line.split(",")
        library.add_member(Member(int(f[0]), f[1], f[2], f[3], f[4]))
    return library


def main() -> None:
    library = load_library()

    print("Formats")
    for book in library.all_books():
        print(book.describe())

    print("Policies")
    for policy in POLICIES.values():
        print(policy.describe())

    print("Fine for 3 days late")
    for policy in POLICIES.values():
        print(f"{policy.name}: {format_money(policy.fine_for(3))}")

    print("Limits")
    for member_id, book_id in [(101, 1), (101, 2), (101, 4), (101, 7), (102, 7), (103, 7)]:
        member = library.find_member(member_id)
        if library.borrow(member_id, book_id) and member is not None:
            print(f"borrow {member_id} {book_id}: OK, due in {member.policy.loan_days()} days")
        else:
            print(f"borrow {member_id} {book_id}: refused")

    if "--stretch" in sys.argv:
        print("Stretch")
        print(policy_for("guest").describe())
        # A guest member works with the unchanged Member and Library
        library.add_member(Member(110, "Sam Green", "sam.green@example.com", "guest", "2026-10-12"))
        for book_id in (1, 2):
            print(f"borrow 110 {book_id}: {'OK' if library.borrow(110, book_id) else 'refused'}")
        counts: dict[str, int] = {}
        for book in library.all_books():
            counts[book.format_name] = counts.get(book.format_name, 0) + 1
        print("formats: " + ", ".join(f"{name} {counts[name]}" for name in ("print", "ebook", "audio")))


if __name__ == "__main__":
    main()
