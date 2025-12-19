# notes.py
from database import get_db_connection

def add_note(user_id, note_text):
    """Add a new note for the user."""
    try:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO notes (user_id, note) VALUES (?, ?)",
                (str(user_id), note_text)
            )
        return True
    except Exception as e:
        print(f"❌ Error adding note: {e}")
        return False

def list_notes(user_id):
    """Get all notes for a user, newest first."""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT note FROM notes WHERE user_id = ? ORDER BY created_at DESC",
                (str(user_id),)
            )
            return [row['note'] for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Error listing notes: {e}")
        return []

def delete_note(user_id, note_index):
    """Delete a specific note by its position in the list."""
    notes = list_notes(user_id)
    
    if 1 <= note_index <= len(notes):
        note_to_delete = notes[note_index - 1]
        try:
            with get_db_connection() as conn:
                conn.execute(
                    "DELETE FROM notes WHERE user_id = ? AND note = ? LIMIT 1",
                    (str(user_id), note_to_delete)
                )
            return True
        except Exception as e:
            print(f"❌ Error deleting note: {e}")
    
    return False

def delete_all(user_id):
    """Delete all notes for a user."""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM notes WHERE user_id = ?",
                (str(user_id),)
            )
            return cursor.rowcount > 0
    except Exception as e:
        print(f"❌ Error deleting all notes: {e}")
        return False
