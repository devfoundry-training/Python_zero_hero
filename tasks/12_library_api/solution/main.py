# ============================================================
# Task 12 - Expose the library (solution, Core + Stretch)
# ============================================================
# Session 12: APIs. Builds on task 11.
#
# Run the server from the repo root:
#   python tasks/12_library_api/solution/main.py DATA_DIR [PORT] [TODAY]
#   (PORT defaults to 8080, TODAY to 2026-10-12)
# Then try:  curl http://localhost:8080/books?title=the
# Stop it with Ctrl+C.
#
# Stretch, offline (prints the summary of a saved Open Library response):
#   python tasks/12_library_api/solution/main.py --summarise FILE
# Stretch, online:
#   python tasks/12_library_api/solution/main.py --lookup TITLE
# ============================================================

import sys
from datetime import date
from pathlib import Path
from typing import Final

import openlibrary
from api import serve
from storage import load_all

DEFAULT_PORT: Final[int] = 8080
DEFAULT_TODAY: Final[date] = date(2026, 10, 12)


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "--summarise":
        text = Path(sys.argv[2]).read_text(encoding="utf-8")
        print("\n".join(openlibrary.summarise(text)))
        return
    if len(sys.argv) == 3 and sys.argv[1] == "--lookup":
        try:
            print("\n".join(openlibrary.summarise(openlibrary.search(sys.argv[2]))))
        except OSError as error:
            print(f"Open Library did not answer: {error}")
        return

    args = sys.argv[1:]
    data = Path(args[0]) if len(args) > 0 else Path("tasks/data")
    port = int(args[1]) if len(args) > 1 else DEFAULT_PORT
    today = date.fromisoformat(args[2]) if len(args) > 2 else DEFAULT_TODAY

    # Every start loads a fresh library from the CSV files, so every
    # run of the check sees the same data
    server = serve(load_all(data), today, port)
    print(f"Library API on http://localhost:{server.server_address[1]} (today is {today.isoformat()})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
