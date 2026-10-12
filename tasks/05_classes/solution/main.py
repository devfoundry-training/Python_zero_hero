# ============================================================
# Task 05 - Classes (solution, Core + Stretch)
# ============================================================
# Session 5: classes and encapsulation. Builds on task 04: the
# records become Book, Member and Library objects with methods.
#
# Run from the repo root:
#   python tasks/05_classes/solution/main.py             (Core output, checked)
#   python tasks/05_classes/solution/main.py --stretch   (Core, then the Stretch)
# ============================================================

import sys
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

MEMBER_TYPES: Final[tuple[str, ...]] = ("standard", "student", "staff")


def plural(count: int, singular: str, many: str) -> str:
    return f"{count} {singular if count == 1 else many}"


# ------------------------------------------------------------
# Book: validated on the way in, knows how many are on loan
# ------------------------------------------------------------
# eq=False: two books are the same book when the ids match, not
# when every field matches (see __eq__ below, Stretch 1).

@dataclass(eq=False)
class Book:
    id: int
    title: str
    author: str
    year: int
    genre: str
    copies: int
    _on_loan: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        # Validation in the constructor: a Book that exists is valid
        if self.id <= 0:
            raise ValueError("book id must be positive")
        if self.title.strip() == "":
            raise ValueError("title must not be blank")
        if not 1450 <= self.year <= 2100:
            raise ValueError("year must be between 1450 and 2100")
        if self.copies < 0:
            raise ValueError("copies must not be negative")

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

    # Stretch 1: identity is the id
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Book) and other.id == self.id

    def __hash__(self) -> int:
        return hash(self.id)

    # Stretch 2: natural order is title A-Z (ignoring case), then year
    def __lt__(self, other: "Book") -> bool:
        return (self.title.lower(), self.year) < (other.title.lower(), other.year)


@dataclass(eq=False)
class Member:
    id: int
    name: str
    email: str
    type: str
    joined: str
    loans: list[int] = field(default_factory=list, init=False)  # book ids

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("member id must be positive")
        if self.name.strip() == "":
            raise ValueError("name must not be blank")
        if self.type not in MEMBER_TYPES:
            raise ValueError("member type must be standard, student or staff")

    def __str__(self) -> str:
        return f"#{self.id} {self.name} ({self.type}), {plural(len(self.loans), 'loan', 'loans')}"


# ------------------------------------------------------------
# Library: owns the books and members, and the borrowing rules
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

    def find_by_id(self, book_id: int) -> Book | None:
        """The book, or None when there is no such id."""
        return self._books.get(book_id)

    def find_member(self, member_id: int) -> Member | None:
        return self._members.get(member_id)

    def find_by_title(self, text: str) -> list[Book]:
        """Books whose title contains text, ignoring case, by id."""
        wanted = text.lower()
        return [b for b in sorted(self._books.values(), key=lambda b: b.id) if wanted in b.title.lower()]

    def borrow(self, member_id: int, book_id: int) -> bool:
        member = self.find_member(member_id)
        book = self.find_by_id(book_id)
        if member is None or book is None:
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

    def available_books(self) -> list[Book]:
        """Stretch 3: books with at least one copy on the shelf."""
        return [b for b in self._books.values() if b.available > 0]

    def all_books(self) -> list[Book]:
        return list(self._books.values())


def load_library() -> Library:
    library = Library()
    for line in BOOK_LINES[1:]:
        f = line.split(",")
        library.add_book(Book(int(f[0]), f[1], f[2], int(f[3]), f[4], int(f[5])))
    for line in MEMBER_LINES[1:]:
        f = line.split(",")
        library.add_member(Member(int(f[0]), f[1], f[2], f[3], f[4]))
    return library


# ------------------------------------------------------------
# The Core script
# ------------------------------------------------------------

def main() -> None:
    library = load_library()
    print(f"Library: {library.book_count} books, {library.member_count} members")
    print(library.find_by_id(4))
    print(library.find_member(101))

    for text in ("the", "zzz"):
        found = library.find_by_title(text)
        if found:
            print(f'Find "{text}": {plural(len(found), "book", "books")}')
            for book in found:
                print(f"  {book}")
        else:
            print(f'Find "{text}": no books')

    missing = library.find_by_id(99)
    print("Find id 99: not found" if missing is None else f"Find id 99: {missing}")

    print("Borrowing")
    script = [
        ("borrow", 101, 4),
        ("borrow", 101, 3),
        ("borrow", 999, 1),
        ("borrow", 101, 99),
        ("borrow", 102, 5),
        ("borrow", 103, 5),
        ("return", 101, 4),
        ("return", 101, 4),
    ]
    for action, member_id, book_id in script:
        if action == "borrow":
            ok = library.borrow(member_id, book_id)
        else:
            ok = library.return_book(member_id, book_id)
        print(f"{action} {member_id} {book_id}: {'OK' if ok else 'refused'}")

    print("After borrowing")
    print(library.find_by_id(4))
    print(library.find_by_id(5))
    print(library.find_member(101))
    print(library.find_member(102))

    print("Validation")
    attempts = [
        lambda: Book(0, "Dune", "Frank Herbert", 1965, "Science Fiction", 4),
        lambda: Book(21, "   ", "Frank Herbert", 1965, "Science Fiction", 4),
        lambda: Book(21, "Dune", "Frank Herbert", 3000, "Science Fiction", 4),
        lambda: Book(21, "Dune", "Frank Herbert", 1965, "Science Fiction", -1),
        lambda: Member(110, "Sam Green", "sam.green@example.com", "visitor", "2026-10-12"),
    ]
    for attempt in attempts:
        try:
            attempt()
            print("Accepted")
        except ValueError as error:
            print(f"Rejected: {error}")

    if "--stretch" in sys.argv:
        print("Stretch")
        copy = Book(4, "Dune (second copy record)", "Frank Herbert", 1965, "Science Fiction", 1)
        print(f"same book as #4: {copy == library.find_by_id(4)}")
        first = sorted(library.all_books())[:5]
        print("first 5 by title: " + ", ".join(f"{b.title} ({b.year})" for b in first))
        print(f"available books: {len(library.available_books())}")


if __name__ == "__main__":
    main()
