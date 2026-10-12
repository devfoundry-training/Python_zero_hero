# ============================================================
# File I/O - Reading, Writing, Binary, Pickling, CSV, SQLite
# ============================================================
# File Modes:
#   'r'  -> Read (default)     'w'  -> Write (overwrite)
#   'a'  -> Append             'x'  -> Create (fail if exists)
#   'r+' -> Read and write     'w+' -> Create/truncate for r/w
#   'a+' -> Create/append for r/w
# ============================================================

import sys
import pickle
import csv
import sqlite3
import os

# ------------------------------------------------------------
# EAFP vs LBYL - Two Approaches to File Access
# ------------------------------------------------------------

# EAFP: Easier to Ask for Forgiveness than Permission
try:
    file = open("drop/Errors.txt", "r")  # Trying to open the file
    print("Reading file content:")
    print(file.read())
except Exception as e:
    print(f"Error occurred: {e}")  # Handling the error after it happens
finally:
    file.close()  # Ensures that the file is closed

# LBYL: Look Before You Leap
if os.path.exists("drop/Errors.txt"):  # Checking if the file exists first
    with open("drop/Errors.txt", "r") as file:
        print("Reading file content using 'with':")
        print(file.read())
else:
    print("File does not exist, cannot open it.")

# ------------------------------------------------------------
# Reading from Files
# ------------------------------------------------------------
with open("drop/Errors.txt", "r") as f:
    print("Read whole file:", f.read())
    f.seek(0)
    print("Read line by line:")
    for line in f:
        print(line.strip())

# Most Pythonic way to read a file line by line
with open("drop/Errors.txt", "r") as f:
    print("File content with for loop:")
    for line in f:
        print(line.strip())

# ------------------------------------------------------------
# Writing to Files
# ------------------------------------------------------------
with open("drop/Errors.txt", "a") as append_f:
    append_f.write("Appending new line to the file\n")
    append_f.writelines(["Another line\n", "Yet another line\n"])

# Using print() to write to files
with open("drop/Errors.txt", "w") as write_f:
    print("This is a new line.", file=write_f)

# ------------------------------------------------------------
# Binary Files
# ------------------------------------------------------------
with open("drop/binary.txt", "wb") as binary_f:
    binary_f.write(b"Binary data\n")

with open("drop/binary.txt", "rb") as binary_f:
    print("Reading binary data:")
    print(binary_f.read().decode())

# Writing and Reading Bytes (byte-like objects)
with open('drop/out.dat', 'wb') as dat_f:
    dat_f.write(b'Single bytes string ')
    s = "Native string as a line\r\n"
    dat_f.write(s.encode())

# ------------------------------------------------------------
# sys.stdin / sys.stdout - Low-Level I/O
# ------------------------------------------------------------
sys.stdout.write("Please enter a value: ")
sys.stdout.flush()
reply = sys.stdin.readline()
safe_reply = sys.stdin.readline().strip()
print(f"Input was: {reply} and {safe_reply}")

# ------------------------------------------------------------
# File Navigation - seek() and tell()
# ------------------------------------------------------------
with open("drop/Errors.txt", "r") as f:
    f.seek(0)  # Move to the beginning
    print("Current position:", f.tell())  # Shows current file position

# ------------------------------------------------------------
# Pickling - Serialising Python Objects
# ------------------------------------------------------------
new_obj = {"key": "value", "number": 42}
with open('drop/pickle-file.pickle', 'wb') as pickle_f:
    pickle.dump(new_obj, pickle_f)

# To load the object back from the pickle file
with open('drop/pickle-file.pickle', 'rb') as pickle_f:
    stored_obj = pickle.load(pickle_f)
    print("Pickled object:", stored_obj)

# ------------------------------------------------------------
# CSV - Reading and Writing
# ------------------------------------------------------------
csv_data = [["Name", "Age"], ["Alice", 30], ["Bob", 25]]
with open('drop/people.csv', 'w', newline='') as csv_f:
    writer = csv.writer(csv_f)
    writer.writerows(csv_data)

# Reading CSV files
with open('drop/people.csv', 'r') as csv_f:
    reader = csv.reader(csv_f)
    for row in reader:
        print("CSV Row:", row)

# ------------------------------------------------------------
# SQLite - Quick Database Example
# ------------------------------------------------------------
conn = sqlite3.connect('drop/my_database.db')
cursor = conn.cursor()

# Creating a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Inserting data
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 30))
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 25))
conn.commit()

# Querying data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print("Database query results:")
for row in rows:
    print(row)

# Closing the connection
conn.close()
