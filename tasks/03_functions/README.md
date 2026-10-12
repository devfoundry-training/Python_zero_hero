# Task 03: Functions and a menu

## Goal

Turn the scripts from tasks 01 and 02 into small, named functions and drive them from a text menu.

## What this session taught

Defining and calling functions, parameters and return values, default values, scope (local versus global), and
splitting a program into reusable pieces.

## Core

1. Turn every feature from tasks 01 and 02 into a function that takes what it needs as parameters and **returns**
   its result (a value, or the lines to print). Only the menu prints. You need at least: `era_of(year)`,
   `copies_text(count)`, `catalogue_line(index)`, `search(term)`, `report()`, `word_count()`, `longest_title()`,
   `total_copies()`, `average_year()`.
2. Write a menu loop. Each time round it prints the menu line, reads one line of input and does what it says:
   - `1` prints the catalogue (task 01 format)
   - `2` prints `Search for:`, reads a second line (the search term) and prints the search result (task 02 format)
   - `3` prints the report table (task 02 format)
   - `4` prints the stats (see Output format)
   - `0` ends the loop
   - anything else prints `Unknown choice: TEXT`
3. Compare the choice as **text** (`"1"`, not the number 1): then `abc` is just another unknown choice.
4. After reading any line, echo it as `> TEXT` (the line with spaces trimmed from both ends; a blank line echoes
   as `>`). The input usually comes from a file, so the echo makes the output read like a conversation.
5. When the input ends without a `0`, behave as if `0` was typed. Always finish with `Goodbye`.

The checker feeds `data/input_03.txt` into your program.

## Stretch

1. Move the functions into their own file or module and import them into the menu program.
2. Add `oldest_and_newest()`, one function that returns two results at once, and print them at the end of the stats
   as `oldest: TITLE (YEAR)` and `newest: TITLE (YEAR)`. (This changes the stats output, so the checker will report
   a difference: run the check before you add it.)

## Challenge

1. Give `search` an optional second parameter, `whole_word`, defaulting to false. When true, `the` matches
   `The Hobbit` but not `Theatre`.
2. Write `menu_choice(prompt, allowed)` that keeps asking until it gets one of the allowed answers, and use it.

## Data contract

The same ten books as task 01, in the same fixed arrays.

Input: lines of text from standard input. `data/input_03.txt`:

```
1
2
the
2
DUNE
abc
9
3
4
0
```

## Output format

`expected.txt` is the exact output. The rules behind it:

- First line: `Library Manager`.
- Before every read of a choice: `Menu: 1 catalogue | 2 search | 3 report | 4 stats | 0 quit`.
- Every line read is echoed as `> TEXT`.
- Choice `1`: `Catalogue (10 books)` and the ten catalogue lines from task 01.
- Choice `2`: `Search for:`, the echoed term, then the search result lines from task 02.
- Choice `3`: the report from task 02, starting with `Report`.
- Choice `4`: `Stats`, then `books: N`, `copies: N`, `out of stock: N`, `pre-1950: N`, `average year: N`,
  `words in titles: N`, `longest title: TITLE (N characters)`.
- Last line: `Goodbye`.

## How to check

```
python tasks/check/check.py 03 -- <the command that runs your program>
```

## Language notes

- **Python:** `sys.stdin.readline()` returns `""` only at the end of the input, so no exceptions are needed. Type
  hint every function (`def era_of(year: int) -> str:`). Stretch 1 is a module: `shelf.py` next to `main.py`,
  then `import shelf`. Stretch 2 returns a tuple: `return oldest, newest`.
- **Java:** read with `BufferedReader.readLine()` (returns `null` at the end) or `Scanner.hasNextLine()`. Methods
  are `static` for now. Stretch 1: a second class `Shelf` with `static` methods. Stretch 2: return a small `record`.
- **C#:** `Console.ReadLine()` returns `null` at the end of the input (`string?`). Stretch 1: a `static class Shelf`
  in its own file. Stretch 2: return a tuple, `(int Oldest, int Newest)`.
- **C++:** `while (std::getline(std::cin, line))` stops at the end of the input. Pass arrays by `const&`.
  Stretch 1: `shelf.h` with declarations and `shelf.cpp` with definitions (see the repo's `compilation` topic).
  Stretch 2: return a `std::pair<int, int>` or a small `struct`, unpacked with structured bindings.
- **JavaScript:** read all input at once with `fs.readFileSync(0, "utf8").split(/\r?\n/)` and walk through the
  lines (the text ends with a newline, so drop the empty string after it), or use `readline` with
  `for await (const line of rl)`. Stretch 1: an ES module with `export function`
  and `import { ... } from "./shelf.js"`. Stretch 2: return an array and destructure it,
  `const [oldest, newest] = oldestAndNewest();`.
