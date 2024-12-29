import sqlite3

def create_db():
    # Connect to SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    # Create tasks table with a timestamp column
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        tid INTEGER PRIMARY KEY,
        task TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create done table with task_id as a foreign key reference to tasks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS done (
        did INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        task_id INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks(tid)
    )
    """)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Call the function to create the database and tables
create_db()
