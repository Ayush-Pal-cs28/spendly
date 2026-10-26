Implementation Plan: 01-Database Setup
1. Objective
Establish the SQLite data layer for Spendly by implementing database connection helper functions (get_db()), table creation logic (init_db()), and initial seed data creation (seed_db()), and integrating them into the Flask startup lifecycle in app.py.
2. Proposed Changes
A. Implement database/db.py
We will replace the stub comments with the complete database module using standard sqlite3 and werkzeug.security:
- get_db():
- Connects to spendly.db in the project root.
- Sets conn.row_factory = sqlite3.Row.
- Executes conn.execute("PRAGMA foreign_keys = ON") on every connection.
- Returns the connection object.
- init_db():
- Uses get_db() to run CREATE TABLE IF NOT EXISTS for two tables:
1. users:
- id INTEGER PRIMARY KEY AUTOINCREMENT
- name TEXT NOT NULL
- email TEXT UNIQUE NOT NULL
- password_hash TEXT NOT NULL
- created_at TEXT DEFAULT (datetime('now'))
2. expenses:
- id INTEGER PRIMARY KEY AUTOINCREMENT
- user_id INTEGER NOT NULL
- amount REAL NOT NULL
- category TEXT NOT NULL
- date TEXT NOT NULL (YYYY-MM-DD format)
- description TEXT
- created_at TEXT DEFAULT (datetime('now'))
- FOREIGN KEY (user_id) REFERENCES users (id)
- Commits changes and closes the connection.
- seed_db():
- Checks if any user exists in the users table. If so, returns early to prevent duplicates.
- Inserts a demo user (Demo User, demo@spendly.com, hashed password for demo123 via generate_password_hash).
- Inserts 8 sample expenses linked to the demo user across the fixed categories (Food, Transport, Bills, Health, Entertainment, Shopping, Other) with realistic dates (YYYY-MM-DD) within the current month.
- Commits changes and closes the connection.
B. Update app.py
- Import get_db, init_db, and seed_db from database.db.
- Add startup hooks to initialize and seed the database within an application context:
with app.app_context():
    init_db()
    seed_db()
3. Verification Plan
- Create a test file tests/test_db.py (or use pytest) to verify:
- get_db() returns a valid connection with row_factory and foreign key enforcement enabled.
- init_db() successfully creates both tables.
- seed_db() correctly populates the demo user and 8 expenses, and is idempotent (does not duplicate on repeated calls).
- Constraints (UNIQUE email, foreign key violation on invalid user_id) correctly raise sqlite3 integrity errors.
- Run pytest to ensure all tests pass.