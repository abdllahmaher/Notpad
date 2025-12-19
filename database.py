# database.py
import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

DB_PATH = "bot_data.db"

@contextmanager
def get_db_connection():
    """Get a database connection with automatic cleanup."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
        conn.commit()  # Save changes
    except Exception:
        conn.rollback()  # Undo changes on error
        raise
    finally:
        conn.close()

def init_database():
    """Initialize database tables if they don't exist."""
    with get_db_connection() as conn:
        # Notes table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                note TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Todos table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                task TEXT NOT NULL,
                done BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for faster queries
        conn.execute('CREATE INDEX IF NOT EXISTS idx_notes_user ON notes(user_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_todos_user ON todos(user_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_todos_done ON todos(done)')
        
        print("✅ Database initialized successfully")

# Initialize database when module loads
init_database()
