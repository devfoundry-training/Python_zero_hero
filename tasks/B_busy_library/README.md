# Task B (bonus): Busy library

## Goal

Many members borrow at the same moment. See how shared data goes wrong when threads race, then fix it so the
numbers always add up.

## What this session taught

Threads (or tasks), starting and joining them, shared state, race conditions, locks (mutexes), atomic operations,
thread pools, and making sure every thread starts at the same moment (barriers / latches).

## The race

Borrowing is "check, then act":

```
if available > 0:        # 1. check
    available -= 1       # 2. act
```

Two threads can both pass step 1 before either reaches step 2, so the library lends a copy it does not have.
Even `available -= 1` on its own is three steps (read, subtract, write): two threads can read the same value, and
one of the two updates is lost.

**The fix:** put the whole check-and-act inside one lock, so only one thread at a time can be in it. Reading and
updating the counters for the loans recorded goes inside the same lock (or uses an atomic counter).

## Core

1. A `Shelf` holds the copies of one book: `copies`, `available` and `loans_recorded`, plus a lock.
   `borrow()` returns true and records a loan when a copy is available, false otherwise; `give_back()` returns a
   copy. Both use the lock around the whole check-and-act.
2. Scenario 1: one book with 3 copies and 8 members (threads). Every thread waits at a barrier (or latch) so they
   all try at once, then each tries to borrow **once** and keeps the book. Wait for every thread (join), then
   count the results.
3. Scenario 2: one book with 4 copies and 4 members (threads, or a thread pool of 4). Each member does 5000 cycles of
   borrow then give back. With 4 copies and 4 members a borrow can never fail, so exactly 20000 loans must be
   recorded and all 4 copies must be back at the end.
4. Print the summary lines, then `Result: OK` when scenario 1 gave exactly 3 borrowed, 5 refused and 0 available
   and scenario 2 gave 20000 loans and 4 available; otherwise `Result: WRONG`.

Only these summary numbers are printed: which member got a copy changes from run to run, so it is never printed.

## Stretch

1. Run both scenarios again without the lock (an `--unsafe` flag or a second set of methods) and print what went
   wrong: more than 3 copies lent, fewer than 20000 loans recorded, copies lost. On a fast machine the race can be
   rare; a tiny pause (a zero-length sleep or a yield) between the check and the act makes it show up nearly every
   time. These numbers are different on every run, so they are not checked.
2. Use your language's thread pool (or task API) for scenario 2 instead of creating threads by hand.

## Challenge

1. Replace the counter lock with an atomic integer and explain why that alone does **not** fix scenario 1.
2. Two books, two locks: a member who borrows both at once (locks book A, then book B) and another who does it the
   other way round can deadlock. Show it, then fix it by always taking the locks in id order.

## Data contract

| Name | Value |
|---|---|
| Scenario 1 members (threads) | 8 |
| Scenario 1 copies | 3 |
| Scenario 2 members (threads) | 4 |
| Scenario 2 copies | 4 |
| Scenario 2 cycles per member | 5000 |

No files are read.

## Output format

`expected.txt` is the exact output:

```
Busy library
Scenario 1: 8 members, 1 book with 3 copies, everyone borrows at once
borrowed: N
refused: N
available at end: N
Scenario 2: 4 members, 4 copies, 5000 borrow-and-return cycles each
loans recorded: N
available at end: N
Result: OK
```

## How to check

```
python tasks/check/check.py B -- <the command that runs your program>
```

Run the check several times: a race that is only sometimes wrong is still wrong.

## Language notes

- **Python:** `threading.Thread`, `threading.Lock` (`with lock:`), `threading.Barrier`,
  `concurrent.futures.ThreadPoolExecutor`. The global interpreter lock does **not** prevent this race: a thread can
  be paused between any two bytecode steps, and the check and the act are many steps apart. `time.sleep(0)` in the
  unsafe version makes the race visible.
- **Java:** `Thread` or `ExecutorService` (`Executors.newFixedThreadPool(4)`, then `shutdown` and
  `awaitTermination`), `synchronized` methods or a `ReentrantLock`, `CountDownLatch` or `CyclicBarrier` for the
  start, `AtomicInteger` for Challenge 1 (see the repo's `concurrency` topic). `Thread.yield()` widens the race.
- **C#:** `Task.Run` and `Task.WaitAll`, or `Parallel.For`; `lock (gate) { ... }` around the check-and-act;
  `Barrier` or `CountdownEvent` for the start; `Interlocked.Increment` for Challenge 1. `Thread.Yield()` widens the
  race.
- **C++:** `std::jthread` (joins itself) or `std::thread` plus `join`, `std::mutex` with `std::lock_guard` or
  `std::scoped_lock`, `std::latch` or `std::barrier` (C++20) for the start, `std::atomic<int>` for Challenge 1,
  `std::scoped_lock(a, b)` locks two mutexes without deadlock (see the repo's `concurrency` topic). The unsafe
  version is a data race, which is undefined behaviour in C++: build it with `-fsanitize=thread` on GCC or Clang
  to see it reported. `std::this_thread::yield()` widens the race.
- **JavaScript:** Node runs your code on one thread, so the race comes from `await` instead: make `borrow` an
  `async` function that checks, then `await`s (for example `await new Promise(r => setTimeout(r, 0))`), then acts,
  and start all the members with `Promise.all`. The fix is to queue the borrows so each one finishes before the next
  starts (a small promise-chain lock), or to do the check and the act with no `await` between them. Real threads are
  `worker_threads` with `SharedArrayBuffer` and `Atomics` (a Challenge in themselves).
