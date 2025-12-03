import json
import os
from pathlib import Path

data_path = Path(__file__).resolve().parents[1] / "data"

def seed_demo_user():
    demo_user = {
        "user_id": "1",
        "user_password": "demo",
        "email": "demo@example.com",
        "first_name": "Demo",
        "last_name": "User",
        "age": 25,
        "is_admin": False,
        "image_url": ""
    }
    
    users_path = data_path / "users.json"
    with open(users_path, "r") as f:
        users = json.load(f)
    
    users = [u for u in users if u.get("user_id") != "1"]
    users.insert(0, demo_user)
    
    with open(users_path, "w") as f:
        json.dump(users, f, indent=2)
    
    print("Demo user created")


def seed_demo_orders():
    demo_orders = [
        {
            "order_id": 1,
            "user_id": 1,
            "order_items": [
                {"product_id": 1, "product_name": "Wayona Nylon Braided USB Cable", "product_desc": "Lightning cable", "quantity": 2, "price": 17.58},
                {"product_id": 5, "product_name": "Portronics Konnect L Cable", "product_desc": "Fast charging cable", "quantity": 1, "price": 6.38}
            ],
            "address": {"line1": "123 Demo Street", "line2": "Apt 4", "city": "Vancouver", "province": "BC", "country": "Canada"},
            "order_date": "2025-01-15T10:30:00",
            "total_price": "41.54",
            "returned": False,
            "is_gift": False,
            "gifter_id": None
        },
        {
            "order_id": 2,
            "user_id": 1,
            "order_items": [
                {"product_id": 3, "product_name": "Sounce Fast Phone Charging Cable", "product_desc": "iPhone cable", "quantity": 3, "price": 30.38}
            ],
            "address": {"line1": "123 Demo Street", "line2": "Apt 4", "city": "Vancouver", "province": "BC", "country": "Canada"},
            "order_date": "2025-02-20T14:15:00",
            "total_price": "91.14",
            "returned": False,
            "is_gift": False,
            "gifter_id": None
        },
        {
            "order_id": 3,
            "user_id": 1,
            "order_items": [
                {"product_id": 4, "product_name": "boAt Deuce USB 300 Cable", "product_desc": "Type-C cable", "quantity": 1, "price": 11.18},
                {"product_id": 6, "product_name": "pTron Solero TB301 Cable", "product_desc": "Fast charging cable", "quantity": 2, "price": 16.00}
            ],
            "address": {"line1": "123 Demo Street", "line2": "Apt 4", "city": "Vancouver", "province": "BC", "country": "Canada"},
            "order_date": "2025-03-10T09:45:00",
            "total_price": "43.18",
            "returned": True,
            "is_gift": False,
            "gifter_id": None
        },
        {
            "order_id": 4,
            "user_id": 1,
            "order_items": [
                {"product_id": 2, "product_name": "Ambrane Unbreakable 60W Cable", "product_desc": "Braided Type C", "quantity": 4, "price": 5.58}
            ],
            "address": {"line1": "123 Demo Street", "line2": "Apt 4", "city": "Vancouver", "province": "BC", "country": "Canada"},
            "order_date": "2025-05-05T16:20:00",
            "total_price": "22.32",
            "returned": False,
            "is_gift": False,
            "gifter_id": None
        },
        {
            "order_id": 5,
            "user_id": 1,
            "order_items": [
                {"product_id": 1, "product_name": "Wayona Nylon Braided USB Cable", "product_desc": "Lightning cable", "quantity": 5, "price": 17.58},
                {"product_id": 2, "product_name": "Ambrane Unbreakable 60W Cable", "product_desc": "Braided Type C", "quantity": 3, "price": 5.58},
                {"product_id": 3, "product_name": "Sounce Fast Phone Charging Cable", "product_desc": "iPhone cable", "quantity": 2, "price": 30.38}
            ],
            "address": {"line1": "123 Demo Street", "line2": "Apt 4", "city": "Vancouver", "province": "BC", "country": "Canada"},
            "order_date": "2025-07-22T11:00:00",
            "total_price": "165.40",
            "returned": False,
            "is_gift": False,
            "gifter_id": None
        },
        {
            "order_id": 6,
            "user_id": 1,
            "order_items": [
                {"product_id": 4, "product_name": "boAt Deuce USB 300 Cable", "product_desc": "Type-C cable", "quantity": 2, "price": 11.18}
            ],
            "address": {"line1": "123 Demo Street", "line2": "Apt 4", "city": "Vancouver", "province": "BC", "country": "Canada"},
            "order_date": "2025-09-18T13:30:00",
            "total_price": "22.36",
            "returned": False,
            "is_gift": False,
            "gifter_id": None
        },
        {
            "order_id": 7,
            "user_id": 1,
            "order_items": [
                {"product_id": 5, "product_name": "Portronics Konnect L Cable", "product_desc": "Fast charging cable", "quantity": 1, "price": 6.38},
                {"product_id": 6, "product_name": "pTron Solero TB301 Cable", "product_desc": "Fast charging cable", "quantity": 1, "price": 16.00}
            ],
            "address": {"line1": "123 Demo Street", "line2": "Apt 4", "city": "Vancouver", "province": "BC", "country": "Canada"},
            "order_date": "2025-11-08T15:45:00",
            "total_price": "22.38",
            "returned": False,
            "is_gift": False,
            "gifter_id": None
        }
    ]
    
    orders_path = data_path / "orders.json"
    with open(orders_path, "r") as f:
        orders = json.load(f)
    
    orders["1"] = demo_orders
    
    with open(orders_path, "w") as f:
        json.dump(orders, f, indent=2)
    
    print(f"Created {len(demo_orders)} orders for demo user")


