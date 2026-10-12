# Task 09: Loans with due dates

## Goal

Give every loan a date: when it was borrowed, when it is due, whether it is overdue, and what the fine is.

## What this session taught

Date types without a time of day, parsing and formatting dates (`YYYY-MM-DD`), adding days, the number of days
between two dates, comparing dates, and why programs should take "today" as an input instead of reading the clock.

## Core

1. The program takes the data folder as its first argument (default `tasks/data`) and **today's date** as an optional
   second argument (default `2026-10-12`). Never read the real clock: the output must be the same on any day.
2. Load `books.csv`, `members.csv` and `loans.csv`. A `Loan` has `id`, `book_id`, `member_id`, `borrowed` and an
   optional `returned` date (empty in the file while the book is still out). Loading an open loan takes a copy off
   the shelf and adds the book to the member's loans (limits are not checked for loans already in the file).
3. The due date is `borrowed` plus the member's policy loan days (task 06).
4. Days late: for a returned loan, `returned - due`; for an open loan, `today - due`; never less than 0. Due today
   is **not** late.
5. The fine is days late times the policy's fine per day (whole pence).
6. Print the loans table, the overdue report and the fines totals (see Output format).
7. Then, on today's date, run: member 105 borrows book 15; member 105 borrows book 16; member 102 returns book 14.
   Use the task 07 exceptions: print `Error: MESSAGE` when one is refused. A new loan's id is the highest loan id
   plus 1.

## Stretch

1. The library is closed on Sundays. List the loans whose due date falls on a Sunday and the Monday it moves to
   (do not change the Core output).
2. List the open loans due within the next 7 days (today to today + 7, inclusive).

## Challenge

1. Cap every fine at £5.00. Where should the cap live so every policy gets it for free?
2. Loans are now stamped with a date and a time (`2026-10-12T17:45`) in UK time. Explain, with an example, why a
   loan taken at 23:30 on the night the clocks go back can be counted as the wrong day, and fix it.

## Data contract

`data/loans.csv`, UTF-8, comma separated, one header row:

| Field | Type | Rule |
|---|---|---|
| `id` | integer | positive, unique |
| `book_id` | integer | an id in books.csv |
| `member_id` | integer | an id in members.csv |
| `borrowed` | date YYYY-MM-DD | |
| `returned` | optional date YYYY-MM-DD | empty while the book is still on loan; not before `borrowed` |

Dates have no time of day and no time zone. Money is integer pence, shown as `£P.PP`.

## Output format

`expected.txt` is the exact output. The rules behind it:

- `Today is YYYY-MM-DD`
- `Loans`, then a table. Columns separated by two spaces:
  `ID` (width 2, right-aligned), `Book` (title, width 30, left), `Member` (name, width 12, left),
  `Borrowed` (10), `Due` (10), `Status` (last column, not padded). Then a row of dashes the width of each column
  (2, 30, 12, 10, 10, and 6 for Status). One row per loan, by id. Status is one of:
  - `returned on time` or `returned N days late`
  - `on loan, N days left`
  - `due today`
  - `overdue by N days`
  (`1 day`, never `1 days`)
- `Overdue on YYYY-MM-DD: N loans`, then one line per overdue open loan, most days late first, then by loan id:
  `N days: TITLE, NAME (TYPE), due YYYY-MM-DD, fine £P.PP`
- `Fines`, then `on overdue loans: £P.PP` (total for open loans) and `on late returns: £P.PP` (total for returned
  loans).
- `New loans on YYYY-MM-DD`, then:
  - `OK: NAME borrowed TITLE, due YYYY-MM-DD`
  - `OK: NAME returned TITLE, on time` or `OK: NAME returned TITLE, N days late, fine £P.PP`
  - `Error: MESSAGE`

## How to check

```
python tasks/check/check.py 09 -- <the command that runs your program> tasks/data
```

## Language notes

- **Python:** `datetime.date`: `date.fromisoformat("2026-10-12")`, `borrowed + timedelta(days=14)`,
  `(today - due).days`, `day.isoformat()`. `weekday()` is 6 for Sunday. Type the optional date as `date | None`.
- **Java:** `java.time.LocalDate` (see the repo's `datetime` topic): `LocalDate.parse`, `plusDays`,
  `ChronoUnit.DAYS.between(due, today)`, `toString()` gives `YYYY-MM-DD`. Optional date: a nullable field read
  through `Optional<LocalDate> returned()`.
- **C#:** `DateOnly`: `DateOnly.ParseExact(text, "yyyy-MM-dd", CultureInfo.InvariantCulture)`, `AddDays`,
  `today.DayNumber - due.DayNumber`, `ToString("yyyy-MM-dd", CultureInfo.InvariantCulture)`. Optional date:
  `DateOnly?`.
- **C++:** C++20 `<chrono>`: parse `YYYY-MM-DD` yourself (`std::from_chars` on each part) into
  `std::chrono::year_month_day`, convert to `std::chrono::sys_days` to add `std::chrono::days{14}` or subtract
  two dates (`.count()` gives the number of days). `std::chrono::weekday{sys_days}` gives the day of the week.
  Optional date: `std::optional<std::chrono::sys_days>`.
- **JavaScript:** there is no date-only type, and `Date` mixes in time zones. Turn each date into a whole day number
  with `Date.UTC(y, m - 1, d) / 86400000`, do all the maths on day numbers, and format back with
  `new Date(days * 86400000).toISOString().slice(0, 10)`. Never use the local-time getters (`getDate()`) for this.
  Optional date: `null`.
