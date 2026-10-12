# ============================================================
# Basic SQL Handling - Raw SQL with SQLite
# ============================================================
# Demonstrates CRUD operations using Python's built-in sqlite3
# module. No ORM, no external dependencies.
# ============================================================

import sqlite3

# ------------------------------------------------------------
# Connection and Table Setup
# ------------------------------------------------------------
# Using a context manager ensures the connection is closed
# automatically, even if an error occurs.

with sqlite3.connect(":memory:") as conn:
    cursor = conn.cursor()

    # Create a table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT,
            salary REAL
        )
    """)

    # ------------------------------------------------------------
    # INSERT - Adding records
    # ------------------------------------------------------------
    # Always use parameterised queries (?) to prevent SQL injection.

    cursor.execute(
        "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
        ("Alice", "Engineering", 75000.00)
    )

    # Insert multiple rows at once with executemany
    employees = [
        ("Bob", "Marketing", 55000.00),
        ("Charlie", "Engineering", 80000.00),
        ("Diana", "HR", 60000.00),
    ]
    cursor.executemany(
        "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
        employees
    )
    conn.commit()

    # ------------------------------------------------------------
    # SELECT - Querying data
    # ------------------------------------------------------------

    # Fetch all rows
    cursor.execute("SELECT * FROM employees")
    print("All employees:")
    for row in cursor.fetchall():
        print(f"  {row}")

    # Fetch with a filter
    cursor.execute(
        "SELECT name, salary FROM employees WHERE department = ?",
        ("Engineering",)
    )
    print("\nEngineering department:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: £{row[1]:,.2f}")

    # ------------------------------------------------------------
    # UPDATE - Modifying records
    # ------------------------------------------------------------

    cursor.execute(
        "UPDATE employees SET salary = ? WHERE name = ?",
        (90000.00, "Charlie")
    )
    conn.commit()

    # Verify the update
    cursor.execute("SELECT name, salary FROM employees WHERE name = ?", ("Charlie",))
    print(f"\nUpdated: {cursor.fetchone()}")

    # ------------------------------------------------------------
    # DELETE - Removing records
    # ------------------------------------------------------------

    cursor.execute("DELETE FROM employees WHERE name = ?", ("Bob",))
    conn.commit()

    # Verify the delete
    cursor.execute("SELECT COUNT(*) FROM employees")
    print(f"\nRemaining employees: {cursor.fetchone()[0]}")

    # ------------------------------------------------------------
    # Aggregate Queries
    # ------------------------------------------------------------

    cursor.execute("SELECT department, AVG(salary) FROM employees GROUP BY department")
    print("\nAverage salary by department:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: £{row[1]:,.2f}")
