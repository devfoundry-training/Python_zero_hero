# Task 04: Dynamic catalogue

## Goal

Grow from ten fixed books to the whole catalogue of twenty, held in collections that grow and shrink: a list of
books, a map from genre to titles, a set of authors and counters for borrowing.

## What this session taught

Lists (dynamic arrays), maps (dictionaries), sets, adding and removing items, looking up by key, iterating over
each kind of collection, and sorting.

## Core

1. Your program starts with the lines of `data/books.csv` as a constant list of strings, header line first (reading
   files comes in task 08). Split each data line on commas into a simple book record and add it to a list. Print
   `Loaded N books`.
2. Build a map from genre to the list of titles in that genre (titles in id order). Print the genres in A-Z order,
   each with its count and titles.
3. Put every author into a set, so each author appears once. Print the number of unique authors and then the authors
   in A-Z order.
4. Apply the borrowing script below in order. Keep a map from book id to the number of copies on loan.
   A borrow works when copies on loan is less than `copies`; a return works when copies on loan is more than 0.
   Print one line per action.
5. Count the successful borrows, the successful returns and the refused actions, and keep a map from book id to how
   many times it was borrowed and returned. Print the counts, then one line per book that was borrowed at least
   once, by id.

The borrowing script (action, book id):

```
borrow 1, borrow 1, borrow 4, return 1, borrow 3, borrow 7, return 9, borrow 1
```

## Stretch

1. Print the authors with more than one book, in A-Z order, on one line.
2. Count the books per decade (`year / 10 * 10` with integer division, so 1813 is the `1810s`) and print the
   decades in order.
3. Print the biggest genre. A tie goes to the genre that comes first A-Z.

## Challenge

1. Sort all twenty books by title A-Z (ignoring case), then by year, without changing the original list, and print
   them.
2. Write a function that groups any list of books by any field (genre, author, decade) and returns a map.

## Data contract

`data/books.csv`, UTF-8, comma separated, one header row, no quoted fields (no title contains a comma):

| Field | Type | Rule |
|---|---|---|
| `id` | integer | positive, unique |
| `title` | text | not blank |
| `author` | text | not blank; several books share an author |
| `year` | integer | year of first publication |
| `genre` | text | not blank, may contain a space (`Science Fiction`) |
| `copies` | integer | 0 or more |
| `format` | text | `print`, `ebook` or `audio` (used from task 06) |
| `length` | integer | pages for print and ebook, minutes for audio (used from task 06) |

**A-Z order** means comparing the lower-case text character by character (ordinal), never a locale-aware compare.

## Output format

`expected.txt` is the exact output. The rules behind it:

- `Loaded 20 books`
- `Genres (N)`, then per genre `GENRE (N): TITLE, TITLE, ...` (titles joined with a comma and a space).
- `Authors (N unique across 20 books)`, then one author per line.
- `Borrowing`, then per action:
  - `borrow ID: OK, N left` or `return ID: OK, N left` (N is copies minus copies on loan, after the action)
  - `borrow ID: refused, none available`
  - `return ID: refused, none on loan`
- `Counts`, then `borrows: N`, `returns: N`, `refused: N`, then `book ID: borrowed N, returned N` for each book
  borrowed at least once, by id.
- No blank lines, no trailing spaces.

## How to check

```
python tasks/check/check.py 04 -- <the command that runs your program>
```

## Language notes

- **Python:** `list`, `dict` and `set`. A `NamedTuple` makes a light record (`book.title`). `dict.get(key, 0)`
  and `setdefault(key, [])` avoid missing-key errors. Sort with `sorted(names, key=str.lower)`.
- **Java:** `ArrayList`, `HashMap` and `HashSet`, or `TreeMap` / `TreeSet` with
  `String.CASE_INSENSITIVE_ORDER` to keep keys sorted. A one-line `record Book(int id, String title, ...)` is
  the record. `map.merge(id, 1, Integer::sum)` counts. Parse numbers with `Integer.parseInt`.
- **C#:** `List<T>`, `Dictionary<TKey, TValue>` and `HashSet<T>`. Sort with
  `StringComparer.OrdinalIgnoreCase` (not the default comparer, which is culture-aware). A one-line
  `record Book(int Id, string Title, ...)` is the record. `TryGetValue` reads a key that might be missing.
- **C++:** `std::vector`, `std::map` and `std::set`. `std::map` and `std::set` sort by byte value, which matches
  A-Z for this data; write a case-insensitive comparator anyway. A `struct Book` is the record. Split lines with
  `std::getline(stream, field, ',')` on a `std::istringstream`; `std::stoi` parses numbers.
- **JavaScript:** `Array`, `Map` and `Set` (a `Map` keeps insertion order; plain objects are fine too). Sort by
  comparing `a.toLowerCase()` with `b.toLowerCase()` using `<` and `>` (return -1, 1 or 0), never `localeCompare`,
  which can ignore spaces and punctuation depending on the locale. Parse numbers with `Number(text)`. A plain object is the record.
