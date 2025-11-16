import json
import os
from pathlib import Path

from backend.app.schemas.reviewClass import Review
from backend.app.services.Interactor import create_item

def create_review(r:Review):
    item = {
            "review_id": r.review_id,
            "user_id": r.user_id,
            "product_id": r.product_id,
            "created_at": str(r.created_at),
            "rating": r.rating,
            "likes": r.likes,
            "title": r.title,
            "body": r.body
        }
    create_item("reviews.json", "review_id", item)

def remove_review(id:int):
    path = Path(__file__).resolve().parents[1] / "data" / "reviews.json"
    tmp_path = path.with_suffix(".tmp")
    with path.open("r", encoding="UTF-8") as f:
        reviews = json.load(f)
        for r in reviews:
            if int(r["review_id"]) == id:
                reviews.remove(r)
        f.close()
    with tmp_path.open("w", encoding="UTF-8") as t:
        json.dump(reviews, t, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)

def get_reviews(user_id: int):
    path = Path(__file__).resolve().parents[1] / "data" / "reviews.json"
    review_list = list()
    with path.open("r", encoding="UTF-8") as f:
        reviews = json.load(f)
        for review in reviews:
            if int(review["user_id"]) == user_id:
                review_list.append(review)                      
    return review_list