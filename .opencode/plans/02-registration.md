# Implementation Plan — Step 02: Registration

## Overview
This feature implements user registration for Spendly, allowing new users to sign up by providing their name, email, and password. It handles form submission, input validation (such as checking for missing fields, password confirmation matching, and duplicate email existence), password hashing using Werkzeug, database insertion via `database/db.py`, and redirection to the login page with a success message upon successful registration.

## Depends on
- Step 01: Database Setup (`database/db.py`, `users` table schema)

## Scope Summary
- Add working `POST /register` route that validates input, hashes passwords, and inserts users via `create_user()` in `database/db.py`.
- `GET /register` renders the registration form.
- Visual design remains unchanged.
- No new pip packages or ORMs introduced.

---

## File-by-File Plan

### 1. `database/db.py`
- Add `create_user(name, email, password)` helper:
  - Normalise email (`email.strip().lower()`) and name (`name.strip()`).
  - Hash password using `generate_password_hash(password)`.
  - Execute parameterized `INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)`.
  - Commit transaction, capture `cursor.lastrowid`, return user ID.
  - Close connection in a `finally` block.
  - Allow `sqlite3.IntegrityError` to propagate so the route layer can catch duplicate emails.

### 2. `app.py`
- Set `app.secret_key` (environment variable with a development fallback).
- Import `flash`, `redirect`, `request`, `url_for` from `flask`, and `create_user` from `database.db`.
- Update `@app.route("/register", methods=["GET", "POST"])`:
  - **GET:** Renders `register.html`.
  - **POST:**
    - Extract and strip `name`, `email`, `password`, `confirm_password`.
    - Validate:
      - All required fields present.
      - Password length $\ge$ 8 characters.
      - `password == confirm_password`.
    - Try creating user via `create_user()`; catch `sqlite3.IntegrityError` for duplicate email.
    - On success: flash success message (`"Account created successfully. Please sign in."`, `"success"`) and redirect to `url_for("login")`.
    - On error: re-render `register.html` with error message and repopulate `name` and `email`.

### 3. `templates/register.html`
- Add confirmation password input field (`name="confirm_password"`).
- Update form `action` to `{{ url_for('register') }}`.
- Preserve input values on failed validation.
- Maintain existing card and styling classes.

### 4. `templates/base.html`
- Add a global flash messages block inside `<main>` above `{% block content %}` supporting category classes (`auth-error`, `auth-success`).

### 5. `static/css/style.css`
- Add `.auth-success` class mirroring `.auth-error` using theme CSS variables (`--accent-light`, `--accent`, `--radius-sm`).

---

## Validation & Error Handling Matrix

| Condition | Action / Result |
|---|---|
| Any required field empty | Re-render form, display error: "All fields are required." |
| Password length < 8 | Re-render form, display error: "Password must be at least 8 characters." |
| Passwords do not match | Re-render form, display error: "Passwords do not match." |
| Email already registered | Catch `IntegrityError`, re-render form, display error: "Email already registered." |
| Valid registration | Hash password, insert user, flash success, redirect to `/login`. |

---

## Verification Plan
1. Run application via `venv\Scripts\python app.py`.
2. Navigate to `http://127.0.0.1:5001/register`.
3. Test validation errors (blank fields, short password, mismatched confirmation, duplicate email).
4. Test successful registration and check redirect to `/login` with success banner.
5. Inspect SQLite database to verify password hashing (Werkzeug format, not plaintext) and auto-populated `created_at`.
6. Run `pytest` to ensure all database and registration tests pass successfully.
