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

def test_register_get(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Create your account" in response.data
    assert b"Confirm password" in response.data

def test_register_success(client):
    response = client.post("/register", data={
        "name": "Test User",
        "email": "test@spendly.com",
        "password": "securepassword123",
        "confirm_password": "securepassword123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created successfully" in response.data
    
    # Check database
    with app.app_context():
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = 'test@spendly.com'").fetchone()
        assert user is not None
        assert user["name"] == "Test User"
        db.close()

def test_register_validation_errors(client):
    # Short password
    response = client.post("/register", data={
        "name": "Test User",
        "email": "test2@spendly.com",
        "password": "short",
        "confirm_password": "short"
    })
    assert response.status_code == 200
    assert b"Password must be at least 8 characters long." in response.data

    # Password mismatch
    response = client.post("/register", data={
        "name": "Test User",
        "email": "test2@spendly.com",
        "password": "securepassword123",
        "confirm_password": "differentpassword"
    })
    assert response.status_code == 200
    assert b"Passwords do not match." in response.data

    # Duplicate email
    response = client.post("/register", data={
        "name": "Another User",
        "email": "demo@spendly.com",
        "password": "securepassword123",
        "confirm_password": "securepassword123"
    })
    assert response.status_code == 200
    assert b"Email address is already registered." in response.data
