# Implementation Plan: Profile Page (Step 04)

## 1. Overview & Goal
Replace the existing `/profile` stub route in `app.py` with a fully featured, elegant profile page that presents:
- **User Info Card:** Avatar initials, user name, email, and member-since date.
- **Summary Stats Row:** Four metrics (Month total, Transaction count, Top category, Daily average).
- **Spending by Category Breakdown:** Category progress bars and totals.
- **Recent Expenses Table:** Tabular transaction history with action links (edit/delete).
- **Authentication Protection:** Redirect unauthenticated users (`session.get("user_id")` absent) to `/login`.

---

## 2. Component & Asset Reuse (from `spendly-ui-designer` skill)
To maintain Spendly's consistent warm editorial aesthetic and strict rules:
- **Icons (`_icons.html`):** Copy the Lucide icon macro to `templates/_icons.html`.
- **Reusable Macros (`_components.html`):** Copy helper macros (`money`, `short_date`, `category_badge`, `stat_card`, `empty_state`) to `templates/_components.html`.
- **Styling (`static/css/profile.css`):** Create the dedicated page stylesheet defining elevation shadows, spacing scale, and category tokens as specified in the design system.
- **Interactivity (`static/js/profile.js`):** Add lightweight vanilla JS for delete confirmation dialogs.

---

## 3. Detailed File Changes

### A. `app.py`
- Update route `GET /profile`:
  - Check `if "user_id" not in session: return redirect(url_for("login"))`.
  - Fetch user details using `get_db()` helper.
  - Fetch user expenses and compute stats (month total, count, top category, daily average, category totals).
  - Render `profile.html` with context variables: `user`, `stats`, `category_totals`, `expenses`.

### B. Templates & Assets to Create
1. **`templates/_icons.html`** — Lucide SVG icon macro.
2. **`templates/_components.html`** — UI component macros (`money`, `stat_card`, `category_badge`, etc.).
3. **`templates/profile.html`** — The profile page template extending `base.html`.
4. **`static/css/profile.css`** — CSS variables, card layout, stat grid, category bars, and responsive media queries.
5. **`static/js/profile.js`** — Confirmations for destructive actions.
6. **`tests/test_profile.py`** — Pytest suite verifying unauthenticated redirects, 200 OK for logged-in users, stats display, and data rendering.

---

## 4. Step-by-Step Verification & Definition of Done
- Visiting `/profile` while unauthenticated redirects to `/login`.
- Visiting `/profile` while logged in returns status 200.
- User info, stat cards, category breakdown, and recent expenses table render correctly.
- All pytest tests pass successfully (`pytest`).
