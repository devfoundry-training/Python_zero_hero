# ============================================================
# Task 12 starter - api: the library over HTTP, JSON in and out
# ============================================================
# Core endpoints:
#   GET  /books              every book, by id
#   GET  /books?title=TEXT   books whose title contains TEXT (any case)
#   POST /loans              {"member_id": 101, "book_id": 4}
#   anything else            404 {"error": "not found"}
# Every response is JSON with Content-Type: application/json.
# ============================================================

import json
import threading
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlsplit

from library import Book, Library

BAD_BODY = "body must be a JSON object with whole-number member_id and book_id"


def book_json(library: Library, book: Book) -> dict[str, Any]:
    """The book object from the brief; available is library.free_copies(book.id)."""
    raise NotImplementedError("not implemented: book_json")


class LibraryApi:
    """The HTTP-free part: takes simple values, returns (status, body)."""

    def __init__(self, library: Library, today: date) -> None:
        self.library = library
        self.today = today
        # Requests arrive on several threads: hold this lock while
        # reading or changing the library
        self.lock = threading.Lock()

    def list_books(self, title: str | None) -> tuple[int, Any]:
        raise NotImplementedError("not implemented: LibraryApi.list_books")

    def create_loan(self, body: bytes) -> tuple[int, Any]:
        """201 and the loan, or 400 / 404 / 409 with {"error": MESSAGE}."""
        raise NotImplementedError("not implemented: LibraryApi.create_loan")


def make_handler(api: LibraryApi) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def send_json(self, status: int, body: Any) -> None:
            payload = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:
            # TODO: urlsplit(self.path) gives the path and the query;
            # parse_qs(query) decodes %20. Call api.list_books.
            self.send_json(404, {"error": "not found"})

        def do_POST(self) -> None:
            # TODO: read Content-Length bytes from self.rfile and call
            # api.create_loan for /loans
            self.send_json(404, {"error": "not found"})

    return Handler


def serve(library: Library, today: date, port: int) -> ThreadingHTTPServer:
    """Create the server (not yet running). Port 0 picks a free port."""
    raise NotImplementedError("not implemented: serve")
