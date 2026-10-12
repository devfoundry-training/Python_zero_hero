# ============================================================
# JSON Handling - Reading, Writing, and Parsing JSON
# ============================================================

import json

# ------------------------------------------------------------
# Writing JSON to a File
# ------------------------------------------------------------

data = {
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "SQL", "Azure"],
    "active": True
}

with open("drop/sample.json", "w") as f:
    json.dump(data, f, indent=4)

print("JSON written to file.")

# ------------------------------------------------------------
# Reading JSON from a File
# ------------------------------------------------------------

with open("drop/sample.json", "r") as f:
    loaded = json.load(f)

print("Loaded from file:", loaded)
print("Name:", loaded["name"])
print("Skills:", loaded["skills"])

# ------------------------------------------------------------
# JSON Strings - dumps() and loads()
# ------------------------------------------------------------

# Convert a Python object to a JSON string
json_string = json.dumps(data, indent=2)
print("JSON string:\n", json_string)

# Convert a JSON string back to a Python object
parsed = json.loads(json_string)
print("Parsed back:", parsed)

# ------------------------------------------------------------
# Working with Nested JSON
# ------------------------------------------------------------

nested = {
    "company": "Devfoundry",
    "employees": [
        {"name": "Alice", "role": "Trainer"},
        {"name": "Bob", "role": "Developer"}
    ]
}

json_nested = json.dumps(nested, indent=4)
print("Nested JSON:\n", json_nested)

# Access nested data after parsing
parsed_nested = json.loads(json_nested)
for emp in parsed_nested["employees"]:
    print(f"  {emp['name']} - {emp['role']}")
