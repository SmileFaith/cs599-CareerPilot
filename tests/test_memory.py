import pytest
import sqlite3
from src.memory.repository import MemoryRepository


@pytest.fixture
def repo():
    # Use SQLite in-memory database for testing
    repository = MemoryRepository("test_memory.db")
    yield repository


def test_create_user(repo):
    user_id = repo.create_user("Alice")
    assert user_id > 1
    
    user_id_2 = repo.create_user("Bob")
    assert user_id_2 > user_id


def test_save_and_load_user_progress(repo):
    user_id = repo.create_user("Charlie")
    
    repo.save_user_progress(user_id, "Python", "pending")
    repo.save_user_progress(user_id, "Docker", "in_progress")
    
    progress = repo.load_user_progress(user_id)
    assert len(progress) == 2
    
    # Verify contents
    skills = {p["skill_name"]: p["status"] for p in progress}
    assert skills["Python"] == "pending"
    assert skills["Docker"] == "in_progress"


def test_update_skill_status(repo):
    user_id = repo.create_user("Dave")
    repo.save_user_progress(user_id, "Kubernetes", "pending")
    
    # Update status to completed
    repo.update_skill_status(user_id, "Kubernetes", "completed")
    
    progress = repo.load_user_progress(user_id)
    assert len(progress) == 1
    assert progress[0]["status"] == "completed"


def test_upsert_behavior_in_save(repo):
    user_id = repo.create_user("Eve")
    # Initial save
    repo.save_user_progress(user_id, "AWS", "pending")
    # Calling save again with same skill should update it
    repo.save_user_progress(user_id, "AWS", "completed")
    
    progress = repo.load_user_progress(user_id)
    assert len(progress) == 1
    assert progress[0]["skill_name"] == "AWS"
    assert progress[0]["status"] == "completed"


def test_save_interview_history(repo):
    user_id = repo.create_user("Frank")
    repo.save_interview_history(user_id, 85, "Good technical skills, need more confidence.")
    
    with repo._get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM interview_history WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        assert len(rows) == 1
        history = dict(rows[0])
        assert history["score"] == 85
        assert history["feedback"] == "Good technical skills, need more confidence."
