from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel

from app.schemas.reviewClass import Review
from app.services import reviewInteractor
from app.services.userInteractor import get_user

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/all", response_model=None)
def get_all_reviews():
    return reviewInteractor.get_all_reviews()

@router.get("/{user_id}", response_model=None)
def get_reviews(user_id:int):
    return reviewInteractor.get_reviews(user_id)


@router.post("")
def add_review(user_id:str, product_id:str, rating:float, title:str, body:str):
    rev = Review(0, user_id, product_id, date.today(), rating, 0, title, body)
    reviewInteractor.create_review(rev)
    return "REVIEW CREATED"

@router.delete("/{review_id}")
def delete_review(review_id:str, email:str, password:str):
    u = get_user(email, password)
    if u is not None and not u.is_admin:
        for review in get_reviews(u.user_id):
            if review["review_id"] == review_id:
                r = review
    if u.is_admin or (r is not None and r["user_id"] == u.user_id):
        reviewInteractor.remove_review(int(review_id))

