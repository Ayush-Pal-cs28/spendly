---
# Spec: Registration

## Overview
This feature implements user registration for Spendly, allowing new users to sign up by providing their name, email, and password. It handles form submission, input validation (such as checking for missing fields, password confirmation matching, and duplicate email existence), password hashing using Werkzeug, database insertion via `database/db.py`, and session establishment for immediate login upon successful registration. On success  the user is shown with a success message and redirected to the login page. This is the entry point for all authenticated feature that follow.

## Depends on
- Step 01: Database Setup (`database/db.py`, `users` table schema)

## Routes
- `GET /register` — renders the registration form — public
- `POST /register` — processes registration form data, validates inputs, creates user, and logs them in — public

## Database changes
No database changes. Uses the existing `users` table schema (`id`, `name`, `email`, `password_hash`, `created_at`) defined in `database/db.py`.

A new DB helper must be added to `database/db.py`:
- `create_user(name, email, password)` — hashes the password with `werkzeug`, inserts a row into `users`, returns the new user's `id`. Raises `sqlite3.IntegrityError` if the email is already taken (UNIQUE constraint).

## Templates
- **Create:** None
- **Modify:** `templates/register.html` (update form action, method, inputs with `name` attributes, and flash/error message rendering (e.g. "Email already registered", "Passwords do not match"))
- keep all existing visual designs

## Files to change
- `app.py` — upgrade `register()` to handle `GET` and `POST`; add flash + redirect logic
- `database/db.py` — add `create_user()` helper
- `templates/register.html` — wire up form action/method and flash message display

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security` (`generate_password_hash`), Flask session, and SQLite helpers from `database/db.py`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done
- [ ] `GET /register` renders registration form extending `base.html`
- [ ] Submitting invalid data (empty fields, mismatched passwords, or existing email) shows appropriate error messages via flash/template
- [ ] Submitting valid registration details successfully hashes the password, inserts a new user record into the database, and logs the user in (setting session)
- [ ] Successfully registered user is redirected to the dashboard/home/profile as appropriate
- [ ] All database queries use parameterized placeholders
- [ ] No ORM or new pip packages introduced
---
