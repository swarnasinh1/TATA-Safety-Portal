import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    employeeid TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Reports Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT,
    employee_id TEXT,
    department TEXT,
    incident_date TEXT,
    incident_time TEXT,
    plant TEXT,
    location TEXT,
    incident_type TEXT,
    severity TEXT,
    description TEXT,
    status TEXT DEFAULT 'Open'
)
""")

conn.commit()
conn.close()

print("Database created successfully.")