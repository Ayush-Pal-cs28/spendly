---
# Spec: Login and Logout

## Overview
This feature implements user login and logout functionality for Spendly. It allows registered users to securely authenticate using their username and password via a login form, establishing a session. It also replaces the stub logout route with a fully functional logout route that clears the session, enabling users to log out safely and return to the landing or login page.

## Depends on
- 01-databse-setup (`user` table must exists)
- 02-registration (`create_user` and password hashing must be in place; a user must exist to log in against)

## Routes
- `GET /login` — render login form — public
- `POST /login` — process user login credentials and create session — public
- `GET /logout` — destroy user session and redirect to landing page — logged-in

## Database changes
No database changes. Uses existing `users` table.

## Templates
- **Create:** None
- **Modify:** 
  - `templates/login.html` — update login form to submit via POST with proper fields and error handling
  - `templates/base.html` — update navigation links to toggle between Login/Register and Logout based on session status

## Files to change
- `app.py`
- `templates/login.html`
- `templates/base.html`
- `tests/test_app.py` (if applicable for tests)

## Files to create
None

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done
- [] Visiting `/login` renders the login form.
- [] Submitting valid credentials logs the user in and redirects to the dashboard/home or profile.
- [] Submitting invalid credentials shows an appropriate error message on the login page.
- [] Visiting `/logout` successfully clears the session and redirects to the landing page.
- [] Navigation bar correctly reflects authentication state (showing Logout when logged in, Login/Register when logged out).
- [] All tests pass successfully.
---
