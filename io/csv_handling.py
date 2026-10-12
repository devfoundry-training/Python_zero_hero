# ============================================================
# CSV Handling - Chunked Reading/Writing with csv and pandas
# ============================================================

import csv
import pandas as pd

# ------------------------------------------------------------
# Reading CSV in Chunks - stdlib csv module
# ------------------------------------------------------------


def process_chunk(chunk):
    """Process a batch of rows. Replace with your own logic."""
    for row in chunk:
        print(row)


chunk_size = 1000
chunk = []

with open('large_dataset.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Skip header row

    for row in csv_reader:
        chunk.append(row)
        if len(chunk) >= chunk_size:
            process_chunk(chunk)
            chunk = []

    if chunk:
        process_chunk(chunk)

# ------------------------------------------------------------
# Reading CSV in Chunks - pandas
# ------------------------------------------------------------

chunks = pd.read_csv('large_dataset.csv', chunksize=chunk_size)

for chunk in chunks:
    print(chunk.head())

# ------------------------------------------------------------
# Writing CSV in Chunks - stdlib csv module
# ------------------------------------------------------------

data = [['Name', 'Age'], ['Alice', 30], ['Bob', 25], ['Charlie', 35]]
chunk = []

with open('output.csv', mode='w', newline='') as file:
    csv_writer = csv.writer(file)

    for row in data:
        chunk.append(row)
        if len(chunk) >= chunk_size:
            csv_writer.writerows(chunk)
            chunk = []

    if chunk:
        csv_writer.writerows(chunk)

# ------------------------------------------------------------
# Writing CSV - pandas DataFrame
# ------------------------------------------------------------

data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [30, 25, 35]}
df = pd.DataFrame(data)
df.to_csv('output.csv', index=False)
