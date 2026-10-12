# Task 11: Test the rules

## Goal

Prove the library's rules work with automated tests, then add a new feature, reservations, test first.

## What this session taught

Unit tests, arrange / act / assert, test fixtures (a fresh setup for every test), asserting that an exception is
thrown, testing dates without the real clock, and test-driven development (red, green, refactor).

## Core

1. Use your language's standard test framework (see Language notes). Every test builds its own fresh library from
   the fixture below, so tests never depend on each other or on the order they run in.
2. Write the 19 tests in the first three groups below, with these names (in your language's naming style: the
   checker ignores case, underscores and a leading `test`). Run them and make them pass against your library
   classes from tasks 09 and 10.
3. Then add **reservations** test first: write one reservation test, watch it fail, write just enough code to make
   it pass, tidy up, repeat, until all six reservation tests pass.

**Borrowing**

| Test | What it checks |
|---|---|
| `test_borrow_reduces_available` | after 101 borrows book 4, book 4 has 3 available |
| `test_return_restores_available` | after 101 borrows and returns book 4, book 4 has 4 available |
| `test_borrow_unknown_book_raises` | 101 borrowing book 99 throws `UnknownBook` |
| `test_borrow_unknown_member_raises` | member 999 borrowing book 1 throws `UnknownMember` |
| `test_borrow_with_no_copies_raises` | 101 borrowing book 3 throws `BookNotAvailable` |
| `test_return_book_not_on_loan_raises` | 101 returning book 4 without borrowing it throws `NotOnLoan` |
| `test_standard_limit_is_three_loans` | 101 borrows 1, 2 and 4; borrowing 7 throws `MemberLimitReached` |
| `test_student_limit_is_five_loans` | 102 borrows 1, 2, 4, 6 and 7; borrowing 8 throws `MemberLimitReached` |

**Dates and fines** (each builds a loan directly with the dates shown)

| Test | What it checks |
|---|---|
| `test_due_date_standard_is_14_days` | 101 borrowing on 2026-10-12 is due 2026-10-26 |
| `test_due_date_student_is_21_days` | 102 borrowing on 2026-10-12 is due 2026-11-02 |
| `test_due_date_staff_is_28_days` | 103 borrowing on 2026-10-12 is due 2026-11-09 |
| `test_due_date_crosses_month_and_year_end` | 102 borrowing on 2026-12-20 is due 2027-01-10 |
| `test_due_date_in_leap_year` | 101 borrowing on 2028-02-20 is due 2028-03-05 |
| `test_not_overdue_on_due_date` | 101 borrowed 2026-09-28; on 2026-10-12 days late is 0 and the fine is 0 |
| `test_fine_one_day_late_standard` | 101 borrowed 2026-09-27; on 2026-10-12 the fine is 25 |
| `test_fine_ten_days_late_student` | 102 borrowed 2026-09-11; on 2026-10-12 the fine is 100 |
| `test_staff_never_fined` | 103 borrowed 2026-01-01; on 2026-10-12 the fine is 0 |
| `test_late_return_fine_uses_return_date` | 101 borrowed 2026-09-17, returned 2026-10-05; on 2026-12-25 the fine is 100 |
| `test_format_money` | 0, 5, 125 and 1000 pence format as `£0.00`, `£0.05`, `£1.25`, `£10.00` |

**Reservations** (written test first; in each, 101 has first borrowed book 5, the only copy of Robinson Crusoe)

| Test | What it checks |
|---|---|
| `test_reserve_book_with_no_free_copies_joins_queue` | 102 reserves book 5 and gets place 1; 103 then gets place 2 |
| `test_reserve_book_with_free_copies_raises` | 102 reserving book 1 (copies free) throws `ReservationNotNeeded` |
| `test_reserve_same_book_twice_raises` | 102 reserving book 5 a second time throws `AlreadyReserved` |
| `test_returned_copy_is_held_for_first_in_queue` | 102 reserves 5, 101 returns 5; 103 borrowing 5 throws `BookNotAvailable` |
| `test_first_in_queue_can_borrow_held_copy` | 102 reserves 5, 101 returns 5, 102 borrows 5: 0 available, nothing held |
| `test_queue_is_first_come_first_served` | 103 then 102 reserve 5, 101 returns 5: the copy is held for 103 and 102 is still queued |

