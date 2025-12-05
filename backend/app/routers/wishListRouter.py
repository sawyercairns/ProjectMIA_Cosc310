from fastapi import APIRouter, HTTPException
from app.services.wishListInteractor import load_wishList, add_entry, remove_entry
from app.services.notificationInteractor import create_notification, _get_next_notification_id
from app.services.productInteractor import get_product
from app.schemas.wishlistAddedNotificationClass import WishlistAddedNotification
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
        
        # Create notification for wishlist item added
        product = get_product(request.product_id)
        if product:
            notification_id = _get_next_notification_id(request.user_id)
            notification = WishlistAddedNotification(
                notification_id=notification_id,
                user_id=int(request.user_id),
                product_id=request.product_id,
                product_name=product.get("product_name", "Unknown Product"),
                price=product.get("actual_price", 0.0)
            )
            create_notification(request.user_id, notification)
        
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