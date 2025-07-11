from flask import Flask, render_template, request, jsonify, redirect
import sqlite3

app = Flask(__name__)

# Function to create a database connection
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch tasks from the tasks table (not yet done)
    cursor.execute("SELECT * FROM tasks ORDER BY timestamp DESC")
    tasks = cursor.fetchall()

    # Fetch tasks from the done table (completed tasks)
    cursor.execute("SELECT * FROM done ORDER BY timestamp DESC")
    completed_tasks = cursor.fetchall()

    conn.close()  # Always close the connection
    return render_template('index.html', tasks=tasks, done=completed_tasks)


@app.route('/addTask', methods=['GET'])
def add_task():
    task = request.args.get('task')
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert the task into the tasks table
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    
    conn.close()
    return redirect('/')


@app.route('/move-to-done/<int:task_id>', methods=['POST'])
def move_to_done(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the task from the tasks table
    cursor.execute("SELECT * FROM tasks WHERE tid = ?", (task_id,))
    task = cursor.fetchone()

    if task:
        # Insert the task into the done table
        cursor.execute("INSERT INTO done (task, task_id) VALUES (?, ?)", (task[1], task[0]))
        conn.commit()

        # Remove the task from the tasks table
        cursor.execute("DELETE FROM tasks WHERE tid = ?", (task_id,))
        conn.commit()

        conn.close()
        return jsonify({"success": True, "message": "Task marked as done!"})
    else:
        conn.close()
        return jsonify({"success": False, "message": "Task not found"})


@app.route('/deleteTask/<int:id>', methods=['GET'])
def delete_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete the task from the tasks table
    cursor.execute("DELETE FROM tasks WHERE tid = ?", (id,))
    conn.commit()
    
    conn.close()
    return redirect('/')


@app.route('/delete-completed/<int:id>', methods=['GET'])
def delete_completed_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete the task from the done table
    cursor.execute("DELETE FROM done WHERE did = ?", (id,))
    conn.commit()
    
    conn.close()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=7860)
