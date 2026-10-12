# ============================================================
# Task 12 Stretch starter - consuming a public API: Open Library
# ============================================================
# https://openlibrary.org/search.json?title=dune
# Keep the two halves apart:
#   * summarise() turns response TEXT into lines, with no network,
#     so it can be checked against data/openlibrary_dune.json
#   * search() does the HTTP call (urllib.request, timeout 10)
# ============================================================

import json
import urllib.parse
import urllib.request
from typing import Final

SEARCH_URL: Final[str] = "https://openlibrary.org/search.json"


def search(title: str, limit: int = 3, timeout: float = 10.0) -> str:
    """Return the raw JSON text of a title search."""
    raise NotImplementedError("not implemented: openlibrary.search")


def summarise(text: str) -> list[str]:
    """The summary lines from the brief. Any field can be missing."""
    raise NotImplementedError("not implemented: openlibrary.summarise")
