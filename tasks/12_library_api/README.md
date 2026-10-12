# Task 12: Expose the library

## Goal

Put the library on the network: a small REST API that lists, searches and lends books as JSON. Then, as a
Stretch, be a client of someone else's API.

## What this session taught

HTTP requests and responses, methods (`GET`, `POST`), paths and query strings, status codes, headers, JSON bodies,
running a server, and calling a public API as a client (timeouts, errors, untrusted data).

## Core

1. The program takes the data folder as its first argument (default `tasks/data`) and the port as an optional
   second argument (default `8080`). It loads a fresh library from the CSV files on every start (books, members and
   loans, as in task 09), so every run starts the same. "Today" is fixed at `2026-10-12`.
2. Listen on `localhost` and answer these requests. Every response, errors included, has the header
   `Content-Type: application/json` and a JSON body.

   | Request | Success | Errors |
   |---|---|---|
   | `GET /books` | `200`, array of every book, by id | |
   | `GET /books?title=TEXT` | `200`, array of the books whose title contains TEXT, ignoring case, by id (an empty array if none). TEXT is URL-encoded: `war%20of` means `war of` | |
   | `POST /loans` with body `{"member_id": 101, "book_id": 4}` | `201`, the new loan | `400` bad body, `404` unknown member or book, `409` refused by a rule |
   | anything else | | `404` `{"error": "not found"}` |

3. `POST /loans` uses the task 09 rules and messages: check the member, then the book, then the limit, then the
   copies. The body must be a JSON object whose `member_id` and `book_id` are whole numbers (not strings, not
   decimals); anything else is a `400` with
   `{"error": "body must be a JSON object with whole-number member_id and book_id"}`.
4. The new loan's id is the highest loan id plus 1; it is borrowed today and its due date comes from the member's
   policy.
5. Book objects show `available` as copies minus open loans (minus copies held for reservations, if you kept task 11's
   reservations).

## Stretch

Consume a public API: Open Library's search, `https://openlibrary.org/search.json?title=TITLE`. It returns JSON with
`numFound` and a `docs` array; each doc may have `title`, `author_name` (array of text), `first_publish_year`,
`edition_count` and `key`. Any field can be missing.

1. Write a function `summarise(json_text)` that turns a search response into the lines below. It takes **text**, not
   a URL, so it can be checked offline against the recorded response in `data/openlibrary_dune.json` (the check
   never touches the network):
   ```
   Open Library search: NUM_FOUND results
   1. TITLE by AUTHOR, AUTHOR, first published YEAR, N editions, KEY
   ```
   with `unknown author` when `author_name` is missing or empty, `first published unknown` when there is no year,
   `0 editions` when there is no count. Run it from your program with `--summarise FILE`.
2. Add `GET /books/ID`: `200` and the book, or `404` `{"error": "no book with id ID"}`.
3. Add `GET /books/ID/openlibrary`: search Open Library for the book's title (live, with a timeout of 10 seconds and
   `&limit=1`) and return `200`
   `{"id": 4, "title": "Dune", "open_library": {"key": ..., "title": ..., "authors": [...], "first_publish_year": ..., "edition_count": ...}}`
   (`"open_library": null` when there are no results), or `502` `{"error": "Open Library did not answer"}` when the
   call fails or times out.

## Challenge

1. Cache Open Library answers in memory for 10 minutes, so the same title is fetched once.
2. Add `POST /returns` and `GET /members/ID/loans`, and write the request and response examples a client
   developer would need.

## Data contract

Book object (keys in any order):

```json
{"id": 4, "title": "Dune", "author": "Frank Herbert", "year": 1965, "genre": "Science Fiction",
 "format": "print", "copies": 4, "available": 3}
```

Loan object (`201` response):

```json
{"id": 13, "book_id": 4, "member_id": 101, "borrowed": "2026-10-12", "due": "2026-10-26"}
```

Error object: `{"error": "MESSAGE"}` with the task 07 messages, for example `no book with id 99`,
`The Hobbit has no copies available`, `Ella Brown already has 3 loans (limit 3)`.

Integers are JSON numbers, text is JSON strings, dates are strings `YYYY-MM-DD`.

## Output format

The check is a scripted conversation, not your program's stdout. The checker starts your server on a free port,
sends the 15 requests in `check/api_script.json` in order (state carries over: the second loan in the script sees
the first), and writes down each request, the status code, whether the content type is JSON, and the body as JSON
with sorted keys and no spaces (arrays one item per line). That transcript must match `expected.txt` exactly, so
key order and spacing in your JSON do not matter, but every value does. Your server's own console output is
ignored. The checker stops the server afterwards.

For the Stretch, `expected_stretch.txt` is the exact output of `--summarise data/openlibrary_dune.json`.

## How to check

```
python tasks/check/check.py 12 -- <the command that runs your server> tasks/data {port}
python tasks/check/check.py 12_stretch -- <the command that runs your program> --summarise tasks/data/openlibrary_dune.json
```

`{port}` is replaced with the free port the checker picked.

## Language notes

- **Python:** `http.server` (`ThreadingHTTPServer` and a `BaseHTTPRequestHandler` with `do_GET` / `do_POST`),
  `urllib.parse` for the path and query (`parse_qs` decodes `%20`), `json` for bodies. Requests can arrive on several
  threads: guard the library with a `threading.Lock`. Stretch client: `urllib.request.urlopen(url, timeout=10)`.
- **Java:** `com.sun.net.httpserver.HttpServer` is in the JDK (see the repo's `apis` topic): one `HttpContext` per
  path, read `exchange.getRequestURI()`, send with `sendResponseHeaders(status, bytes.length)`. Decode the query
  with `URLDecoder.decode(text, StandardCharsets.UTF_8)`. No JSON in the JDK: write it by hand and read the two-field
  body with a small parser or a regular expression, or add Jackson / Gson through Maven. Stretch client:
  `java.net.http.HttpClient` with `.timeout(Duration.ofSeconds(10))`.
- **C#:** an ASP.NET Core minimal API (`Microsoft.NET.Sdk.Web`, part of the .NET SDK, no NuGet):
  `app.MapGet("/books", ...)`, `app.MapPost("/loans", ...)`, `Results.Json(value, statusCode: 409)`, and
  `app.MapFallback(...)` for the `404`. Read the body yourself with `JsonDocument` so a bad body becomes your `400`.
  Pass the port with `app.Run($"http://localhost:{port}")`. Stretch client: `HttpClient` with `Timeout`.
- **C++:** no extra libraries. Core: a minimal HTTP/1.1 server on raw operating system sockets (Winsock2 on
  Windows, POSIX sockets elsewhere): accept a connection, read the request line and headers, read
  `Content-Length` bytes of body, answer with a status line, `Content-Type`, `Content-Length` and the body, then
  close. Only the three endpoints; decode `%XX` in the query yourself; write the JSON by hand and parse the
  two-field body by hand. Stretch: call the system `curl` (`curl.exe` ships with Windows 10 and later, macOS and
  Linux) through `_popen` / `popen` with `--max-time 10`, and parse the JSON by hand (or use the recorded sample
  file for the check). WinHTTP is an optional Windows-only alternative.
- **JavaScript:** `node:http` (`http.createServer((req, res) => ...)`), `new URL(req.url, "http://localhost")` for
  the path and `searchParams.get("title")` (decodes `%20`), collect the body from the `data` events, `JSON.parse`
  inside `try`. Stretch client: the built-in `fetch` with `AbortSignal.timeout(10000)`.
