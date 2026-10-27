import os
import pytest
from app import app
from database.db import get_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "localhost:5001"
    if os.path.exists("spendly.db"):
        os.remove("spendly.db")
    with app.app_context():
        from database.db import init_db, seed_db
        init_db()
        seed_db()
    with app.test_client() as client:
        yield client
    if os.path.exists("spendly.db"):
        os.remove("spendly.db")

def test_login_get(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Sign in to your Spendly account" in response.data

def test_login_success(client):
    response = client.post("/login", data={
        "email": "demo@spendly.com",
        "password": "demo123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome back, Demo User!" in response.data
    assert b"Track every rupee. Own your finances." in response.data

def test_login_invalid_credentials(client):
    response = client.post("/login", data={
        "email": "demo@spendly.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 200
    assert b"Invalid email or password." in response.data

def test_logout(client):
    # First login
    client.post("/login", data={
        "email": "demo@spendly.com",
        "password": "demo123"
    }, follow_redirects=True)

    # Then logout
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been logged out successfully." in response.data
    assert b"Sign in" in response.data

def test_logged_in_user_redirected_from_login_and_register(client):
    # Login first
    client.post("/login", data={
        "email": "demo@spendly.com",
        "password": "demo123"
    }, follow_redirects=True)

    # Attempt to visit /login while logged in
    res_login = client.get("/login", follow_redirects=True)
    assert res_login.status_code == 200
    # Should be redirected to landing (or home) page
    assert b"Sign in to your Spendly account" not in res_login.data
    assert b"Track every rupee. Own your finances." in res_login.data

    # Attempt to visit /register while logged in
    res_reg = client.get("/register", follow_redirects=True)
    assert res_reg.status_code == 200
    assert b"Create your account" not in res_reg.data
    assert b"Track every rupee. Own your finances." in res_reg.data
