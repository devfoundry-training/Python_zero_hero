# Task 05: Classes

## Goal

Replace the loose records and maps with three classes that look after their own data: `Book`, `Member` and
`Library`.

## What this session taught

Classes and objects, constructors, fields and methods, encapsulation (private data behind methods or properties),
validation, and a readable text form of an object (to-string).

## Core

1. `Book` holds `id`, `title`, `author`, `year`, `genre`, `copies` and a private count of copies on loan. It has
   `available` (copies minus on loan), `lend()` and `take_back()`, each returning true or false, and a to-string.
2. `Member` holds `id`, `name`, `email`, `type`, `joined` and the list of book ids it has on loan, plus a
   to-string.
3. Both constructors validate their input and refuse bad values by throwing the language's standard "invalid
   argument" error with exactly these messages:
   - `book id must be positive` (id 0 or less)
   - `title must not be blank` (empty or only spaces)
   - `year must be between 1450 and 2100`
   - `copies must not be negative`
   - `member type must be standard, student or staff`
   (Your own exception classes come in task 07.)
4. `Library` holds the books and members, keyed by id, and has `add_book`, `add_member`, `find_by_id` (returns the
   book or "not found", see Language notes), `find_member`, `find_by_title(text)` (titles containing the text,
   ignoring case, in id order), `borrow(member_id, book_id)` and `return_book(member_id, book_id)`. `borrow` and
   `return_book` return true or false:
   - borrow fails if the member or the book is unknown, or no copy is available
   - return fails if the member or the book is unknown, or the member does not have that book on loan
5. Load the twenty books and nine members from the CSV lines (constants, as in task 04) and run the script in
   Output format.

## Stretch

1. Equality: two `Book` objects are equal when their ids are equal, whatever the other fields say.
2. Natural order: books sort by title A-Z (ignoring case), then by year. Print the first five.
3. `Library.available_books()` returns the books with at least one copy available.

## Challenge

1. Make every field read-only from outside the class, except through methods that keep the rules.
2. Add `Member.joined` validation: it must be a real date in the form YYYY-MM-DD (no date library yet: check the
   pattern and the month and day ranges yourself).

## Data contract

| Class | Field | Type | Rule |
|---|---|---|---|
| Book | `id` | integer | greater than 0 |
| Book | `title` | text | not blank |
| Book | `author` | text | |
| Book | `year` | integer | 1450 to 2100 |
| Book | `genre` | text | |
| Book | `copies` | integer | 0 or more |
| Book | on loan | integer | private, 0 to copies |
| Member | `id` | integer | greater than 0 |
| Member | `name` | text | not blank; two members can share a name (identity is the id) |
| Member | `email` | text | |
| Member | `type` | text | `standard`, `student` or `staff` |
| Member | `joined` | date YYYY-MM-DD | kept as text in this task |
| Member | `loans` | list of integer | book ids on loan |

`data/members.csv` has the fields `id,name,email,type,joined`.

## Output format

`expected.txt` is the exact output. The script and the rules behind it:

- `Library: 20 books, 9 members`
- The to-string of book 4, then of member 101:
  - Book: `#ID TITLE by AUTHOR (YEAR), AVAILABLE of COPIES available`
  - Member: `#ID NAME (TYPE), N loans` (`1 loan` for one)
- `Find "the": N books` (or `1 book`) then each book's to-string indented by two spaces; `Find "zzz": no books`.
- `Find id 99: not found`
- `Borrowing`, then for each of these, `ACTION MEMBER BOOK: OK` or `ACTION MEMBER BOOK: refused`:
  `borrow 101 4`, `borrow 101 3`, `borrow 999 1`, `borrow 101 99`, `borrow 102 5`, `borrow 103 5`,
  `return 101 4`, `return 101 4`
- `After borrowing`, then the to-strings of book 4, book 5, member 101 and member 102.
- `Validation`, then `Rejected: MESSAGE` for each attempt, in this order: a book with id 0; a book with title
  `"   "`; a book with year 3000; a book with copies -1; a member with type `visitor`.

## How to check

```
python tasks/check/check.py 05 -- <the command that runs your program>
```

## Language notes

- **Python:** `@dataclass` with checks in `__post_init__`, raising `ValueError(message)`. A leading underscore
  (`_on_loan`) marks private by convention; `@property` gives read-only `available`. To-string is `__str__`.
  Not found is `None`: `def find_by_id(self, book_id: int) -> Book | None`.
- **Java:** `private final` fields, a constructor that throws `IllegalArgumentException(message)`, getters, and
  `toString()`. Not found is `Optional<Book>` (`Optional.ofNullable(map.get(id))`).
- **C#:** properties with `private set` (or `init`), a constructor that throws `new ArgumentException(message)`.
  Do not pass a parameter name: it adds `(Parameter 'x')` to the message. To-string is `override ToString()`. Not
  found is `null` (`Book?`) or the `bool TryFindById(int id, out Book book)` pattern.
- **C++:** `private` members, a constructor that throws `std::invalid_argument(message)`, read with `e.what()`.
  To-string is a `to_string()` member or `operator<<`. Not found: return `const Book*` (`nullptr` when missing)
  or `std::optional<std::reference_wrapper<const Book>>`; `std::optional<Book&>` is not allowed.
- **JavaScript:** `class Book` with `#private` fields and `get available()`, throwing `new RangeError(message)`
  (or `TypeError`). To-string is `toString()`; template strings call it. Not found is `undefined` (what
  `Map.get` returns). Document fields with JSDoc (`/** @type {number} */`).
