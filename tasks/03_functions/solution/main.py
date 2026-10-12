# ============================================================
# Task 03 - Functions and a menu (solution, Core + Stretch)
# ============================================================
# Session 3: functions. Builds on task 02.
#
# Run from the repo root:
#   python tasks/03_functions/solution/main.py < tasks/data/input_03.txt
#   python tasks/03_functions/solution/main.py --stretch < tasks/data/input_03.txt
# Type the choices yourself if you run it without "<".
# ============================================================

import sys

import shelf  # Stretch 1: our own module, in shelf.py next to this file

MENU = "Menu: 1 catalogue | 2 search | 3 report | 4 stats | 0 quit"


def read_line() -> str | None:
    """Read one line from the keyboard (or a piped file).

    Returns the line without surrounding spaces, or None at the end
    of the input. We echo it back as "> text" so the output reads
    like a transcript even when the input comes from a file.
    """
    line = sys.stdin.readline()
    if line == "":  # "" only happens at the end of the input
        return None
    text = line.strip()
    print(f"> {text}" if text else ">")  # never leave a trailing space
    return text


def show(lines: list[str]) -> None:
    for line in lines:
        print(line)


def run_menu(include_stretch: bool) -> None:
    print("Library Manager")
    while True:
        print(MENU)
        choice = read_line()
        if choice is None or choice == "0":
            break

        # The choice is compared as text, so "abc" is just another
        # unknown choice: no number parsing, nothing to go wrong.
        match choice:
            case "1":
                show(shelf.catalogue())
            case "2":
                print("Search for:")
                term = read_line()
                if term is None:
                    break
                show(shelf.search_report(term))
            case "3":
                show(shelf.report())
            case "4":
                show(shelf.stats(include_stretch))
            case _:
                print(f"Unknown choice: {choice}")
    print("Goodbye")


if __name__ == "__main__":
    run_menu("--stretch" in sys.argv)
