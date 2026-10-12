# ============================================================
# Task 05 - Classes (starter)
# ============================================================
# Session 5: classes and encapsulation. Builds on task 04: the
# records become Book, Member and Library objects with methods.
# The data and the loading code are here; every method that
# still raises NotImplementedError is yours to write.
#
# Run from the repo root:
#   python tasks/05_classes/starter/main.py
# Check it:
#   python tasks/check/check.py 05 -- python tasks/05_classes/starter/main.py
# ============================================================

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
# Book
# ------------------------------------------------------------

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
        # TODO Core 3: refuse bad values with ValueError("book id must be positive"), ...
        pass

    @property
    def available(self) -> int:
        raise NotImplementedError("not implemented: Book.available")

    def lend(self) -> bool:
        raise NotImplementedError("not implemented: Book.lend")

    def take_back(self) -> bool:
        raise NotImplementedError("not implemented: Book.take_back")

    def __str__(self) -> str:
        raise NotImplementedError("not implemented: Book.__str__")


# ------------------------------------------------------------
# Member
# ------------------------------------------------------------

@dataclass(eq=False)
class Member:
    id: int
    name: str
    email: str
    type: str
    joined: str
    loans: list[int] = field(default_factory=list, init=False)  # book ids

    def __post_init__(self) -> None:
        # TODO Core 3: the type must be one of MEMBER_TYPES
        pass

    def __str__(self) -> str:
        raise NotImplementedError("not implemented: Member.__str__")


# ------------------------------------------------------------
# Library: owns the books and members, and the borrowing rules
# ------------------------------------------------------------

class Library:
    def __init__(self) -> None:
        self._books: dict[int, Book] = {}
        self._members: dict[int, Member] = {}

    def add_book(self, book: Book) -> None:
        raise NotImplementedError("not implemented: Library.add_book")

    def add_member(self, member: Member) -> None:
        raise NotImplementedError("not implemented: Library.add_member")

    @property
    def book_count(self) -> int:
        return len(self._books)

    @property
    def member_count(self) -> int:
        return len(self._members)

    def find_by_id(self, book_id: int) -> Book | None:
        """The book, or None when there is no such id."""
        raise NotImplementedError("not implemented: Library.find_by_id")

    def find_member(self, member_id: int) -> Member | None:
        raise NotImplementedError("not implemented: Library.find_member")

    def find_by_title(self, text: str) -> list[Book]:
        """Books whose title contains text, ignoring case, by id."""
        raise NotImplementedError("not implemented: Library.find_by_title")

    def borrow(self, member_id: int, book_id: int) -> bool:
        raise NotImplementedError("not implemented: Library.borrow")

    def return_book(self, member_id: int, book_id: int) -> bool:
        raise NotImplementedError("not implemented: Library.return_book")


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
    # TODO Core 5: the rest of the script in README.md, Output format:
    # book 4 and member 101, the finds, borrowing, after borrowing
    # and validation
    print("The rest of the script: not implemented")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as error:
        print(error)  # the first piece still to write
