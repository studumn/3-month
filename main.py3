import flet as ft
from flet import Icons
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

def update_task_db(task_id, text=None, completed=None):
    if text is not None and completed is not None:
        cursor.execute("UPDATE tasks SET text=?, completed=? WHERE id=?", (text, completed, task_id))
    elif text is not None:
        cursor.execute("UPDATE tasks SET text=? WHERE id=?", (text, task_id))
    elif completed is not None:
        cursor.execute("UPDATE tasks SET completed=? WHERE id=?", (completed, task_id))
    conn.commit()

def delete_task_db(task_id):
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

def delete_completed_tasks():
    cursor.execute("DELETE FROM tasks WHERE completed=1")
    conn.commit()

def main(page: ft.Page):
    page.title = "Todo List"
    page.theme_mode = ft.ThemeMode.DARK

    task_list = ft.Column(spacing=10)

    def load_tasks():
        task_list.controls.clear()
        for t in get_tasks():
            task_list.controls.append(create_task_row(t[0], t[1], t[2]))
        page.update()

    def create_task_row(task_id, text, completed):
        checkbox = ft.Checkbox(value=bool(completed))
        field = ft.TextField(value=text, expand=True)

        def on_text_change(e):
            update_task_db(task_id, text=field.value)
        field.on_change = on_text_change

        def on_checkbox_change(e):
            update_task_db(task_id, completed=int(checkbox.value))
        checkbox.on_change = on_checkbox_change

        delete_btn = ft.IconButton(Icons.DELETE, on_click=lambda e: delete(task_id))

        return ft.Row([checkbox, field, delete_btn])

    def add_task(e):
        if input_field.value.strip():
            add_task_db(input_field.value.strip())
            input_field.value = ""
            load_tasks()

    def delete(task_id):
        delete_task_db(task_id)
        load_tasks()

    def clear_completed(e):
        delete_completed_tasks()
        load_tasks()

    input_field = ft.TextField(hint_text="Добавьте задачу", expand=True)
    add_btn = ft.ElevatedButton("Добавить", on_click=add_task)
    clear_btn = ft.ElevatedButton("Очистить выполненные", on_click=clear_completed)

    page.add(ft.Column([
        ft.Row([input_field, add_btn]),
        clear_btn,
        task_list
    ]))

    load_tasks()

ft.app(target=main)
