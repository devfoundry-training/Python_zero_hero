# ============================================================
# Task B - Busy library (starter)
# ============================================================
# Bonus session: concurrency. Many members borrow at once.
# Borrowing is "check, then act": two threads can both pass the
# check before either acts. Put the whole check-and-act inside
# one lock (see README.md).
#
# Run from the repo root:
#   python tasks/B_busy_library/starter/main.py
# Check it:
#   python tasks/check/check.py B -- python tasks/B_busy_library/starter/main.py
# ============================================================

import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Final

MEMBERS_1: Final[int] = 8
COPIES_1: Final[int] = 3
MEMBERS_2: Final[int] = 4
COPIES_2: Final[int] = 4
CYCLES: Final[int] = 5000


class Shelf:
    """The copies of one book, shared by every thread."""

    def __init__(self, copies: int) -> None:
        self.copies = copies
        self.available = copies
        self.loans_recorded = 0
        self._lock = threading.Lock()

    def borrow(self) -> bool:
        """True and one loan recorded when a copy is available, else False."""
        raise NotImplementedError("not implemented: Shelf.borrow")

    def give_back(self) -> None:
        raise NotImplementedError("not implemented: Shelf.give_back")


def scenario_1() -> tuple[int, int, int]:
    """MEMBERS_1 threads wait at a threading.Barrier, then each tries
    once to borrow. Join them all. Returns (borrowed, refused, available)."""
    raise NotImplementedError("not implemented: scenario_1")


def scenario_2() -> tuple[int, int]:
    """MEMBERS_2 threads each borrow and give back CYCLES times.
    Returns (loans recorded, available at the end)."""
    raise NotImplementedError("not implemented: scenario_2")


def main() -> None:
    print("Busy library")
    print(f"Scenario 1: {MEMBERS_1} members, 1 book with {COPIES_1} copies, everyone borrows at once")
    borrowed, refused, available_1 = scenario_1()
    print(f"borrowed: {borrowed}")
    print(f"refused: {refused}")
    print(f"available at end: {available_1}")

    print(f"Scenario 2: {MEMBERS_2} members, {COPIES_2} copies, {CYCLES} borrow-and-return cycles each")
    loans, available_2 = scenario_2()
    print(f"loans recorded: {loans}")
    print(f"available at end: {available_2}")

    # TODO Core 4: "Result: OK" when both scenarios add up, else "Result: WRONG"
    print("Result: not implemented")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as error:
        print(error)  # the first piece still to write
