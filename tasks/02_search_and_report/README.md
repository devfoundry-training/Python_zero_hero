# Task 02: Search and report

## Goal

Make the bookshelf from task 01 useful: a neat report table, a search that ignores case, and some facts about the
titles.

## What this session taught

`for`, `while` and for-each loops, `break` and `continue`, and working with strings: length, case, searching
inside a string, splitting, padding and formatting.

## Core

Use the same ten books and fixed arrays as task 01.

1. Print a report table with a header row, a row of dashes and one row per book (see Output format for the exact
   column widths and alignment).
2. Search the titles for each of these three terms, in this order: `the`, `TIME`, `zzz`. The search ignores case
   and matches anywhere in the title. Collect the matching titles with a `while` loop into a fixed array plus a
   count, then print them in array order.
3. Count the words in all ten titles together. Words are separated by spaces; `Eighty-Four` is one word.
4. Find the longest title (most characters). If two are equally long, the first one in the array wins.

## Stretch

1. Print the initials of every title in capitals (`Pride and Prejudice` gives `PAP`).
2. Find the shortest title (the first one wins a tie).
3. Print a compact list where titles longer than 20 characters are cut to their first 17 characters plus `...`.

## Challenge

1. Print each title centred in a 40-character banner made of `*` characters.
2. Word-wrap the longest title so no line is longer than 12 characters, breaking only at spaces.

## Data contract

The same ten books as task 01:

| Field | Type | Rule |
|---|---|---|
| `id` | integer | 1 to 10, unique |
| `title` | text | not blank, ASCII only |
| `year` | integer | year of first publication |
| `copies` | integer | 0 or more |

## Output format

`expected.txt` is the exact output. The rules behind it:

- `Report`, then the table. Four columns separated by two spaces:
  - `ID`: width 2, right-aligned
  - `Title`: width 30, left-aligned (padded with spaces on the right)
  - `Year`: width 4
  - `Copies`: width 6, right-aligned
  The header uses the same widths. The second row is dashes the width of each column (2, 30, 4, 6).
- For each term: `Search "TERM": N matches` (or `1 match`) followed by each title indented by two spaces, or
  `Search "TERM": no matches`. TERM is printed exactly as given, quotes are straight double quotes.
- `Words in titles: N`
- `Longest title: TITLE (N characters)`
- No blank lines, no trailing spaces.

## How to check

```
python tasks/check/check.py 02 -- <the command that runs your program>
```

## Language notes

- **Python:** f-strings pad for you: `f"{title:<30}"` (left), `f"{n:>6}"` (right). Lower-case with `.lower()`
  and test with `in`. `title.split()` splits on any run of spaces.
- **Java:** `String.format("%2d  %-30s  %-4d  %6d", ...)` pads (`-` means left-aligned). Use
  `title.toLowerCase(Locale.ROOT).contains(term.toLowerCase(Locale.ROOT))`. Words: `title.trim().split("\\s+")`.
  `"-".repeat(30)` makes the dashes.
- **C#:** `$"{id,2}  {title,-30}  {year,-4}  {copies,6}"` pads (negative width means left-aligned). Search with
  `title.Contains(term, StringComparison.OrdinalIgnoreCase)`. Words:
  `title.Split(' ', StringSplitOptions.RemoveEmptyEntries)`. `new string('-', 30)` makes the dashes.
- **C++:** `std::format("{:>2}  {:<30}  {:<4}  {:>6}", ...)` (C++20) or `std::setw` with `std::left` /
  `std::right`. Lower-case one `char` at a time with `std::tolower(static_cast<unsigned char>(c))`, then use
  `find(...) != std::string::npos`. Count words with a `std::istringstream` and `>>`.
- **JavaScript:** `String(id).padStart(2)`, `title.padEnd(30)`. Search with
  `title.toLowerCase().includes(term.toLowerCase())`. Words: `title.trim().split(/\s+/)`. `"-".repeat(30)` makes
  the dashes.
