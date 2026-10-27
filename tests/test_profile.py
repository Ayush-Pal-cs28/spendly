import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    with app.test_client() as client:
        with app.app_context():
            from database.db import init_db, seed_db
            init_db()
            seed_db()
        yield client


def test_profile_requires_login(client):
    response = client.get("/profile", follow_redirects=True)
    # Should redirect to login page
    assert response.status_code == 200
    assert b"Sign in" in response.data or b"Email address" in response.data


def test_profile_renders_for_logged_in_user(client):
    # Log in as demo user
    response = client.post("/login", data={
        "email": "demo@spendly.com",
        "password": "demo123"
    }, follow_redirects=True)
    assert response.status_code == 200

    # Visit profile
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Demo User" in response.data
    assert b"demo@spendly.com" in response.data
    assert b"Spending by category" in response.data
    assert b"Recent expenses" in response.data
