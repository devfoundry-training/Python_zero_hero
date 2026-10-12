# Task 08: Persistence

## Goal

Stop copying the data into the program: read the real files, save the library as CSV and JSON, and keep going when
a file is missing or damaged.

## What this session taught

Reading and writing text files, paths, file encodings (UTF-8), CSV, JSON, closing files safely (`with` / `try`
with resources / `using` / RAII), and handling I/O errors.

## Core

1. The program takes the data folder as its first command-line argument (default `tasks/data`). Load
   `books.csv` and `members.csv` from it, replacing the constants used in tasks 04 to 07. Use the task 07 classes.
2. Save the books to `out/books.csv` (same header and columns as `data/books.csv`, `\n` line endings) and the whole
   library to `out/library.json` (shape below). `out` is a folder in the current directory; create it if needed.
3. Load `out/books.csv` back and compare it with the library in memory: same ids, in the same order, with the same
   field values. Print `same as before` or `DIFFERENT`.
4. Try to load `missing.csv` from the data folder. It does not exist: catch the error, print a message and carry
   on with an empty catalogue.
5. Load `books_corrupt.csv`. Report every bad line and skip it; keep every good line. Checks, in this order, for each
   line:
   1. blank line: skip it silently
   2. the right number of fields (8): `expected 8 fields, found N`
   3. `id`, `year`, `copies` and `length` are whole numbers, checked in that order:
      `year must be a whole number, got 'TEXT'`
   4. the format: `format must be print, ebook or audio, got 'TEXT'` (from the task 06 factory)
   5. the Book rules from tasks 05 and 06, with their messages (for example `copies must not be negative`)
   6. an id already loaded from this file: `duplicate book id ID`

   Line numbers count from 1, and the header is line 1.

## Stretch

1. Load `out/library.json` back and compare books and members with the library in memory.
2. Load `data/library_corrupt.json` (cut off half way) and print `not valid JSON, starting with an empty catalogue`.
3. Make loans survive a restart: after a borrow, save the JSON (each member's `loans` list), then build a new library
   from the file and show that the member still has the loan and the book still has one copy fewer.

## Challenge

1. Save safely: write to `library.json.tmp` first, then rename it over `library.json`, so a crash while saving never
   leaves a half-written file.
2. Titles may one day contain commas. Change the CSV writer and reader to quote fields that contain a comma or a
   double quote (the CSV rules: wrap in `"`, double any `"` inside), and prove it with a title such as
   `Me, Myself and "I"`.

## Data contract

`data/books.csv` and `data/members.csv` as described in tasks 04 and 05: UTF-8, comma separated, one header row, no
quoted fields.

`out/library.json`, UTF-8, two-space indent, keys in this order:

```json
{
  "books": [
    {"id": 1, "title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813,
     "genre": "Classic", "copies": 3, "format": "print", "length": 432}
  ],
  "members": [
    {"id": 101, "name": "Amira Khan", "email": "amira.khan@example.com", "type": "standard",
     "joined": "2023-01-15", "loans": []}
  ]
}
```

Numbers are JSON numbers, text is JSON strings, `loans` is a list of book ids (integers). Books and members are in
id order.

## Output format

`expected.txt` is the exact output. The rules behind it:

- `Loaded N books from books.csv`, `Loaded N members from members.csv`
- `Saved N books to out/books.csv`, `Saved N books and N members to out/library.json`
- `Reloaded out/books.csv: N books, same as before`
- For each extra file, `Loading NAME`, then indented by two spaces either
  `file not found, starting with an empty catalogue`, or one `line N: REASON` per bad line followed by
  `loaded N books, skipped N lines`.
- Paths in the output always use `/`, whatever the operating system.

## How to check

```
python tasks/check/check.py 08 -- <the command that runs your program> tasks/data
```

Run it from the repo root: the program writes `out/` in the current directory (`out/` is in `.gitignore`).

## Language notes

- **Python:** `pathlib.Path`, `open(..., encoding="utf-8", newline="")` with the `csv` module (pass
  `lineterminator="\n"` to the writer), and `json.dump(..., indent=2)`. A missing file raises
  `FileNotFoundError`; broken JSON raises `json.JSONDecodeError`.
- **Java:** `Files.readAllLines(path, StandardCharsets.UTF_8)` and `Files.writeString`; a missing file throws
  `NoSuchFileException`. The JDK has no JSON library: write the JSON yourself with a `StringBuilder` (escape `"`
  and `\` in text). For the Stretch, add Jackson or Gson through Maven, or write a small parser.
- **C#:** `File.ReadAllLines(path)` and `File.WriteAllText(path, text)`; a missing file throws
  `FileNotFoundException`. `System.Text.Json` is built in: `JsonSerializer.Serialize(obj, new
  JsonSerializerOptions { WriteIndented = true })`; broken JSON throws `JsonException`.
- **C++:** `std::ifstream` / `std::ofstream` and `std::filesystem` (`exists`, `create_directories`). Open output
  files with `std::ios::binary` so Windows does not turn `\n` into `\r\n`. There is no JSON in the standard
  library: write it by hand with escaping. Reading JSON back (Stretch) means writing a small parser for this one
  shape; treat it as a Challenge if time is short.
- **JavaScript:** `fs.readFileSync(path, "utf8")` and `fs.writeFileSync`; a missing file throws an error with
  `code === "ENOENT"`. `JSON.stringify(obj, null, 2)` and `JSON.parse` (throws `SyntaxError`) are built in. Split
  lines with `/\r?\n/` in case the file has Windows line endings.
