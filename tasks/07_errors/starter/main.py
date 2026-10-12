# ============================================================
# Task 07 - Errors done properly (starter)
# ============================================================
# Session 7: exceptions. Builds on task 06 (now in library.py).
# Reads commands, one per line, and must never crash:
#   borrow MEMBER_ID BOOK_ID | return MEMBER_ID BOOK_ID
#   loans MEMBER_ID          | quit
#
# Run from the repo root:
#   python tasks/07_errors/starter/main.py < tasks/data/input_07.txt
# Check it:
#   python tasks/check/check.py 07 -- python tasks/07_errors/starter/main.py
# ============================================================

import re
import sys
from typing import Final

from library import Library, Member, make_book

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


def load_library() -> Library:
    library = Library()
    for line in BOOK_LINES[1:]:
        library.add_book(make_book(line.split(",")))
    for line in MEMBER_LINES[1:]:
        f = line.split(",")
        library.add_member(Member(int(f[0]), f[1], f[2], f[3], f[4]))
    return library


# ------------------------------------------------------------
# Turning text into commands (TODO)
# ------------------------------------------------------------

def parse_id(text: str, what: str) -> int:
    """'4' -> 4. Anything else raises CommandError with
    "WHAT must be a whole number, got 'TEXT'". Check the text with
    re.fullmatch(r"-?[0-9]+", text) first: int() alone accepts '+4'."""
    raise NotImplementedError("not implemented: parse_id")


def run_command(library: Library, words: list[str]) -> str:
    """Do one command and return the line to print, or raise a
    LibraryError subclass when it cannot be done."""
    raise NotImplementedError("not implemented: run_command")


def main() -> None:
    library = load_library()
    # TODO Core 3 to 6: print the first line, then read sys.stdin
    # line by line until "quit" or the end of the input. Echo each
    # non-blank line, run it, print "Error: MESSAGE" for a
    # LibraryError and "Error: unexpected problem" for anything else,
    # and finish with "Goodbye".
    raise NotImplementedError("not implemented: the command loop")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as error:
        print(error)  # the first piece still to write
