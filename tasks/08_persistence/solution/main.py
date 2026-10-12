# ============================================================
# Task 08 - Persistence (solution, Core + Stretch)
# ============================================================
# Session 8: file I/O. Builds on task 07: the data now comes from
# the files in the data folder, and the library is saved to CSV
# and JSON in a folder called out (made in the current folder).
# Core reads CSV back; reading JSON back is the Stretch.
#
# Run from the repo root:
#   python tasks/08_persistence/solution/main.py DATA_DIR             (Core, checked)
#   python tasks/08_persistence/solution/main.py DATA_DIR --stretch   (Core, then Stretch)
# DATA_DIR defaults to tasks/data.
# ============================================================

import sys
from collections.abc import Callable
from pathlib import Path

from library import Library
from storage import (LoadResult, build_library, load_books_csv, load_json, load_members_csv,
                     save_books_csv, save_json)

OUT = Path("out")


def same_books(a: Library, b: Library) -> bool:
    """Same ids with the same field values, in the same order."""
    def rows(library: Library) -> list[tuple[object, ...]]:
        return [(x.id, x.title, x.author, x.year, x.genre, x.copies, x.format_name, x.length)
                for x in library.all_books()]
    return rows(a) == rows(b)


def same_members(a: Library, b: Library) -> bool:
    def rows(library: Library) -> list[tuple[object, ...]]:
        return [(m.id, m.name, m.email, m.type, m.joined, tuple(m.loans)) for m in library.all_members()]
    return rows(a) == rows(b)


def try_load(name: str, loader: Callable[[Path], LoadResult], path: Path) -> None:
    """Load a file that might be missing or broken, and say what happened."""
    print(f"Loading {name}")
    try:
        result = loader(path)
    except FileNotFoundError:
        print("  file not found, starting with an empty catalogue")
        return
    except ValueError as error:
        print(f"  {error}, starting with an empty catalogue")
        return
    for problem in result.problems:
        print(f"  {problem}")
    print(f"  loaded {len(result.books)} books, skipped {result.skipped} lines")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    data = Path(args[0]) if args else Path("tasks/data")

    # ------------------------------------------------------------
    # Core 1: load the real data from disk
    # ------------------------------------------------------------
    books = load_books_csv(data / "books.csv")
    members = load_members_csv(data / "members.csv")
    print(f"Loaded {len(books.books)} books from books.csv")
    print(f"Loaded {len(members.members)} members from members.csv")
    books.members = members.members
    library = build_library(books)

    # ------------------------------------------------------------
    # Core 2: save as CSV and JSON, then load the CSV back and compare
    # ------------------------------------------------------------
    save_books_csv(library, OUT / "books.csv")
    print(f"Saved {library.book_count} books to out/books.csv")
    save_json(library, OUT / "library.json")
    print(f"Saved {library.book_count} books and {library.member_count} members to out/library.json")

    from_csv = build_library(load_books_csv(OUT / "books.csv"))
    verdict = "same as before" if same_books(library, from_csv) else "DIFFERENT"
    print(f"Reloaded out/books.csv: {from_csv.book_count} books, {verdict}")

    # ------------------------------------------------------------
    # Core 3: a missing file and a corrupt CSV
    # ------------------------------------------------------------
    try_load("missing.csv", load_books_csv, data / "missing.csv")
    try_load("books_corrupt.csv", load_books_csv, data / "books_corrupt.csv")

    # ------------------------------------------------------------
    # Stretch: read the JSON back, cope with broken JSON, and keep
    # loans across a restart
    # ------------------------------------------------------------
    if "--stretch" in sys.argv:
        print("Stretch")
        from_json = build_library(load_json(OUT / "library.json"))
        same = same_books(library, from_json) and same_members(library, from_json)
        verdict = "same as before" if same else "DIFFERENT"
        print(f"Reloaded out/library.json: {from_json.book_count} books and {from_json.member_count} members, "
              f"{verdict}")
        try_load("library_corrupt.json", load_json, data / "library_corrupt.json")
        library.borrow(101, 4)
        library.borrow(101, 7)
        save_json(library, OUT / "library.json")
        restarted = build_library(load_json(OUT / "library.json"))
        print(f"after restart: {restarted.find_member(101)}")
        print(f"after restart: {restarted.find_by_id(4)}")


if __name__ == "__main__":
    main()
