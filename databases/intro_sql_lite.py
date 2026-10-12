# ============================================================
# SQLite - Full CRUD with Python's sqlite3 Module
# ============================================================
# SQLite is serverless and stores everything in a single file.
# Ideal for local storage, prototyping, and teaching SQL.
# Note: SQLite is dynamically typed - it doesn't enforce column
# types as strictly as MySQL or PostgreSQL.
# ============================================================

import sqlite3

# It's good practice to use 'with' to manage database connections.
# This ensures the connection is automatically closed when done.
# Using 'with' also helps in managing resources properly and avoids memory leaks.
with sqlite3.connect("example.db") as conn:
    c = conn.cursor()  # Create a cursor object, used to interact with the database

    # ============================
    # CREATE: Creating a new table
    # ============================

    # Create a table if it does not exist already.
    # It's better to use the "IF NOT EXISTS" clause to prevent errors if the table already exists.
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,  
            name TEXT NOT NULL,      
            age INTEGER,             
            grade TEXT               
        )
    """)

    # Commit the transaction to save the changes to the database.
    conn.commit()

    # ============================
    # INSERT: Inserting data into the table
    # ============================

    # Here, we're using placeholders "?" instead of directly passing variables in the SQL statement.
    # This helps prevent SQL injection attacks and makes the code safer.

    # Before inserting, check if the data already exists
    c.execute("SELECT * FROM students WHERE name = ? AND age = ? AND grade = ?", ("chris", 40, "A"))

    # If no data matches the condition, insert the data
    if c.fetchone() is None:
        c.execute("""
            INSERT INTO students (name, age, grade)
            VALUES (?, ?, ?)  
        """, ("chris", 40, "A"))
        # Use placeholders for safe insertion
        conn.commit()  # Save the new record to the database
    else:
        print("already in the db")  # If the record already exists, don't insert it again

    # ============================
    # UPDATE: Modifying data
    # ============================

    # To update existing records, you can use the UPDATE statement.
    # Here, we are changing "chris"'s grade from "A" to "B".
    c.execute("""
        UPDATE students
        SET grade = ?
        WHERE name = ?
    """, ("B", "chris"))
    conn.commit()  # Save the changes to the database

    # ============================
    # QUERY: Retrieving data from the table
    # ============================

    # You can retrieve data from the table using SELECT queries.
    # Here we fetch all records from the "students" table.
    c.execute("SELECT * FROM students")
    x = c.fetchall()  # Get all rows as a list of tuples

    # Loop through and print each row in the table
    for data in x:
        print(data)

    # ============================
    # DELETE: Removing data from the table
    # ============================

    # This will delete a student record where the name matches "chris".
    c.execute("""
        DELETE FROM students
        WHERE name = ?
    """, ("chris",))
    conn.commit()  # Save the changes (record is deleted)

    # ============================
    # EXECUTE MANY: Insert multiple rows at once
    # ============================

    # If you want to insert multiple records at once, you can use `executemany()`.
    # This is more efficient than calling `execute()` for each record.

    students_data = [
        ("person1", 22, "A"),
        ("person2", 30, "B"),
        ("person3", 60, "A")
    ]  # List of tuples with data to insert

    # Insert multiple rows using executemany
    c.executemany("""
        INSERT INTO students (name, age, grade)
        VALUES (?, ?, ?)  
    """, students_data)
    conn.commit()  # Save all records to the database

    # ============================
    # QUERY: Retrieving data again
    # ============================

    # Retrieve and print all the data from the table after insertions.
    c.execute("SELECT * FROM students")
    x = c.fetchall()  # Get all rows as a list of tuples

    for data in x:
        print(data)
