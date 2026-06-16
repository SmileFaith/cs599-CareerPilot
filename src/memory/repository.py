import sqlite3
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class MemoryRepository:
    """Repository layer for interacting with SQLite based long-term memory."""

    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initialize the database schema."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # user_progress table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        skill_name TEXT NOT NULL,
                        status TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')
                
                # interview_history table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS interview_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        score INTEGER,
                        feedback TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')
                
                conn.commit()
                logger.info("Database schema initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def create_user(self, name: str) -> int:
        """Create a new user and return their ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
            conn.commit()
            return cursor.lastrowid

    def save_user_progress(self, user_id: int, skill_name: str, status: str = "pending"):
        """Save a new skill progress entry for a user."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Check if skill already exists to avoid duplicates (optional, based on requirement)
            cursor.execute('SELECT id FROM user_progress WHERE user_id = ? AND skill_name = ?', (user_id, skill_name))
            if cursor.fetchone():
                logger.warning(f"Skill {skill_name} already exists for user {user_id}. Updating instead.")
                self.update_skill_status(user_id, skill_name, status)
                return
                
            cursor.execute(
                'INSERT INTO user_progress (user_id, skill_name, status) VALUES (?, ?, ?)',
                (user_id, skill_name, status)
            )
            conn.commit()

    def update_skill_status(self, user_id: int, skill_name: str, new_status: str):
        """Update the status of an existing skill for a user."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE user_progress SET status = ? WHERE user_id = ? AND skill_name = ?',
                (new_status, user_id, skill_name)
            )
            conn.commit()

    def load_user_progress(self, user_id: int) -> List[Dict[str, Any]]:
        """Load all skill progress history for a user."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, skill_name, status FROM user_progress WHERE user_id = ?',
                (user_id,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def save_interview_history(self, user_id: int, score: int, feedback: str):
        """Save an interview result for a user."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO interview_history (user_id, score, feedback) VALUES (?, ?, ?)',
                (user_id, score, feedback)
            )
            conn.commit()
