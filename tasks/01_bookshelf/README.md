# Task 01: Bookshelf

## Goal

Start the Library Manager: keep ten books in fixed-size arrays, print the catalogue, flag the old books, sort them
into centuries and add up the totals.

## What this session taught

Data types, variables and constants, arithmetic and comparison operators, `if` / `else`, `switch` / `match`, and
fixed-size arrays. A simple `for` loop over an array is fine here; loops are covered properly in task 02.

## Core

1. Store the ten books below in four fixed-size arrays of length 10, one per field (`ids`, `titles`, `years`,
   `copies`). Position `i` in every array describes the same book. Keep the size in a constant.
2. Print the catalogue: one line per book, in array order, in the format shown under Output format.
3. Describe the copies with `if` / `else`: `out of stock` for 0, `1 copy` for 1, `N copies` otherwise.
4. Work out the century with `switch` / `match` on `year / 100` (integer division): 17 is `18th century`,
   18 is `19th century`, 19 is `20th century`, 20 is `21st century`, anything else is `unknown era`.
5. Flag every book published before 1950 by adding ` | pre-1950` to the end of its line.
6. "Remove" every book with an even id. A fixed array cannot shrink, so copy the odd-id books into a second pair
   of arrays (ids and titles) of the same size and keep a count of the slots used. Print them.
7. Print the totals: number of books, total copies, books out of stock, books before 1950, and the average year
   using integer division (it rounds down).

## Stretch

1. Find the oldest and the newest book and print them.
2. Count the books in each century, using the same `switch` / `match` as Core step 4.

## Challenge

1. Sort a copy of the arrays by year, oldest first, with your own sort (bubble sort or insertion sort): when you
   swap two books, swap them in every array.
2. Why do parallel arrays get harder to manage as fields are added? Write two sentences in a comment. (Task 05
   answers this with classes.)

## Data contract

The ten books, hard-coded in your program (they are the first ten rows of `data/books.csv`):

| Field | Type | Rule |
|---|---|---|
| `id` | integer | 1 to 10, unique |
| `title` | text | not blank |
| `year` | integer | year of first publication |
| `copies` | integer | 0 or more |

| id | title | year | copies |
|---|---|---|---|
| 1 | Pride and Prejudice | 1813 | 3 |
| 2 | Nineteen Eighty-Four | 1949 | 2 |
| 3 | The Hobbit | 1937 | 0 |
| 4 | Dune | 1965 | 4 |
| 5 | Robinson Crusoe | 1719 | 1 |
| 6 | The Time Machine | 1895 | 2 |
| 7 | Animal Farm | 1945 | 5 |
| 8 | Emma | 1815 | 1 |
| 9 | The Left Hand of Darkness | 1969 | 0 |
| 10 | Murder on the Orient Express | 1934 | 2 |

## Output format

`expected.txt` is the exact output. The rules behind it:

- `Catalogue (10 books)`, then one line per book:
  `id | title | year | copies text | century`, plus ` | pre-1950` when the year is before 1950.
  Fields are separated by a space, a vertical bar and a space.
- `Odd ids only (N books)`, then `id | title` for each kept book.
- `Totals`, then five lines: `books: N`, `copies: N`, `out of stock: N`, `pre-1950: N`, `average year: N`.
- No blank lines, no trailing spaces.

## How to check

```
python tasks/check/check.py 01 -- <the command that runs your program>
```

The checker prints `PASS`, or `FAIL` with the first line that differs.

## Language notes

- **Python:** lists stand in for arrays: create each with all ten values and never `append` or `remove`.
  `year // 100` is integer division (`/` would give 18.13). Use `match` / `case` (Python 3.10+). Add type hints
  (`ids: list[int] = [...]`) and `Final` for the size.
- **Java:** `int[] ids = {1, 2, ...};` and `String[] titles = {...};` are fixed size already. `/` on two `int`
  values is integer division. Use a switch expression: `case 18 -> "19th century";`.
- **C#:** `int[] ids = { 1, 2, ... };` is fixed size. `/` on two `int` values is integer division. Use a switch
  expression: `18 => "19th century", _ => "unknown era"`.
- **C++:** `std::array<int, 10>` (or a plain C array) with `constexpr std::size_t SIZE = 10;`. `/` on two `int`
  values is integer division. In a classic `switch`, remember `break` (or `return` from a helper function).
- **JavaScript:** arrays always grow, so create each with ten values and never `push` or `splice`. All numbers are
  floating point: use `Math.floor(year / 100)` for integer division. `switch` needs `break` (or `return`).
  Add `// @ts-check` and JSDoc (`/** @type {number[]} */`) to get type checking in the editor.
