import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "spendly.db"

def get_db():
    """Opens a connection to the SQLite database with row factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Creates tables if they do not already exist."""
    conn = get_db()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
    conn.close()

def seed_db():
    """Inserts demo user and sample expenses if the database is empty."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if users already exist
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count > 0:
        conn.close()
        return

    # Insert demo user
    password_hash = generate_password_hash("demo123")
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash)
    )
    user_id = cursor.lastrowid

    # Insert 8 sample expenses covering all categories
    sample_expenses = [
        (user_id, 14.50, "Food", "2026-10-02", "Lunch with colleagues"),
        (user_id, 45.00, "Transport", "2026-10-05", "Monthly metro pass"),
        (user_id, 120.00, "Bills", "2026-10-07", "Electricity bill"),
        (user_id, 35.00, "Health", "2026-10-10", "Pharmacy prescription"),
        (user_id, 60.00, "Entertainment", "2026-10-12", "Movie tickets and snacks"),
        (user_id, 85.20, "Shopping", "2026-10-15", "Groceries and household items"),
        (user_id, 22.00, "Food", "2026-10-18", "Coffee and pastry"),
        (user_id, 15.00, "Other", "2026-10-20", "Charity donation")
    ]

    cursor.executemany(
        """
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        sample_expenses
    )

    conn.commit()
    conn.close()


def get_user_by_email(email):
    """Fetches a user record by email."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()
    finally:
        conn.close()


def get_user_by_id(user_id):
    """Fetch user record by ID."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
    finally:
        conn.close()


def get_expenses_by_user(user_id):
    """Fetch all expenses for a given user, newest first."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, user_id, amount, category, date, description, created_at
            FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
            """,
            (user_id,)
        )
        return cursor.fetchall()
    finally:
        conn.close()


def create_user(name, email, password):
    """Creates a new user with a hashed password. Returns True on success, raises sqlite3.IntegrityError if email exists."""
    conn = get_db()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        return True
    finally:
        conn.close()
