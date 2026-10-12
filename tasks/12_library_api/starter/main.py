# ============================================================
# Task 12 - Expose the library (starter)
# ============================================================
# Session 12: APIs. Builds on task 11 (library.py and storage.py
# are the task 11 solution, reservations included). The HTTP work
# goes in api.py, the Stretch client in openlibrary.py.
#
# Run the server from the repo root:
#   python tasks/12_library_api/starter/main.py tasks/data [PORT]
# Check it:
#   python tasks/check/check.py 12 -- python tasks/12_library_api/starter/main.py tasks/data {port}
# Stretch, offline:
#   python tasks/12_library_api/starter/main.py --summarise tasks/data/openlibrary_dune.json
# ============================================================

import sys
from datetime import date
from pathlib import Path
from typing import Final

import openlibrary
from api import serve
from storage import load_all

DEFAULT_PORT: Final[int] = 8080
TODAY: Final[date] = date(2026, 10, 12)


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "--summarise":
        text = Path(sys.argv[2]).read_text(encoding="utf-8")
        print("\n".join(openlibrary.summarise(text)))
        return

    args = sys.argv[1:]
    data = Path(args[0]) if len(args) > 0 else Path("tasks/data")
    port = int(args[1]) if len(args) > 1 else DEFAULT_PORT

    # Every start loads a fresh library from the CSV files
    server = serve(load_all(data), TODAY, port)
    print(f"Library API on http://localhost:{server.server_address[1]}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as error:
        print(error)  # the first piece still to write
