import sys
from datetime import datetime, timedelta
import random
from database.db import get_db, DATABASE

def main():
    args = sys.argv[1:]
    if len(args) != 3:
        print("Usage: /seed-expenses <user-id> <count> <months>")
        print("Example: /seed-expenses 1 50 6")
        sys.exit(1)

    try:
        user_id = int(args[0])
        count = int(args[1])
        months = int(args[2])
    except ValueError:
        print("Usage: /seed-expenses <user-id> <count> <months>")
        print("Example: /seed-expenses 1 50 6")
        sys.exit(1)

    db = get_db()
    cursor = db.cursor()

    # Step 2 - Verify user exists
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        print(f"No user found with id {user_id}")
        db.close()
        sys.exit(1)

    # Step 3 - Generate and insert expenses
    # Categories with ranges (min, max, weight) and realistic Indian descriptions
    categories_config = {
        "Food": {
            "range": (50, 800),
            "weight": 35,
            "descriptions": [
                "Swiggy food delivery", "Zomato dinner order", "Local restaurant lunch",
                "Chai and snacks", "Grocery store essentials", "Cafe coffee with friends",
                "South Indian breakfast", "Street food evening snack"
            ]
        },
        "Transport": {
            "range": (200, 3000),
            "weight": 20,
            "descriptions": [
                "Ola cab ride", "Uber commute", "Metro card recharge",
                "Petrol refill", "Auto rickshaw fare", "Local train pass"
            ]
        },
        "Bills": {
            "range": (200, 3000),
            "weight": 15,
            "descriptions": [
                "Electricity bill payment", "Broadband internet bill", "Mobile postpaid bill",
                "LPG gas cylinder booking", "Water utility bill", "Municipal corporation tax"
            ]
        },
        "Shopping": {
            "range": (200, 5000),
            "weight": 15,
            "descriptions": [
                "Amazon online shopping", "Flipkart festival sale", "Myntra clothing purchase",
                "Supermarket grocery run", "Local apparel store", "Footwear purchase"
            ]
        },
        "Entertainment": {
            "range": (100, 1500),
            "weight": 5,
            "descriptions": [
                "Movie tickets at PVR", "Netflix monthly subscription", "Spotify premium plan",
                "Gaming arcade tokens", "Amusement park ticket", "Concert pass"
            ]
        },
        "Health": {
            "range": (100, 2000),
            "weight": 5,
            "descriptions": [
                "Pharmacy medicines purchase", "Doctor consultation fee", "Pathology blood test",
                "Gym membership monthly fee", "Vitamin supplements"
            ]
        },
        "Other": {
            "range": (50, 1000),
            "weight": 5,
            "descriptions": [
                "Charity donation", "Stationery and notebooks", "Gift for a friend",
                "Haircut at salon", "Miscellaneous petty cash"
            ]
        }
    }

    category_names = list(categories_config.keys())
    weights = [cfg["weight"] for cfg in categories_config.values()]

    now = datetime.now()
    start_date = now - timedelta(days=months * 30)

    expenses_to_insert = []
    generated_dates = []

    for _ in range(count):
        category = random.choices(category_names, weights=weights, k=1)[0]
        cfg = categories_config[category]
        amount = round(random.uniform(cfg["range"][0], cfg["range"][1]), 2)
        description = random.choice(cfg["descriptions"])

        # Random datetime between start_date and now
        delta_seconds = int((now - start_date).total_seconds())
        random_seconds = random.randint(0, max(0, delta_seconds))
        expense_date = start_date + timedelta(seconds=random_seconds)
        date_str = expense_date.strftime("%Y-%m-%d")
        
        generated_dates.append(expense_date)
        expenses_to_insert.append((user_id, amount, category, date_str, description))

    try:
        with db:
            cursor.executemany(
                """
                INSERT INTO expenses (user_id, amount, category, date, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                expenses_to_insert
            )
        
        # Step 4 - Confirm
        min_date = min(generated_dates).strftime("%Y-%m-%d")
        max_date = max(generated_dates).strftime("%Y-%m-%d")

        print(f"Successfully inserted {count} expenses.")
        print(f"Date range: {min_date} to {max_date}")
        print("\nSample of 5 inserted records:")

        cursor.execute(
            """
            SELECT id, user_id, amount, category, date, description, created_at 
            FROM expenses 
            WHERE user_id = ? 
            ORDER BY id DESC 
            LIMIT 5
            """,
            (user_id,)
        )
        samples = cursor.fetchall()
        for row in reversed(samples):
            print(f"  - ID: {row['id']}, Date: {row['date']}, Category: {row['category']}, Amount: Rs.{row['amount']:.2f}, Desc: {row['description']}")

    except Exception as e:
        print(f"Error inserting expenses, rolling back: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
