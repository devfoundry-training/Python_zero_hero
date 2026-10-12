# Tasks: the Library Manager

One set of tasks for every Zero to Hero repo (Python, Java, C#, C++, JavaScript; the SQL repo uses the same schema
and data in its own order). Every language gets the same briefs, the same sample data and the same expected output.
Only the code differs.

There are 12 tasks and a bonus, one for the end of each session. Each task combines everything taught in that
session and builds on the task before, so by the end the learner has one working program, the **Library Manager**:
from a fixed array of ten books to a tested REST API over a SQLite database.

## Core, Stretch and Challenge

Every task has three levels:

- **Core** is for everyone. `expected.txt` is the exact Core output for the sample data, and it is what the checker
  compares.
- **Stretch** is for those who finish early. A solution prints its Stretch output only when asked (see the running
  section below), so its default run always matches `expected.txt`.
- **Challenge** is for the strongest learners or for homework. The solutions cover Core and Stretch only.

## Session to task map

The topic folders each task follows in each repo. "(no topic yet)" marks a session the repo does not teach today:
the task still works, but the repo needs a short topic file before the task is used on a course.

| # | Task | Session | Python | Java | C# | C++ | JavaScript |
|---|---|---|---|---|---|---|---|
| 01 | Bookshelf | types, operators, conditionals, switch, arrays | basics | basics, control_flow | datatypes, operators, control_flow | basics, control_flow | basics, control_flow |
| 02 | Search and report | loops, strings | iteration | iteration, basics (strings) | iteration, string_manipulation | iteration | iteration |
| 03 | Functions and a menu | functions, modules | functions, module_packages | functions | (no topic yet) | functions, compilation | functions |
| 04 | Dynamic catalogue | collections | collections | collections | collections, linq | collections | collections |
| 05 | Classes | classes, encapsulation | oop | oop | oop | oop | oop |
| 06 | Book types and loan policies | inheritance, interfaces, polymorphism | oop | oop | oop | oop, memory | oop |
| 07 | Errors done properly | exceptions | exceptions | exceptions | exceptions | exceptions | exceptions |
| 08 | Persistence | file I/O, CSV, JSON | io | io | io | io | (no topic yet) |
| 09 | Loans with due dates | dates | (no topic yet) | datetime | (no topic yet) | datetime | (no topic yet) |
| 10 | SQLite storage | databases | databases | databases | (no topic yet) | c_interop (C API) | (no topic yet) |
| 11 | Test the rules | testing, TDD | testing | testing | CS_zero_heroTests | testing | (no topic yet) |
| 12 | Expose the library | HTTP APIs | apis | apis | (no topic yet) | (no topic yet) | async |
| B | Busy library (bonus) | concurrency | (no topic yet) | concurrency | (no topic yet) | concurrency | async |

**SQL repo:** the same `schema.sql`, `seed.sql` and CSV data, with eight tasks (S1 to S8) in SQL's own order:
SELECT, filtering, joins, aggregation, subqueries and views, window functions, design (a `reservations` table, as in
task 10 Challenge 2) and transactions (a borrow that rolls back, as in task 10 Stretch 1).

## Choosing tasks: 3 days or 5 days

**5-day course:** all 12, one or two per half day in order, with B for groups that finish early or as homework.

| Day | Tasks |
|---|---|
| 1 | 01, 02, 03 |
| 2 | 04, 05, 06 |
| 3 | 07, 08, 09 |
| 4 | 10, 11 |
| 5 | 12, B (bonus) |

**3-day course:** these 8, which follow the usual fundamentals order and make one program end to end:

| Day | Tasks | Why |
|---|---|---|
| 1 | 01, 02, 03 | the language basics, ending with a working menu |
| 2 | 04, 05, 06 | collections and the object model the rest depends on |
| 3 | 07, 08 | errors and files: a program that survives bad input and keeps its data |

Swaps for a 3-day group with different needs (the starters carry the previous solution, so skipping is safe):

- **Testing focus:** replace 08 with 11 (start from the task 11 starter; the date tests use the model it provides).
- **Strong group:** fold 02 into 01 (Core only) and add 09 on day 3.
- **Web focus:** replace 06 with 12 on day 3 (start from the task 12 starter).

## What is in this folder

```
tasks/
  README.md              this file
  data/                  sample data, identical in every repo: books, members, loans, schema.sql, seed.sql
  check/check.py         the checker (Python 3.10 or later, standard library only)
  check/api_script.json  the requests the checker sends in task 12
  01_bookshelf/
    README.md            the brief: Core, Stretch, Challenge, data contract, output format, language notes
    expected.txt         the exact Core output for the sample data
    starter/             builds and runs as it is; unfinished parts say "not implemented"
    solution/            Core and Stretch, passes the check
  ...
  12_library_api/        also expected_stretch.txt (the Open Library summary)
  B_busy_library/        bonus: concurrency
```

