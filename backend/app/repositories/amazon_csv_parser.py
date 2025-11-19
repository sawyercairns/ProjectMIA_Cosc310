import csv
import json
import os
import re
from pathlib import Path
from datetime import datetime

try:
    from backend.app.schemas.productClass import Product
    from backend.app.schemas.userClass import User
    from backend.app.schemas.reviewClass import Review
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from app.schemas.productClass import Product
    from app.schemas.userClass import User
    from app.schemas.reviewClass import Review

_NUM_RX = re.compile(r"[^\d.\-]")

def _num(s: str | None) -> float:
    """Extract numeric value from string, stripping currency symbols."""
    if not s:
        return 0.0
    s = _NUM_RX.sub("", s).strip()
    return float(s) if s else 0.0

def _inr_to_cad(inr_price: float) -> float:
    """Convert INR to CAD using fixed exchange rate."""
    exchange_rate = 0.016 
    return round(inr_price * exchange_rate, 2)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def parse_amazon_csv() -> tuple[list[Product], list[User], list[Review]]:
    """
    Parse products, users, and reviews from amazon.csv.
    """
    source_path = DATA_DIR / "amazon.csv"
    
    products: list[Product] = []
    users: list[User] = []
    reviews: list[Review] = []
    
    user_id_map: dict[str, int] = {}
    product_name_map: dict[str, int] = {}
    
    next_user_id = 101
    next_product_id = 1
    next_review_id = 1
    
    with source_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # parse product for this row
            product_name = (row.get("product_name") or "").strip()
            if product_name and product_name not in product_name_map:
                product_name_map[product_name] = next_product_id
                p = Product(
                    product_id=next_product_id,
                    product_name=product_name,
                    product_desc=(row.get("about_product") or "").strip(),
                    price=_inr_to_cad(_num(row.get("actual_price"))),
                    discount_price=_inr_to_cad(_num(row.get("discounted_price"))),
                    discount_percent=_num(row.get("discount_percentage")),
                )
                products.append(p)
                next_product_id += 1
            
            # split up CSV fields for parsing
            user_ids_csv = (row.get("user_id") or "").split(",")
            user_names_csv = (row.get("user_name") or "").split(",")
            review_titles_csv = (row.get("review_title") or "").split(",")
            review_contents_csv = (row.get("review_content") or "").split(",")
            

            product_rating = _num(row.get("rating"))
            
            num_reviews = len(user_ids_csv)
            
            for i in range(num_reviews):
                original_user_id = user_ids_csv[i].strip() if i < len(user_ids_csv) else ""
                user_name = user_names_csv[i].strip() if i < len(user_names_csv) else "User"
                review_title = review_titles_csv[i].strip() if i < len(review_titles_csv) else ""
                review_content = review_contents_csv[i].strip() if i < len(review_contents_csv) else ""
                
                if not original_user_id:
                    continue

                # create new users if they don't exist
                if original_user_id not in user_id_map:
                    user_id_map[original_user_id] = next_user_id
                    email_number = next_user_id - 100  
                    u = User(
                        user_id=next_user_id,
                        user_password="test",
                        email=f"test{email_number}@test.com",
                        first_name=user_name
                    )
                    users.append(u)
                    next_user_id += 1
                
                # parse product reviews
                if product_name in product_name_map:
                    r = Review(
                        review_id=next_review_id,
                        user_id=user_id_map[original_user_id],
                        product_id=product_name_map[product_name],
                        created_at=datetime.now().date(),
                        rating=product_rating, 
                        likes=0,
                        title=review_title,
                        body=review_content,
                    )
                    reviews.append(r)
                    next_review_id += 1
    
    return products, users, reviews

def save_products_json(products: list[Product]) -> None:
    """Save a list of products to backend/app/data/products.json"""
    target_path = DATA_DIR / "products.json"
    tmp_path = target_path.with_suffix(".tmp")
    
    products_data = [
        {
            "product_id": str(p.product_id),
            "product_name": p.product_name,
            "product_desc": p.product_desc,
            "price": p._price,                    
            "discount_price": p._discount_price,  
            "discount_percent": p._discount_percent,
            "rating": p._rating,                  
            "rating_count": p._rating_count,
            "units_sold": p._units_sold,
        }
        for p in products
    ]
    
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(products_data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, target_path)

def save_users_json(users: list[User]) -> None:
    """Atomic write to users.json following repository pattern."""
    target_path = DATA_DIR / "users.json"
    tmp_path = target_path.with_suffix(".tmp")
    
    users_data = [
        {
            "user_id": str(u.user_id),
            "user_password": u.user_password,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "age": u.age,
        }
        for u in users
    ]
    
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, target_path)

def save_reviews_json(reviews: list[Review]) -> None:
    """Atomic write to reviews.json following repository pattern."""
    target_path = DATA_DIR / "reviews.json"
    tmp_path = target_path.with_suffix(".tmp")
    
    reviews_data = [
        {
            "review_id": str(r.review_id),
            "product_id": str(r.product_id),
            "user_id": str(r.user_id),
            "rating": r.rating,
            "title": r.title,
            "body": r.body,
            "likes": r.likes,
            "created_at": r.created_at.isoformat(),
        }
        for r in reviews
    ]
    
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(reviews_data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, target_path)

if __name__ == "__main__":
    print("Parsing amazon.csv into JSON files")
    
    products, users, reviews = parse_amazon_csv()
    
    save_products_json(products)
    print(f"✓ Saved {len(products)} products → products.json")
    
    save_users_json(users)
    print(f"✓ Saved {len(users)} users → users.json")
    
    save_reviews_json(reviews)
    print(f"✓ Saved {len(reviews)} reviews → reviews.json")