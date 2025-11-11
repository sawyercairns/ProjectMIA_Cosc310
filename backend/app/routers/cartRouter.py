from fastapi import APIRouter, HTTPException
from backend.app.services.cartInteractor import load_cart, add_item
from backend.app.schemas.orderItemClass import OrderItem
from pydantic import BaseModel
from decimal import Decimal


router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("", response_model=dict)
def get_user_cart(user_id: str):
    
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

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


@router.post("/add-item", response_model=dict)
def add_item_endpoint(request: AddItemRequest):
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


