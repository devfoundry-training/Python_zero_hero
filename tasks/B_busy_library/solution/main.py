# ============================================================
# Task B - Busy library (solution, Core + Stretch)
# ============================================================
# Bonus session: concurrency. Many members borrow at once.
#
# The race: borrowing is "check, then act":
#     if shelf.available > 0:      # 1. check
#         shelf.available -= 1     # 2. act
# Two threads can both pass step 1 before either does step 2,
# and the library lends a copy it does not have. Even
# "available -= 1" on its own is read, subtract, write: two
# threads can read the same value and one update is lost.
#
# The fix: a lock around the whole check-and-act, so only one
# thread at a time can be inside it.
#
# Run from the repo root:
#   python tasks/B_busy_library/solution/main.py             (Core: the safe version, checked)
#   python tasks/B_busy_library/solution/main.py --stretch   (Core, then the race without the lock)
# ============================================================

import sys
import threading
import time
from collections.abc import Callable
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

    # --- the fix: check and act together, under one lock ----------

    def borrow_safe(self) -> bool:
        with self._lock:  # one thread at a time from here...
            if self.available > 0:
                self.available -= 1
                self.loans_recorded += 1
                return True
            return False  # ...to here (the lock is released on return)

    def give_back_safe(self) -> None:
        with self._lock:
            self.available += 1

    # --- the race (Stretch only): the same code with no lock --------

    def borrow_unsafe(self) -> bool:
        if self.available > 0:
            time.sleep(0)  # give other threads a chance to run, as a busy machine would
            self.available -= 1
            count = self.loans_recorded
            time.sleep(0)
            self.loans_recorded = count + 1
            return True
        return False

    def give_back_unsafe(self) -> None:
        value = self.available
        time.sleep(0)
        self.available = value + 1


def scenario_1(borrow: Callable[[Shelf], bool]) -> tuple[int, int, int]:
    """MEMBERS_1 threads each try once to borrow from COPIES_1 copies.
    A barrier holds every thread until all are ready, so they really
    do arrive at the same moment. Returns (borrowed, refused, available)."""
    shelf = Shelf(COPIES_1)
    start = threading.Barrier(MEMBERS_1)
    results: list[bool] = []
    results_lock = threading.Lock()

    def member() -> None:
        start.wait()
        ok = borrow(shelf)
        with results_lock:
            results.append(ok)

    threads = [threading.Thread(target=member) for _ in range(MEMBERS_1)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()  # wait for every thread before reading the results
    borrowed = results.count(True)
    return borrowed, len(results) - borrowed, shelf.available


def scenario_2(borrow: Callable[[Shelf], bool], give_back: Callable[[Shelf], None]) -> tuple[int, int]:
    """MEMBERS_2 threads each borrow and return CYCLES times.
    Returns (loans recorded, available at the end)."""
    shelf = Shelf(COPIES_2)

    def member() -> None:
        for _ in range(CYCLES):
            if borrow(shelf):
                give_back(shelf)

    # A thread pool: the executor starts the threads and the with
    # block waits for all of them to finish
    with ThreadPoolExecutor(max_workers=MEMBERS_2) as pool:
        for _ in range(MEMBERS_2):
            pool.submit(member)
    return shelf.loans_recorded, shelf.available


def main() -> None:
    print("Busy library")
    print(f"Scenario 1: {MEMBERS_1} members, 1 book with {COPIES_1} copies, everyone borrows at once")
    borrowed, refused, available_1 = scenario_1(Shelf.borrow_safe)
    print(f"borrowed: {borrowed}")
    print(f"refused: {refused}")
    print(f"available at end: {available_1}")

    print(f"Scenario 2: {MEMBERS_2} members, {COPIES_2} copies, {CYCLES} borrow-and-return cycles each")
    loans, available_2 = scenario_2(Shelf.borrow_safe, Shelf.give_back_safe)
    print(f"loans recorded: {loans}")
    print(f"available at end: {available_2}")

    ok = (borrowed == COPIES_1 and available_1 == 0
          and loans == MEMBERS_2 * CYCLES and available_2 == COPIES_2)
    print(f"Result: {'OK' if ok else 'WRONG'}")

    if "--stretch" in sys.argv:
        # Not checked: the numbers change from run to run, which is the point
        print("Stretch: the same scenarios with no lock")
        borrowed, refused, available_1 = scenario_1(Shelf.borrow_unsafe)
        print(f"scenario 1: borrowed {borrowed} of {COPIES_1} copies, available at end {available_1}")
        loans, available_2 = scenario_2(Shelf.borrow_unsafe, Shelf.give_back_unsafe)
        print(f"scenario 2: loans recorded {loans} of {MEMBERS_2 * CYCLES}, available at end {available_2}")


if __name__ == "__main__":
    main()
