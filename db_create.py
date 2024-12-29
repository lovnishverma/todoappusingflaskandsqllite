import sqlite3

# Connect to SQLite database
def create_db():
    conn = sqlite3.connect('todo.db')
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
        did INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        task_id INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks(tid)
    )
    """)

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    print("Database and tables created successfully!")

if __name__ == '__main__':
    create_db()
