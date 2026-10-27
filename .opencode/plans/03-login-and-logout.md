# Implementation Plan: Login and Logout (`03-login-and-logout`)

Based on the spec (`.opencode/specs/03-login-and-logout.md`) and project conventions in `AGENTS.md`, here is the detailed plan for implementing user login and logout.

---

## 1. Database Helper (`database/db.py`)
- Check existing query functions from Step 2 (Registration). Ensure there is a parameterised query helper to fetch a user by username (e.g., `get_user_by_username(username)`).

## 2. Routes (`app.py`)
- **`GET /login`**:
  - Renders `login.html`.
- **`POST /login`**:
  - Extract `username` and `password` from `request.form`.
  - Validate that both fields are present. If missing, flash an error message and re-render `login.html`.
  - Query the database using parameterised queries to find the user by username.
  - Verify the password hash using Werkzeug security (`check_password_hash`).
  - If valid, store user identifier in `session` and redirect to profile or dashboard.
  - If invalid, flash an error message ("Invalid username or password") and re-render `login.html`.
- **`GET /logout`**:
  - Clear the user session (`session.clear()`).
  - Flash a success message.
  - Redirect to the landing page (`/`).

## 3. Templates
- **`templates/login.html`**:
  - Ensure form uses `method="POST"`.
  - Include fields for `username` and `password`.
  - Render flashed messages.
  - Extend `base.html` and use CSS variables.
- **`templates/base.html`**:
  - Update navigation links conditionally based on session state:
    - Logged in: Show "Logout" (`url_for('logout')`).
    - Logged out: Show "Login" (`url_for('login')`) and "Register" (`url_for('register')`).

## 4. Testing & Verification
- Add or update tests in `tests/test_app.py` covering successful login, failed login, logout, and navbar state.
- Run `pytest` via subagent to verify all test results.