def seed_demo_reviews():
    reviews_path = data_path / "reviews.json"
    with open(reviews_path, "r") as f:
        reviews = json.load(f)
    
    max_id = max(int(r.get("review_id", 0)) for r in reviews) if reviews else 0
    next_id = max_id + 1
    
    demo_reviews = [
        {
            "review_id": str(next_id),
            "product_id": "1",
            "user_id": "1",
            "rating": 5.0,
            "title": "Excellent cable!",
            "body": "Best charging cable I've ever used. Fast charging and very durable.",
            "likes": 42,
            "created_at": "2025-01-20"
        },
        {
            "review_id": str(next_id + 1),
            "product_id": "2",
            "user_id": "1",
            "rating": 4.5,
            "title": "Great value",
            "body": "Works perfectly for the price. Highly recommend.",
            "likes": 28,
            "created_at": "2025-03-15"
        },
        {
            "review_id": str(next_id + 2),
            "product_id": "3",
            "user_id": "1",
            "rating": 3.5,
            "title": "Decent but could be better",
            "body": "Does the job but the cable is a bit stiff.",
            "likes": 15,
            "created_at": "2025-05-10"
        },
        {
            "review_id": str(next_id + 3),
            "product_id": "4",
            "user_id": "1",
            "rating": 4.0,
            "title": "Good quality",
            "body": "Solid build quality and fast charging speeds.",
            "likes": 33,
            "created_at": "2025-08-25"
        },
        {
            "review_id": str(next_id + 4),
            "product_id": "5",
            "user_id": "1",
            "rating": 5.0,
            "title": "Perfect!",
            "body": "Exactly what I needed. Works flawlessly with my iPhone.",
            "likes": 51,
            "created_at": "2025-11-12"
        }
    ]
    
    reviews = [r for r in reviews if r.get("user_id") != "1"]
    reviews = demo_reviews + reviews
    
    with open(reviews_path, "w") as f:
        json.dump(reviews, f, indent=2)
    
    print(f"Created {len(demo_reviews)} reviews for demo user")


def seed_demo_wishlist():
    demo_wishlist = {
        "entries": [
            {"product_id": 7, "added_at": "2025-06-15T10:00:00"},
            {"product_id": 8, "added_at": "2025-08-20T14:30:00"},
            {"product_id": 10, "added_at": "2025-10-05T09:15:00"}
        ]
    }
    
    wishlist_path = data_path / "wishlist.json"
    with open(wishlist_path, "r") as f:
        wishlist = json.load(f)
    
    wishlist["1"] = demo_wishlist
    
    with open(wishlist_path, "w") as f:
        json.dump(wishlist, f, indent=2)
    
    print(f"Created wishlist with {len(demo_wishlist['entries'])} items for demo user")


def seed_all():
    print("Seeding demo user data...")
    seed_demo_user()
    seed_demo_orders()
    seed_demo_reviews()
    seed_demo_wishlist()
    print("\nDemo user seeding complete!")
    print("\nDemo User Credentials:")
    print("  Email: demo@example.com")
    print("  Password: demo123")
    print("  User ID: 1")


if __name__ == "__main__":
    seed_all()