The reservation rules:

- `reserve(member_id, book_id)` returns the member's place in the queue (1 is next).
- A member may reserve only when no copy is free (free = available minus copies held for someone):
  otherwise `ReservationNotNeeded` with `TITLE has copies available, borrow it instead`.
- A member cannot be in the same queue twice: `AlreadyReserved` with `NAME has already reserved TITLE`.
- When a copy comes back and the queue is not empty, the copy is **held** for the first member in the queue, who
  leaves the queue. Only that member can borrow the held copy; for everyone else it does not count as available.

## Stretch

1. Test the CSV loader: loading `data/books_corrupt.csv` keeps books 1, 2, 4, 6 and 10 and skips 5 lines.
2. Turn the fines into one table-driven test (member, days late, expected pence) using your framework's
   parameterised tests or sub-tests: (101, 0, 0), (101, 1, 25), (101, 20, 500), (102, 1, 10), (102, 30, 300),
   (103, 365, 0).

## Challenge

1. Measure the test coverage of your library code and add tests until every rule is covered.
2. A test that never fails is worth nothing: break one rule on purpose (for example make the fine 24p) and check
   that exactly the right tests fail. Undo it.

## Data contract

The fixture (built in code, not read from files): books 1 to 8 from `data/books.csv` and three members, no loans.

| id | name | type |
|---|---|---|
| 101 | Amira Khan | standard |
| 102 | Ben Taylor | student |
| 103 | Chloe Evans | staff |

"Today" is the fixed date 2026-10-12 unless a test says otherwise. Fines are integer pence.

New exceptions (subclasses of `LibraryError`): `ReservationNotNeeded`, `AlreadyReserved`.

## Output format

There is no program output to compare. `expected.txt` lists the 25 Core test names, each followed by `PASS`. The
checker runs your test command and passes when the run succeeds (exit code 0) and every name in `expected.txt`
appears somewhere in the test output. Extra tests are welcome.

## How to check

```
python tasks/check/check.py 11 -- <the command that runs your tests>
```

Your test runner must print the name of every test it runs (most do with a "verbose" or "detailed" option).

## Language notes

- **Python:** `unittest` (see the repo's `testing` topic). `setUp` builds the fixture; `assertRaises` as a context
  manager; `subTest` for the Stretch table. Run with `python -m unittest -v test_library` or
  `unittest.main(verbosity=2)`; the verbose output lists every test name.
- **Java:** JUnit 5 (`@Test`, `@BeforeEach`, `assertThrows`, `@ParameterizedTest` with `@CsvSource`). Method
  names in camelCase, for example `borrowReducesAvailable`. Maven only lists failures by default: run the tests with
  the JUnit console launcher or a Surefire setting that prints every test (the repo's tasks README has the
  command).
- **C#:** MSTest (`[TestClass]`, `[TestMethod]`, `[TestInitialize]`, `Assert.ThrowsExactly<T>`,
  `[DataRow]` for the Stretch). Run with `dotnet test --logger "console;verbosity=detailed"` so every test name
  is printed.
- **C++:** the repo's own `mini_test.h` harness (no download). Each test is a function registered by name; build
  a fresh fixture inside each one. Run the test executable directly so it prints each name and returns a non-zero
  exit code on failure.
- **JavaScript:** `node:test` and `node:assert/strict` are built in (`test("borrow reduces available", ...)`,
  `assert.throws(() => ..., UnknownBookError)`, `beforeEach`). Run with `node --test`; the default reporter
  prints every test name.
