# ============================================================
# Task 12 - api: the library over HTTP, JSON in and out
# ============================================================
# Core endpoints:
#   GET  /books              every book, by id
#   GET  /books?title=TEXT   books whose title contains TEXT (any case)
#   POST /loans              {"member_id": 101, "book_id": 4}
# Stretch endpoints:
#   GET  /books/ID               one book
#   GET  /books/ID/openlibrary   Open Library's first match for it
# ============================================================

import json
import sys
import threading
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlsplit

import openlibrary
from library import (Book, BookNotAvailableError, Library, LibraryError, MemberLimitReachedError,
                     UnknownBookError, UnknownMemberError)

BAD_BODY = "body must be a JSON object with whole-number member_id and book_id"


def book_json(library: Library, book: Book) -> dict[str, Any]:
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "genre": book.genre,
        "format": book.format_name,
        "copies": book.copies,
        "available": library.free_copies(book.id),
    }


class LibraryApi:
    """The HTTP-free part: takes simple values, returns (status, body).
    Keeping this apart from the handler makes it easy to test."""

    def __init__(self, library: Library, today: date) -> None:
        self.library = library
        self.today = today
        # ThreadingHTTPServer runs requests on several threads at once;
        # one lock makes each request see and change the library alone
        self.lock = threading.Lock()

    def list_books(self, title: str | None) -> tuple[int, Any]:
        with self.lock:
            books = self.library.find_by_title(title) if title else self.library.all_books()
            return 200, [book_json(self.library, b) for b in books]

    def get_book(self, book_id: int) -> tuple[int, Any]:
        with self.lock:
            book = self.library.find_by_id(book_id)
            if book is None:
                return 404, {"error": f"no book with id {book_id}"}
            return 200, book_json(self.library, book)

    def create_loan(self, body: bytes) -> tuple[int, Any]:
        try:
            data = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return 400, {"error": BAD_BODY}
        # type(...) is int, not isinstance: in Python True counts as an int
        if not isinstance(data, dict) or type(data.get("member_id")) is not int \
                or type(data.get("book_id")) is not int:
            return 400, {"error": BAD_BODY}
        with self.lock:
            try:
                loan = self.library.borrow(data["member_id"], data["book_id"], self.today)
            except (UnknownMemberError, UnknownBookError) as error:
                return 404, {"error": str(error)}
            except (BookNotAvailableError, MemberLimitReachedError, LibraryError) as error:
                return 409, {"error": str(error)}  # a rule said no: a conflict
            return 201, {
                "id": loan.id,
                "book_id": loan.book_id,
                "member_id": loan.member_id,
                "borrowed": loan.borrowed.isoformat(),
                "due": self.library.due_date(loan).isoformat(),
            }

    def open_library(self, book_id: int) -> tuple[int, Any]:
        with self.lock:
            book = self.library.find_by_id(book_id)
        if book is None:
            return 404, {"error": f"no book with id {book_id}"}
        try:
            match = openlibrary.first_match(openlibrary.search(book.title, limit=1))
        except (OSError, ValueError):
            return 502, {"error": "Open Library did not answer"}
        return 200, {"id": book.id, "title": book.title, "open_library": match}


def make_handler(api: LibraryApi) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def send_json(self, status: int, body: Any) -> None:
            payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:
            url = urlsplit(self.path)
            parts = [p for p in url.path.split("/") if p]
            if parts == ["books"]:
                titles = parse_qs(url.query).get("title")  # parse_qs decodes %20 and +
                self.send_json(*api.list_books(titles[0] if titles else None))
            elif len(parts) == 2 and parts[0] == "books" and parts[1].isdigit():
                self.send_json(*api.get_book(int(parts[1])))
            elif len(parts) == 3 and parts[0] == "books" and parts[1].isdigit() and parts[2] == "openlibrary":
                self.send_json(*api.open_library(int(parts[1])))
            else:
                self.send_json(404, {"error": "not found"})

        def do_POST(self) -> None:
            if urlsplit(self.path).path.rstrip("/") != "/loans":
                self.send_json(404, {"error": "not found"})
                return
            length = int(self.headers.get("Content-Length") or 0)
            self.send_json(*api.create_loan(self.rfile.read(length)))

        def log_message(self, format: str, *args: Any) -> None:
            # Quieter than the default: one short line per request, on stderr
            print(f"{self.command} {self.path} -> {args[1] if len(args) > 1 else ''}", file=sys.stderr)

    return Handler


def serve(library: Library, today: date, port: int) -> ThreadingHTTPServer:
    """Create the server (not yet running). Port 0 picks a free port."""
    return ThreadingHTTPServer(("localhost", port), make_handler(LibraryApi(library, today)))

