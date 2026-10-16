import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect(
    "database/workforce.db",
    check_same_thread=False
)

cursor = conn.cursor()

# Create the employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    start_date TEXT,
    location TEXT,
    role TEXT
)
""")

conn.commit()
