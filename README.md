# Python Zero to Hero

[![Tasks](https://github.com/devfoundry-training/Python_zero_hero/actions/workflows/tasks.yml/badge.svg)](https://github.com/devfoundry-training/Python_zero_hero/actions/workflows/tasks.yml)

A structured teaching repository covering Python from first principles through to object-oriented programming, data handling, and testing. Each topic is a self-contained module with runnable examples and in-code commentary.

---

## Who Is This For?

- Beginners learning Python for the first time
- Delegates on instructor-led Python fundamentals courses
- Self-learners who want a clear, progressive syllabus to follow

No prior Python experience is assumed. Basic comfort with a command line is helpful.

---

## Prerequisites

| Tool   | Minimum Version |
|--------|----------------|
| Python | 3.10+          |

```bash
python --version
```

---

## Getting Started

### Option 1: Virtual Environment (Recommended)

```bash
# Clone the repository
git clone git@github.com:Edrzapi/Python_zero_hero.git
cd Python_zero_hero

# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Install Directly

If you prefer not to use a virtual environment:

```bash
git clone git@github.com:Edrzapi/Python_zero_hero.git
cd Python_zero_hero
pip install -r requirements.txt
```

> **Note:** Most modules use only the standard library. The `requirements.txt` covers the data I/O and API modules that need `requests`, `SQLAlchemy`, `pandas`, and `mysql-connector-python`.

The tasks in `tasks/` use only the standard library.

---

## Repository Structure

```
basics/               # Primitives, strings, type conversion
collections/          # Lists, tuples, sets, dicts, comprehensions
iteration/            # for, while, enumerate, itertools
functions/            # Parameters, scope, lambdas, decorators
module_packages/      # What makes a folder a package (__init__.py)
oop/                  # Classes, inheritance, MRO, abstraction
exceptions/           # try/except, custom exceptions
io/                   # File I/O, JSON, CSV
databases/            # SQLite, SQLAlchemy
apis/                 # HTTP requests with the requests library
testing/              # Doctests, unittest, test suites
tasks/                # The Library Manager tasks (see Tasks below)
  README.md           # Session to task map, 3-day and 5-day plans, how to check
  data/               # Shared sample data
  check/              # Shared checker
  01_bookshelf/ ... 12_library_api/, B_busy_library/
practice/             # Short exercises (they used to live in tasks/)
  calculator/         # OOP calculator with unit tests
  garage/             # Inheritance project with test suite
  comprehension_task/ # Comprehension practice
  palindrome/         # String manipulation exercise
main.py               # Entry point
pytest.ini            # Points pytest at the task tests
requirements.txt      # Third-party packages for the topic files
```

---

## Topics Covered

### Core Language

- **Data Types**: integers, floats, strings, booleans. Lists, tuples, sets, dictionaries. Mutability, iteration, common operations.
- **Control Flow**: `if`/`elif`/`else`, `for` and `while` loops, `break`/`continue`, list/set/dict comprehensions.
- **Functions**: defining functions, positional and keyword arguments, `*args`/`**kwargs`, scope, lambda functions, decorators.

### Object-Oriented Programming

- **Classes and Objects**: `__init__`, attributes, methods, encapsulation.
- **Inheritance**: single and multiple inheritance, method resolution order (MRO).
- **Abstraction**: abstract base classes, interface patterns.

### Error Handling

- **Exception Handling**: `try`/`except`/`finally`, raising exceptions, custom exception classes.

### Data and I/O

- **File Handling**: reading and writing text files, context managers (`with` statement).
- **Structured Data**: JSON and CSV processing.
- **Databases**: SQLite with raw SQL, introduction to SQLAlchemy.
- **APIs**: HTTP GET requests using the `requests` library.

### Testing

- **Doctests**: inline test examples in docstrings.
- **unittest**: test classes, assertions, setup/teardown.
- **Test Suites**: grouping and running multiple test modules.

---

## Tasks

The [`tasks/`](tasks/README.md) folder holds the **Library Manager**, one practical project shared by every Zero to
Hero repo: 12 tasks and a bonus in Python, Java, C#, C++ and JavaScript, and eight tasks (S1 to S8) in SQL's own
order on the same database. Every repo uses the same briefs, the same sample data and the same expected output; only
the code differs.

- **One task per session.** Each task is the end-of-session check and builds on the one before, so by the end the
  learner has one working program.
- **Three levels:** Core (everyone), Stretch (for those who finish early) and Challenge (the strongest learners, or
  homework).
- **Every task folder** has the brief (`README.md`), the exact expected output (`expected.txt`), a `starter/` that
  runs as it is (unfinished parts say "not implemented") and a `solution/` with Core and Stretch.
- **One checker:** `tasks/check/check.py` (Python 3.10 or later, standard library only) runs a program and prints
  `PASS`, or `FAIL` with the first line that differs from `expected.txt`. On Windows, `py` works in place of
  `python`.

[tasks/README.md](tasks/README.md) has the session to task map, the 3-day and 5-day selections, and the run and
check command for every task. To check the first task's solution, from the repo root:

```bash
python tasks/check/check.py 01 -- python tasks/01_bookshelf/solution/main.py
```

---

## How to Run

Each topic file can be run directly:

```bash
python basics/basic_datatypes.py
python functions/intro_func.py
python oop/Inheritance.py
```

Run unit tests:
```bash
python -m unittest -v testing/intro_to_unittest.py
```

The practice exercises import each other as packages, so run them from inside `practice/`:
```bash
cd practice
python -m garage.runner
python -m unittest -v calculator.TestCalculator
python -m unittest -v garage.testing.TestVehicle garage.testing.TestCar garage.testing.TestMotorbike
```

Check the tasks (see [tasks/README.md](tasks/README.md) for every check command):
```bash
python -m pytest
python -m unittest discover -s tasks/11_testing/solution -v
```
`python -m pytest` needs pytest (`pip install pytest`); the `unittest` line runs the same tests with the standard
library.

---

## Teaching Approach

- Each file is a standalone, runnable example
- Concepts are explained in comments alongside working code
- Topics progress from simple to complex within each module
- Tasks give delegates a chance to apply what they've learned
- Third-party libraries are introduced only where they serve a teaching purpose (requests, SQLAlchemy, pandas)

---

## Tech Stack

| Technology             | Purpose                                  |
|------------------------|------------------------------------------|
| Python 3.10+           | Language                                 |
| unittest               | Testing framework (stdlib)               |
| SQLite                 | Embedded database (stdlib)               |
| SQLAlchemy 2.0+        | ORM introduction                         |
| requests               | HTTP client library                      |
| pandas                 | CSV chunked processing                   |
| mysql-connector-python | MySQL driver (used with SQLAlchemy)      |

No Django. No Flask. No Jupyter. No notebooks.

---

## What's Next?

This course covers Python fundamentals and OOP. For applied Python topics (web development, data engineering, automation), see the applied course repositories in this family.

For the same structured approach in other languages, see the companion repositories:

- [Java Zero to Hero](https://github.com/Edrzapi/Java_zero_hero)
- [C# Zero to Hero](https://github.com/Edrzapi/CS_zero_hero)
