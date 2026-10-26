import os
import sqlite3
import pytest
from flask import Flask
from database.db import get_db, init_db, seed_db

@pytest.fixture
def app():
    # Use an in-memory or temporary database for testing
    app = Flask(__name__)
    app.config["TESTING"] = True
    
    # Override DATABASE in db module or test with default spendly.db if appropriate,
    # but since db.py uses "spendly.db", let's clean up spendly.db before/after if needed.
    if os.path.exists("spendly.db"):
        os.remove("spendly.db")
        
    with app.app_context():
        init_db()
        seed_db()
        
    yield app
    
    if os.path.exists("spendly.db"):
        os.remove("spendly.db")

def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is not None
        # Check row_factory
        assert db.row_factory == sqlite3.Row
        # Check foreign keys enabled
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys;")
        row = cursor.fetchone()
        assert row[0] == 1
        db.close()

def test_init_and_seed_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Check user exists
        cursor.execute("SELECT * FROM users WHERE email = 'demo@spendly.com'")
        user = cursor.fetchone()
        assert user is not None
        assert user["name"] == "Demo User"
        
        # Check expenses exist (8 expenses)
        cursor.execute("SELECT COUNT(*) FROM expenses WHERE user_id = ?", (user["id"],))
        count = cursor.fetchone()[0]
        assert count == 8
        
        db.close()

def test_idempotent_seed(app):
    with app.app_context():
        # Running seed_db again should not duplicate records
        seed_db()
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        assert cursor.fetchone()[0] == 1
        cursor.execute("SELECT COUNT(*) FROM expenses")
        assert cursor.fetchone()[0] == 8
        db.close()

def test_constraints(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Test unique email constraint
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                ("Another User", "demo@spendly.com", "hash")
            )
            db.commit()
            
        # Test foreign key constraint on expenses
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)",
                (9999, 10.0, "Food", "2026-10-21")
            )
            db.commit()
            
        db.close()
