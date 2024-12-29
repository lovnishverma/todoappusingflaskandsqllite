from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY timestamp DESC').fetchall()
    done_tasks = conn.execute('SELECT * FROM done ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks, done=done_tasks)

@app.route('/addTask', methods=['GET'])
def add_task():
    task = request.args.get('task')
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/move-to-done/<int:task_id>', methods=['POST'])
def move_to_done(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE tid = ?', (task_id,)).fetchone()
    if task:
        conn.execute('INSERT INTO done (task, task_id) VALUES (?, ?)', (task['task'], task['tid']))
        conn.execute('DELETE FROM tasks WHERE tid = ?', (task_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Task moved to done!"})
    else:
        conn.close()
        return jsonify({"success": False, "message": "Task not found!"})

@app.route('/deleteTask/<int:id>', methods=['GET'])
def delete_task(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE tid = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete-completed/<int:id>', methods=['GET'])
def delete_completed_task(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM done WHERE did = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
