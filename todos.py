# todos.py
from database import get_db_connection

def add_todo(user_id, task):
    """Add a new todo task for the user."""
    try:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO todos (user_id, task) VALUES (?, ?)",
                (str(user_id), task)
            )
        return True
    except Exception as e:
        print(f"❌ Error adding todo: {e}")
        return False

def list_todos(user_id):
    """Get all todos for a user."""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT id, task, done FROM todos WHERE user_id = ? ORDER BY created_at",
                (str(user_id),)
            )
            todos = []
            for row in cursor.fetchall():
                todos.append({
                    'id': row['id'],
                    'task': row['task'],
                    'done': bool(row['done'])
                })
            return todos
    except Exception as e:
        print(f"❌ Error listing todos: {e}")
        return []

def mark_done(user_id, todo_index):
    """Mark a todo as done by its position in the list."""
    todos = list_todos(user_id)
    
    if 0 <= todo_index < len(todos):
        todo_id = todos[todo_index]['id']
        try:
            with get_db_connection() as conn:
                conn.execute(
                    "UPDATE todos SET done = 1 WHERE id = ?",
                    (todo_id,)
                )
            return True
        except Exception as e:
            print(f"❌ Error marking todo as done: {e}")
    
    return False

def delete_task(user_id, task_index):
    """Delete a specific task by its position in the list."""
    todos = list_todos(user_id)
    
    if 1 <= task_index <= len(todos):
        todo_id = todos[task_index - 1]['id']
        try:
            with get_db_connection() as conn:
                conn.execute(
                    "DELETE FROM todos WHERE id = ?",
                    (todo_id,)
                )
            return True
        except Exception as e:
            print(f"❌ Error deleting task: {e}")
    
    return False

def delete_all_tasks(user_id):
    """Delete all tasks for a user."""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM todos WHERE user_id = ?",
                (str(user_id),)
            )
            return cursor.rowcount > 0
    except Exception as e:
        print(f"❌ Error deleting all tasks: {e}")
        return False
