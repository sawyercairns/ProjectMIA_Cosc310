from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.reviewClass import Review
from app.services import reviewInteractor
from app.services.userInteractor import get_user, find_user_by_id
from app.services.Interactor import load_json

# inside helper method
def _resolve_actor(user_id: Optional[int], email: Optional[str], password: Optional[str]) -> tuple[int, bool]:
    """Return (user_id, is_admin) for the acting user."""
    if email and password:
        user = get_user(email, password)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user.user_id, user.is_admin

    if user_id is not None:
        users = load_json("users.json")
        try:
            record = find_user_by_id(users, str(user_id))
        except ValueError:
            raise HTTPException(status_code=404, detail="User not found")
        return int(record["user_id"]), bool(record.get("is_admin", False))

    raise HTTPException(status_code=401, detail="Authentication required")

router = APIRouter(prefix="/reviews", tags=["reviews"])


class UpdateReviewRequest(BaseModel):
    rating: Optional[float] = None
    title: Optional[str] = None
    body: Optional[str] = None

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
def delete_review(review_id: str, email: str, password: str):
    user = get_user(email, password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    review_to_remove = None
    if not user.is_admin:
        for review in get_reviews(user.user_id):
            if str(review["review_id"]) == str(review_id):
                review_to_remove = review
                break
        if review_to_remove is None:
            raise HTTPException(status_code=403, detail="Not authorized to delete this review")

    review = review_to_remove
    if user.is_admin and review_to_remove is None:
        review = next((rev for rev in reviewInteractor.get_all_reviews() if str(rev["review_id"]) == str(review_id)), None)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    reviewInteractor.remove_review(int(review_id))
    return {"message": "Review deleted successfully"}


@router.put("/{review_id}")
def update_review(
    review_id: str,
    request: UpdateReviewRequest,
    user_id: Optional[int] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
):
    acting_user_id, acting_user_is_admin = _resolve_actor(user_id, email, password)

    try:
        reviewInteractor.update_review_by_id(
            int(review_id),
            acting_user_id,
            acting_user_is_admin,
            request.rating,
            request.title,
            request.body,
        )
        return {"message": "Review updated successfully"}
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    except ValueError as exc:
        detail = str(exc)
        status = 404 if "not found" in detail.lower() else 400
        raise HTTPException(status_code=status, detail=detail)

