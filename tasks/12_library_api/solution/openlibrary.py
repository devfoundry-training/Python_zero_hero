# ============================================================
# Task 12 Stretch - consuming a public API: Open Library search
# ============================================================
# https://openlibrary.org/search.json?title=dune
# Two halves, kept apart on purpose:
#   * summarise() turns response TEXT into lines. No network, so
#     it is checked against the recorded data/openlibrary_dune.json
#   * search() does the HTTP call. It needs the network, so it is
#     never part of a check
# ============================================================

import json
import urllib.parse
import urllib.request
from typing import Any, Final

SEARCH_URL: Final[str] = "https://openlibrary.org/search.json"
FIELDS: Final[str] = "key,title,author_name,first_publish_year,edition_count,number_of_pages_median"


def search(title: str, limit: int = 3, timeout: float = 10.0) -> str:
    """Return the raw JSON text. Raises OSError (URLError is one) when
    the network or Open Library lets us down."""
    query = urllib.parse.urlencode({"title": title, "limit": limit, "fields": FIELDS})
    request = urllib.request.Request(f"{SEARCH_URL}?{query}",
                                     headers={"User-Agent": "ZeroToHeroLibrary/1.0 (teaching example)"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def first_match(text: str) -> dict[str, Any] | None:
    """The first result as a small dict for the API, or None."""
    docs = json.loads(text).get("docs", [])
    if not docs:
        return None
    doc = docs[0]
    return {
        "key": doc.get("key"),
        "title": doc.get("title"),
        "authors": doc.get("author_name", []),
        "first_publish_year": doc.get("first_publish_year"),
        "edition_count": doc.get("edition_count"),
    }


def summarise(text: str) -> list[str]:
    """Lines describing a search response. Any field can be missing
    from a real response, so every read has a fallback."""
    document = json.loads(text)
    lines = [f"Open Library search: {document.get('numFound', 0)} results"]
    for number, doc in enumerate(document.get("docs", []), start=1):
        authors = ", ".join(doc.get("author_name", [])) or "unknown author"
        year = doc.get("first_publish_year", "unknown")
        editions = doc.get("edition_count", 0)
        lines.append(f"{number}. {doc.get('title', 'untitled')} by {authors}, first published {year}, "
                     f"{editions} editions, {doc.get('key', 'no key')}")
    return lines
