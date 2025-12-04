import json
import os
from pathlib import Path
from typing import Optional

from app.schemas.reviewClass import Review
from app.services.Interactor import create_item, remove_item, load_json, write_to_json

def has_reviewed(user_id: int, product_id: int) -> bool:
    path = Path(__file__).resolve().parents[1] / "data" / "reviews.json"
    with path.open("r", encoding="UTF-8") as f:
        reviews = json.load(f)
        for review in reviews:
            if int(review["user_id"]) == user_id and int(review["product_id"]) == product_id:
                return True
    return False

def create_review(r:Review):
    # Check if user has reviewed the product already
    if has_reviewed(r.user_id, r.product_id):
        raise ValueError("User has already reviewed this product. Please update existing review instead.")
    
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

def get_all_reviews():
    return load_json("reviews.json")

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
    reviews = load_json("reviews.json")

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

    write_to_json("reviews.json", reviews)


def get_review_by_id(review_id: int) -> Optional[dict]:
    reviews = load_json("reviews.json")
    for review in reviews:
        if int(review.get("review_id", -1)) == review_id:
            return review
    return None


def update_review_by_id(
    review_id: int,
    acting_user_id: int,
    acting_user_is_admin: bool,
    rating: Optional[float] = None,
    title: Optional[str] = None,
    body: Optional[str] = None,
):
    reviews = load_json("reviews.json")

    target_review = None
    for review in reviews:
        if int(review.get("review_id", -1)) == review_id:
            target_review = review
            break

    if target_review is None:
        raise ValueError("Review not found.")

    if not acting_user_is_admin and acting_user_id != int(target_review.get("user_id")):
        raise PermissionError("Not authorized to update this review.")

    if rating is not None:
        target_review["rating"] = rating
    if title is not None:
        target_review["title"] = title
    if body is not None:
        target_review["body"] = body

    write_to_json("reviews.json", reviews)

    return target_review