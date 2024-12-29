import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('todo.db', check_same_thread=False)
cursor = conn.cursor()

# Create tasks table with a timestamp column to sort tasks by their creation time
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    tid INTEGER PRIMARY KEY,
    task TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Create done table with a foreign key reference to the tasks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS done (
    did INTEGER PRIMARY KEY,
    task TEXT NOT NULL,
    task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(tid)
)
""")

# Close the cursor and the connection
cursor.close()
conn.close()
