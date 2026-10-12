# Task 06: Book types and loan policies

## Goal

Teach the library that books come in different formats and members follow different rules, without filling the
code with `if format == ...` checks.

## What this session taught

Inheritance, abstract classes, interfaces, overriding, polymorphism (one call, different behaviour), and factory
functions.

## Core

1. Make `Book` abstract. It gains a `length` field (integer, must be positive: `length must be positive`) and two
   abstract members: `format_name` and `length_text()`. It also gets `describe()`, written once in `Book`, that
   returns `#ID TITLE: FORMAT, LENGTH TEXT`.
2. Three concrete types:
   - `PrintBook`: format `print`, length text `N pages`
   - `EBook`: format `ebook`, length text `N pages`
   - `AudioBook`: format `audio`, length in minutes shown as `Hh MMm` (1150 is `19h 10m`, 480 is `8h 00m`)
3. A factory, `make_book(fields)`, reads the `format` column and builds the right type. An unknown format is
   refused with `format must be print, ebook or audio, got 'FORMAT'`.
4. A `LoanPolicy` interface with `loan_days()`, `fine_per_day()` (pence) and `max_loans()`, plus
   `fine_for(days_late)` (days late times the daily fine, never below 0). Three implementations:

   | Policy | Loan days | Fine per day | Max loans |
   |---|---|---|---|
   | standard | 14 | 25p | 3 |
   | student | 21 | 10p | 5 |
   | staff | 28 | 0p | 10 |

5. Each `Member` gets the policy for its `type` when it is created. `Library.borrow` now also fails when the member
   already has `max_loans()` books.
6. Run the script in Output format.

## Stretch

1. Add a `guest` policy (7 days, 50p a day, 1 loan) without changing `Library` or `Member` (only the code that maps
   a type name to a policy).
2. Count the books per format by calling `format_name` (no type checks such as `instanceof` / `isinstance`).

## Challenge

1. Add a `ReferenceBook` type that can never be lent. Where does that rule belong: in `Book`, in `Library`, or in
   the policy? Justify your choice in a comment.
2. A member could hold more than one role (a student who is also staff). Sketch two designs (inheritance versus
   composition) and say which you would choose.

## Data contract

Book gains:

| Field | Type | Rule |
|---|---|---|
| `format` | text | `print`, `ebook` or `audio`; decides the class |
| `length` | integer | greater than 0; pages for print and ebook, minutes for audio |

LoanPolicy:

| Member | Type |
|---|---|
| `name` | text (`standard`, `student`, `staff`) |
| `loan_days()` | integer |
| `fine_per_day()` | money (integer pence) |
| `max_loans()` | integer |
| `fine_for(days_late)` | money (integer pence) |

Money is always whole pence in an integer. It is shown as `£` + pounds + `.` + two-digit pence: 25 is `£0.25`,
125 is `£1.25`, 0 is `£0.00`. Work out pounds and pence with integer division and remainder by 100.

## Output format

`expected.txt` is the exact output. The script and the rules behind it:

- `Formats`, then `describe()` for all twenty books, by id.
- `Policies`, then one line per policy (standard, student, staff):
  `NAME: N days, £X.XX a day, up to N loans` (`no fines` instead of `£0.00 a day`).
- `Fine for 3 days late`, then `NAME: £X.XX` per policy.
- `Limits`, then for each borrow below `borrow MEMBER BOOK: OK, due in N days` (N from the member's policy) or
  `borrow MEMBER BOOK: refused`: `101 1`, `101 2`, `101 4`, `101 7`, `102 7`, `103 7`.
- No blank lines, no trailing spaces.

## How to check

```
python tasks/check/check.py 06 -- <the command that runs your program>
```

## Language notes

- **Python:** `from abc import ABC, abstractmethod`. `LoanPolicy(ABC)` is the interface; a class attribute
  `format_name = "print"` can satisfy an abstract property. Divide money with `//` and `%`, and pad pence with
  `f"{pence % 100:02d}"`.
- **Java:** `abstract class Book` and `interface LoanPolicy` (a `default` method can hold `fineFor`).
  `String.format("£%d.%02d", pence / 100, pence % 100)`.
- **C#:** `abstract class Book` with `abstract string FormatName { get; }` and `interface ILoanPolicy` (a default
  interface method can hold `FineFor`). `$"£{pence / 100}.{pence % 100:D2}"`. Set
  `Console.OutputEncoding = System.Text.Encoding.UTF8;` at the start of `Main` so `£` comes out as UTF-8.
- **C++:** `Book` has pure virtual functions (`= 0`) and a `virtual ~Book() = default;`. `Library` owns the books
  as `std::vector<std::unique_ptr<Book>>` (or a map of `unique_ptr`): one owner, no `delete`, and no slicing. Hand
  out `const Book&` or `const Book*`, never ownership. `make_book` returns `std::unique_ptr<Book>`. Policies can be
  three `static` objects that members point to. `£` is two bytes in UTF-8: never pad a string containing it with
  `setw` (this task never does). Compile MSVC with `/utf-8`.
- **JavaScript:** no `abstract` or `interface` keywords: make the base methods throw `new Error("not
  implemented")`, and describe the interface with JSDoc (`@interface`, `@implements`). Money is still a whole
  number of pence: `Math.floor(pence / 100)` and `String(pence % 100).padStart(2, "0")`.
