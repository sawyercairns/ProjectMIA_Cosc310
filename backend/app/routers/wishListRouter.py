from fastapi import APIRouter, HTTPException
from backend.app.services.wishListInteractor import load_wishList, add_entry, remove_entry
from pydantic import BaseModel

router = APIRouter(prefix="/wishlist", tags=["WishList"])


@router.get("", response_model = dict)
def get_user_wishlist(user_id: str):
    try:
        wishlist = load_wishList(user_id)
        return wishlist.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AddWishRequest(BaseModel):
    user_id: str
    product_id: int


@router.post("/items", response_model = dict)
def add_wish_item(request: AddWishRequest):
    try:
        wishlist = add_entry(request.user_id, request.product_id)
        return wishlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/users/{user_id}/items/{product_id}", response_model = dict)
def remove_wish_item(user_id: str, product_id: int):
    try:
        wishlist = remove_entry(user_id, product_id)
        return wishlist
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))