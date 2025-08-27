import sqlite3

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    completed INTEGER
)
""")
conn.commit()

def get_tasks():
    cursor.execute("SELECT id, text, completed FROM tasks")
    return cursor.fetchall()

def add_task_db(text):
    cursor.execute("INSERT INTO tasks (text, completed) VALUES (?, 0)", (text,))
    conn.commit()

def update_task_db(task_id, text, completed):
    cursor.execute("UPDATE tasks SET text=?, completed=? WHERE id=?", (text, completed, task_id))
    conn.commit()

def delete_task_db(task_id):
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

def delete_completed_tasks():
    cursor.execute("DELETE FROM tasks WHERE completed=1")
    conn.commit()
