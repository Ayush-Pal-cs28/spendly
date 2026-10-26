import random
from datetime import datetime
from werkzeug.security import generate_password_hash
from database.db import get_db, init_db

# Ensure tables exist
init_db()

# Lists of realistic Indian first and last names across regions
first_names = [
    "Aarav", "Ananya", "Rohan", "Priya", "Vikram", "Sneha", "Aditya", "Neha",
    "Rahul", "Pooja", "Kiran", "Divya", "Arjun", "Kavita", "Siddharth", "Meera",
    "Amit", "Sunita", "Manish", "Deepika", "Karthik", "Swati", "Nikhil", "Preeti"
]

last_names = [
    "Sharma", "Patel", "Verma", "Reddy", "Gupta", "Iyer", "Nair", "Singh",
    "Kumar", "Mehta", "Joshi", "Choudhury", "Bose", "Deshmukh", "Pillai", "Das"
]

db = get_db()
cursor = db.cursor()

while True:
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    
    # Generate email with random 2-3 digit number suffix
    suffix = random.randint(10, 999)
    email = f"{first.lower()}.{last.lower()}{suffix}@gmail.com"
    
    # Check if email exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    existing = cursor.fetchone()
    if not existing:
        break

password = "password123"
password_hash = generate_password_hash(password)
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Insert user
cursor.execute(
    "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
    (name, email, password_hash, created_at)
)
db.commit()

user_id = cursor.lastrowid

# Print confirmation
print(f"ID: {user_id}")
print(f"Name: {name}")
print(f"Email: {email}")

db.close()
