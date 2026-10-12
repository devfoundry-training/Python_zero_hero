-- ============================================================
-- Library Manager schema (shared by every Zero to Hero repo)
-- ============================================================
-- Used by task 10 in every language and by the SQL repo.
-- Portable on purpose: it runs unchanged on SQLite 3 and on
-- MySQL 8.0.16 or later (select a database first in MySQL).
--
-- Rules the code relies on:
--   * ids are given by the data, never generated, so the same
--     rows get the same ids in every database. A new loan uses
--     the highest loan id plus 1.
--   * dates are DATE in MySQL and text 'YYYY-MM-DD' in SQLite.
--     Both sort and compare correctly as written.
--   * returned is NULL while the book is still on loan.
--   * money is never stored: fines are worked out in code, in
--     whole pence.
--   * SQLite only enforces the FOREIGN KEY lines after
--     PRAGMA foreign_keys = ON (run it once per connection).
--   * no semicolons inside comments or strings, so a program
--     may split this file on semicolons to run one statement
--     at a time (JDBC needs that)
-- ============================================================

DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS books;

CREATE TABLE books (
    id      INTEGER      NOT NULL PRIMARY KEY,
    title   VARCHAR(100) NOT NULL,
    author  VARCHAR(100) NOT NULL,
    year    INTEGER      NOT NULL CHECK (year BETWEEN 1450 AND 2100),
    genre   VARCHAR(50)  NOT NULL,
    copies  INTEGER      NOT NULL CHECK (copies >= 0),
    format  VARCHAR(10)  NOT NULL CHECK (format IN ('print', 'ebook', 'audio')),
    length  INTEGER      NOT NULL CHECK (length > 0)
);

CREATE TABLE members (
    id      INTEGER      NOT NULL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    email   VARCHAR(100) NOT NULL UNIQUE,
    type    VARCHAR(10)  NOT NULL CHECK (type IN ('standard', 'student', 'staff')),
    joined  DATE         NOT NULL
);

CREATE TABLE loans (
    id         INTEGER NOT NULL PRIMARY KEY,
    book_id    INTEGER NOT NULL,
    member_id  INTEGER NOT NULL,
    borrowed   DATE    NOT NULL,
    returned   DATE    NULL,
    FOREIGN KEY (book_id) REFERENCES books (id),
    FOREIGN KEY (member_id) REFERENCES members (id),
    CHECK (returned IS NULL OR returned >= borrowed)
);
