# Task 07: Errors done properly

## Goal

Make the library say **why** something failed, and make the command loop impossible to crash, whatever the user
types.

## What this session taught

Throwing and catching exceptions, `try` / `catch` (`except`) / `finally`, custom exception classes and
hierarchies, catching the specific before the general, wrapping one exception in another, and when not to use
exceptions.

## Core

1. Create a base exception, `LibraryError`, and one subclass per problem. Each builds its own message:

   | Exception | Message |
   |---|---|
   | `UnknownBook` | `no book with id ID` |
   | `UnknownMember` | `no member with id ID` |
   | `BookNotAvailable` | `TITLE has no copies available` |
   | `MemberLimitReached` | `NAME already has N loans (limit N)` |
   | `NotOnLoan` | `TITLE is not on loan to NAME` |
   | `CommandError` | (the message passed in) |

2. `Library.borrow` and `Library.return_book` throw these instead of returning false. `borrow` checks in this
   order: member exists, book exists, member is under the limit, a copy is available. `return_book` checks:
   member exists, book exists, the member has that book on loan.
3. A command loop reads lines from standard input until `quit` or the end of the input. Commands (the first word is
   not case-sensitive, words are separated by spaces):
   - `borrow MEMBER_ID BOOK_ID`
   - `return MEMBER_ID BOOK_ID`
   - `loans MEMBER_ID` (the titles the member has on loan, in the order borrowed)
   - `quit`
4. Blank lines are skipped silently. Every other line is echoed as `> ` followed by its words joined by single
   spaces.
5. Problems with the input itself are `CommandError`s:
   - wrong number of words: `usage: borrow MEMBER_ID BOOK_ID` (or `return ...`, or `usage: loans MEMBER_ID`)
   - an id that is not a whole number: `member id must be a whole number, got 'TEXT'` (or `book id ...`).
     A whole number is an optional `-` followed by the digits 0 to 9 only. Check the member id first.
   - an unknown first word: `unknown command 'WORD'` (the word as typed)
6. The loop catches `LibraryError` and prints `Error: MESSAGE`. It also catches any other exception and prints
   `Error: unexpected problem` so the loop keeps going (the sample input never triggers this).
7. The library data is the same CSV constants as tasks 04 to 06. The checker feeds `data/input_07.txt` into your
   program.

## Stretch

1. Count the commands, the successes and the errors, and print `Session: N commands, N OK, N errors` just before
   `Goodbye`, from a `finally` block so it prints however the loop ends.
2. When an id fails to parse, keep the language's own parsing error as the **cause** of your `CommandError`
   (exception chaining), and show the cause when the program runs with a `--debug` flag.

## Challenge

1. Write a second version of `borrow` that does not throw: it returns a result object (success with the loan, or
   failure with the reason). Compare the two calling styles in a comment: which is clearer, and when?
2. Make sure a failed `borrow` changes nothing: no half-updated counts if a check fails halfway.

## Data contract

Exceptions: one base class, `LibraryError`, and the subclasses above. Name them in your language's style: Python
`UnknownBookError`, Java and C# `UnknownBookException`, C++ `UnknownBookError`, JavaScript `UnknownBookError`.

Input: `data/input_07.txt`, one command per line (it includes a blank line, upper-case `BORROW`, a bad id and a
command after `quit` that must never run).

## Output format

`expected.txt` is the exact output. The rules behind it:

- First line: `Library Manager: 20 books, 9 members`
- Each non-blank input line: `> WORDS`
- Success lines:
  - borrow: `OK: NAME borrowed TITLE, due in N days` (N from the member's policy)
  - return: `OK: NAME returned TITLE`
  - loans: `NAME has N loans: TITLE, TITLE` (`1 loan`), or `NAME has no loans`
- Failure lines: `Error: MESSAGE`
- `quit` is echoed, then the program prints `Goodbye` and stops reading. At the end of the input it also prints
  `Goodbye`.

## How to check

```
python tasks/check/check.py 07 -- <the command that runs your program>
```

## Language notes

- **Python:** `class LibraryError(Exception)` and `class UnknownBookError(LibraryError)` calling
  `super().__init__(message)`. `int("x")` raises `ValueError`, but `int()` also accepts `+4` and `4_000`, so check
  the text first (`re.fullmatch(r"-?[0-9]+", text)`). Chain with `raise CommandError(...) from error`.
- **Java:** extend `RuntimeException` (unchecked) for `LibraryException` and pass the message to `super(message)`.
  `Integer.parseInt` throws `NumberFormatException` and accepts `+4`, so check the pattern with
  `text.matches("-?[0-9]+")`. Chain with `new CommandException(message, cause)`.
- **C#:** `class LibraryException : Exception` with `: base(message)`. `int.TryParse` returns false instead of
  throwing, which is the idiomatic choice; it accepts spaces and `+`, so check the pattern too. Chain with the
  `innerException` constructor argument.
- **C++:** derive `LibraryError` from `std::runtime_error`; catch by `const LibraryError&`. `std::stoi("4abc")`
  returns 4 without complaint, so use `std::from_chars` and check that it used every character. Challenge 1 is
  the classic C++ alternative: return `std::optional`, an error code, or `std::expected` (C++23).
- **JavaScript:** `class LibraryError extends Error` and set `this.name = "LibraryError"` in the constructor.
  `Number("x")` gives `NaN` and `Number("")` gives 0, neither throws, so test with `/^-?[0-9]+$/` first. Chain with
  `new CommandError(message, { cause: error })`.
