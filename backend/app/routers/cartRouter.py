from fastapi import APIRouter, HTTPException
from app.services.cartInteractor import load_cart, add_item, delete_item
from app.schemas.orderItemClass import OrderItem
from pydantic import BaseModel
from decimal import Decimal


router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("", response_model=dict)
def get_user_cart(user_id: str):

    try:
        cart = load_cart(user_id)
        return cart.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class AddItemRequest(BaseModel):
    user_id: str
    product_id: int
    product_name: str
    product_desc: str
    price: Decimal
    quantity: int


@router.post("/cart/items", response_model=dict)
def add_item_endpoint(request: AddItemRequest):
    try:
        order_item = OrderItem(
            product_id = request.product_id,
            product_name = request.product_name,
            product_desc = request.product_desc,
            quantity = request.quantity,
            price = request.price
        )
        add_item(request.user_id, order_item)
        cart = load_cart(request.user_id)
        return cart.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/items", response_model=dict)
def delete_item_endpoint(user_id: str, product_id: str):
    try:
        cart = delete_item(user_id, product_id)
        return cart
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



