# Task 10: SQLite storage

## Goal

Move the library into a real database. The CSV files are imported once; after that the database is where the data
lives, and every question is answered with SQL.

## What this session taught

Connecting to a database, creating tables from a schema, `INSERT`, `SELECT`, `UPDATE`, `WHERE`, `JOIN`,
`GROUP BY`, parameterised queries (and why string-built SQL is dangerous), and transactions.

## Core

1. The program takes the data folder as its first argument (default `tasks/data`) and today's date as an optional
   second argument (default `2026-10-12`).
2. Delete `out/library.db` if it exists, create it, switch on foreign keys and run `data/schema.sql` (the same schema
   the SQL repo uses). Print `Created out/library.db from schema.sql`.
3. Import the three CSV files with parameterised `INSERT`s, inside one transaction. Print the row counts, taken from
   the database with `SELECT COUNT(*)`.
4. Answer these in SQL (one query each), in this order:
   1. books per genre, A-Z by genre (`GROUP BY`)
   2. books with nothing on the shelf: copies minus open loans is 0 (`LEFT JOIN` + `GROUP BY` + `HAVING`), by id
   3. a title search for `the`, then for `x' OR '1'='1`, using `LOWER(title) LIKE ?` with the `%` wildcards inside
      the parameter value, by id. The second search must find nothing: that is the parameter keeping the quote
      characters as data
   4. open loans per member, including members with none (`LEFT JOIN`), by member id
5. Load the task 09 model from the database (not from the CSV files) and run the same three actions as task 09
   (105 borrows 15, 105 borrows 16, 102 returns 14). Save each success with one parameterised `INSERT` or `UPDATE`.
6. Load the model from the database again and print the counts and the task 09 overdue report, to prove the changes
   were saved.

**Parameterised queries only.** Never build SQL by joining strings with values.

## Stretch

1. Do a whole borrow inside one transaction: insert the loan, then check in SQL that open loans do not exceed
   copies, and roll back if they do. Show that a refused borrow leaves the number of loans unchanged.
2. Add an index on `loans(member_id)` and explain in a comment which query it helps.

## Challenge

1. Show the danger: build the search SQL by joining strings (in a throwaway function) and find a search text that
   returns every book. Then explain why the parameter version is safe.
2. Add a `reservations` table to a copy of the schema (book, member, position, created date) with the right keys
   and constraints, ready for task 11.

## Data contract

`data/schema.sql` (shared with the SQL repo; runs on SQLite 3 and MySQL 8):

| Table | Columns |
|---|---|
| `books` | `id` INTEGER primary key, `title` VARCHAR(100), `author` VARCHAR(100), `year` INTEGER (1450 to 2100), `genre` VARCHAR(50), `copies` INTEGER (0 or more), `format` VARCHAR(10) (`print`, `ebook`, `audio`), `length` INTEGER (more than 0) |
| `members` | `id` INTEGER primary key, `name` VARCHAR(100), `email` VARCHAR(100) unique, `type` VARCHAR(10) (`standard`, `student`, `staff`), `joined` DATE |
| `loans` | `id` INTEGER primary key, `book_id` INTEGER (references books), `member_id` INTEGER (references members), `borrowed` DATE, `returned` DATE or NULL |

Ids always come from the data; a new loan gets the highest loan id plus 1. Dates are stored as text `YYYY-MM-DD`
in SQLite. Money is never stored. The schema has no semicolons inside comments, so it can be split on `;` and run
one statement at a time.

## Output format

`expected.txt` is the exact output. The rules behind it:

- `Created out/library.db from schema.sql`
- `Imported N books, N members, N loans`
- `Books per genre`, then `GENRE: N`
- `Nothing on the shelf`, then `#ID TITLE: N of N available`
- `Search "TEXT": N books` (`1 book`, `0 books`), then `  #ID TITLE (YEAR)` per match
- `Open loans per member`, then `#ID NAME: N`
- `New loans on YYYY-MM-DD`, then:
  - `OK: NAME borrowed TITLE, due YYYY-MM-DD, saved as loan ID`
  - `Error: MESSAGE`
  - `OK: NAME returned TITLE, fine £P.PP, saved`
- `Reloaded: N books, N members, N loans (N open)`
- The overdue report exactly as in task 09.

## How to check

```
python tasks/check/check.py 10 -- <the command that runs your program> tasks/data
```

## Language notes

- **Python:** `sqlite3` is in the standard library. `conn.executescript(schema)` runs the whole file;
  `conn.execute("PRAGMA foreign_keys = ON")`; `?` placeholders with a tuple of values; `executemany` for the
  import; `with conn:` commits, or rolls back on an exception.
- **Java:** JDBC with the `org.xerial:sqlite-jdbc` driver added in `pom.xml` (the repo's `databases` topic uses
  JDBC already). `PreparedStatement` with `?` and `setInt` / `setString`; `addBatch` / `executeBatch` for the
  import; `conn.setAutoCommit(false)` then `commit()` / `rollback()`. JDBC runs one statement at a time: split the
  schema on `;`.
- **C#:** `Microsoft.Data.Sqlite` (NuGet). `SqliteCommand` with `$name` or `@name` parameters
  (`command.Parameters.AddWithValue`), `ExecuteNonQuery` runs the whole schema, `BeginTransaction()` /
  `Commit()`.
- **C++:** no extra libraries: use the SQLite that ships with the operating system. Windows 10 and 11:
  `winsqlite3.dll` is part of Windows; the header `<winsqlite/winsqlite3.h>` and `winsqlite3.lib` come with the
  Windows SDK. macOS: the system `libsqlite3` (`<sqlite3.h>`, link `-lsqlite3`). Linux: the distro's
  `libsqlite3-dev` package. All three give the same C API: `sqlite3_open`, `sqlite3_exec` (runs the whole schema),
  `sqlite3_prepare_v2`, `sqlite3_bind_int` / `sqlite3_bind_text`, `sqlite3_step`, `sqlite3_column_*`,
  `sqlite3_finalize`, `sqlite3_close`. Wrap the connection and each statement in a small RAII class so they are
  always finalised and closed (see the repo's `c_interop` topic).
- **JavaScript:** `node:sqlite` is built in (`DatabaseSync`, Node 22.13 or later; older 22.x needs
  `--experimental-sqlite`, and some versions print an experimental warning on stderr, which the checker ignores).
  `db.exec(schema)` runs the whole file; `db.prepare(sql).run(...)` / `.all(...)` with `?` placeholders.