Each `starter/` contains the previous task's solution (or the parts of it the task builds on) plus stubs for the
new work, so a group can start any task without having finished the one before. Task B stands alone, so it can
follow any task from 07 on.

## The checker

`check/check.py TASK [--expected FILE] [--timeout SECS] -- COMMAND ...` runs the command and prints `PASS`, or
`FAIL` with the first line that differs. Exit code 0 is a pass. It needs Python 3.10 or later and nothing else.

- Line endings, trailing spaces and trailing blank lines do not count; everything else does.
- Tasks 03 and 07 read commands from standard input: the checker feeds in `data/input_03.txt` and
  `data/input_07.txt` itself.
- Task 11 runs the tests and passes when the run succeeds and every test name in `expected.txt` appears in the
  output.
- Task 12 starts the server on a free port (`{port}` in the command is replaced with it), sends the requests in
  `check/api_script.json`, compares the answers with `expected.txt`, then stops the server.

## Conventions every solution follows

| Rule | Detail |
|---|---|
| Output | Exactly `expected.txt`: no extra lines, no prompts, no colours. Debug output goes to stderr. |
| Data folder | Tasks 08 to 12 take it as the first argument, default `tasks/data`. Tasks 01 to 07 carry their data in the code. |
| Today | Tasks 09 and 10 take today's date as the second argument, default `2026-10-12`; task 12 uses `2026-10-12`. Nothing reads the real clock. |
| Port | Task 12 takes the port as the second argument, default `8080`. |
| Written files | Tasks 08 and 10 write into `out/` in the current directory (git-ignored). |
| Money | Integer pence everywhere, shown as `£1.25`. |
| Sorting text | A-Z means lower-case, character by character (ordinal). Never a locale-aware compare. |

## Running and checking: Python

Python 3.10 or later, standard library only: the tasks need no `pip install`. Run every command from the
repository root. On Windows, `py -3.13` (or `py`) works wherever `python` is shown.

Tasks 01 to 06 and B are one file, `main.py`. From task 07 the model moves into `library.py`, which `main.py`
imports; task 08 adds `storage.py`, task 10 `db.py`, task 11 `test_library.py`, and task 12 `api.py` and
`openlibrary.py`. Each folder is a program on its own: run it from the repository root and Python finds the files
next to `main.py`.

### Running

```
python tasks/01_bookshelf/solution/main.py
python tasks/01_bookshelf/solution/main.py --stretch
python tasks/03_functions/solution/main.py < tasks/data/input_03.txt
python tasks/09_due_dates/solution/main.py tasks/data 2026-10-12
python tasks/11_testing/solution/test_library.py
python tasks/12_library_api/solution/main.py tasks/data 8080
```

A solution prints the Core output by default, which is what the checker compares. `--stretch` adds the Stretch
output after it. Task 12 runs a server until you press Ctrl+C; try `curl http://localhost:8080/books?title=the`.
Swap `solution` for `starter` to run the starter.

### Checking

| Task | Check command |
|---|---|
| 01 to 07, B | `python tasks/check/check.py 01 -- python tasks/01_bookshelf/solution/main.py` |
| 03, 07 | the same: the checker feeds `data/input_03.txt` / `data/input_07.txt` to stdin itself |
| 08, 09, 10 | `python tasks/check/check.py 09 -- python tasks/09_due_dates/solution/main.py tasks/data` |
| 11 | `python tasks/check/check.py 11 -- python tasks/11_testing/solution/test_library.py` |
| 12 | `python tasks/check/check.py 12 -- python tasks/12_library_api/solution/main.py tasks/data {port}` |
| 12 Stretch | `python tasks/check/check.py 12_stretch -- python tasks/12_library_api/solution/main.py --summarise tasks/data/openlibrary_dune.json` |

Every solution, in PowerShell:

```
foreach ($t in Get-ChildItem tasks -Directory | Where-Object Name -match '^(\d\d|B)_') {
    $id = $t.Name.Split('_')[0]
    $run = "tasks/$($t.Name)/solution/main.py"
    switch ($id) {
        { $_ -in '08', '09', '10' } { py -3.13 tasks/check/check.py $id -- py -3.13 $run tasks/data }
        '11' { py -3.13 tasks/check/check.py 11 -- py -3.13 tasks/11_testing/solution/test_library.py }
        '12' { py -3.13 tasks/check/check.py 12 -- py -3.13 $run tasks/data '{port}'
               py -3.13 tasks/check/check.py 12_stretch -- py -3.13 $run --summarise tasks/data/openlibrary_dune.json }
        default { py -3.13 tasks/check/check.py $id -- py -3.13 $run }
    }
}
```

### Testing the whole repository

`pytest.ini` at the repository root points pytest at the task 11 tests, the one test suite under `tasks/`:

```
python -m pytest
```

Without pytest, the standard library runs the same tests:

```
python -m unittest discover -s tasks/11_testing/solution -v
```
