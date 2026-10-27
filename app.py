from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id, get_expenses_by_user
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "spendly-secret-key-change-in-production"

# Initialize and seed database on startup
with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            error = "All fields are required."
            return render_template("register.html", error=error, name=name, email=email)

        if len(password) < 8:
            error = "Password must be at least 8 characters long."
            return render_template("register.html", error=error, name=name, email=email)

        if password != confirm_password:
            error = "Passwords do not match."
            return render_template("register.html", error=error, name=name, email=email)

        try:
            create_user(name, email, password)
            flash("Account created successfully! Please sign in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            error = "Email address is already registered."
            return render_template("register.html", error=error, name=name, email=email)

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            error = "Both email and password are required."
            return render_template("login.html", error=error, email=email)

        user = get_user_by_email(email)
        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Invalid email or password."
            return render_template("login.html", error=error, email=email)

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("landing"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("login"))

    expenses = get_expenses_by_user(session["user_id"])

    # Compute stats
    count = len(expenses)
    month_total = sum(e["amount"] for e in expenses)

    # Top category
    cat_totals = {}
    for e in expenses:
        cat = e["category"]
        cat_totals[cat] = cat_totals.get(cat, 0.0) + e["amount"]

    top_category = "—"
    if cat_totals:
        top_category = max(cat_totals, key=cat_totals.get)

    daily_avg = month_total / 30.0 if count > 0 else 0.0

    stats = {
        "month_total": month_total,
        "count": count,
        "top_category": top_category,
        "daily_avg": daily_avg
    }

    # Category totals with percentages
    category_totals = []
    if month_total > 0:
        sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
        for cat, total in sorted_cats:
            percent = (total / month_total) * 100
            category_totals.append({
                "category": cat,
                "total": total,
                "percent": percent
            })

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        category_totals=category_totals,
        expenses=expenses
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
