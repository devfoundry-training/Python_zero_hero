# ============================================================
# Task 08 - Persistence (starter)
# ============================================================
# Session 8: file I/O. Builds on task 07 (library.py is the task
# 07 solution). The data now comes from the files in the data
# folder, and the library is saved to CSV and JSON in a folder
# called out (made in the current folder). The file work goes in
# storage.py; the steps of the run go here (see README.md).
#
# Run from the repo root:
#   python tasks/08_persistence/starter/main.py tasks/data
# Check it:
#   python tasks/check/check.py 08 -- python tasks/08_persistence/starter/main.py tasks/data
# ============================================================

import sys
from pathlib import Path

from storage import build_library, load_books_csv, load_members_csv

OUT = Path("out")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    data = Path(args[0]) if args else Path("tasks/data")

    # Core 1: load the real data from disk
    books = load_books_csv(data / "books.csv")
    members = load_members_csv(data / "members.csv")
    print(f"Loaded {len(books.books)} books from books.csv")
    print(f"Loaded {len(members.members)} members from members.csv")
    books.members = members.members
    library = build_library(books)

    # TODO Core 2 and 3: save out/books.csv and out/library.json,
    # load out/books.csv back and compare it with the library
    # TODO Core 4 and 5: missing.csv and books_corrupt.csv
    raise NotImplementedError("not implemented: saving, reloading and the bad files (Core 2 to 5)")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as error:
        print(error)  # the first piece still to write
