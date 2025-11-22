import json
import os
from pathlib import Path

from app.schemas.reviewClass import Review
from app.services.Interactor import create_item, remove_item

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
    remove_item("reviews.json", "review_id", id)

def get_reviews(user_id: int = None, product_id: int = None):
    path = Path(__file__).resolve().parents[1] / "data" / "reviews.json"
    review_list = list()
    with path.open("r", encoding="UTF-8") as f:
        reviews = json.load(f)
        for review in reviews:
            if int(review["user_id"]) == user_id:
                review_list.append(review)                      
    return review_list

def update_review(user_id: int, product_id: int, rating: float = None, title: str = None, body: str = None):
    path = Path(__file__).resolve().parents[1] / "data" / "reviews.json"
    with path.open("r", encoding="UTF-8") as f:
        reviews = json.load(f)

    review_found = False
    for review in reviews:
        if int(review["user_id"]) == user_id and int(review["product_id"]) == product_id:
            if rating is not None:
                review["rating"] = rating
            if title is not None:
                review["title"] = title
            if body is not None:
                review["body"] = body
            review_found = True
            break
    
    if not review_found:
        raise ValueError("Review not found.")
    
    with path.open("w", encoding="UTF-8") as f:
        json.dump(reviews, f, indent=2)