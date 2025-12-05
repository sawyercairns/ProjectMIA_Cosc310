from fastapi import APIRouter, HTTPException
from app.services.orderInteractor import load_orders, add_order, get_order_by_id
from app.schemas.orderClass import Order
from app.schemas.orderItemClass import OrderItem
from app.schemas.addressClass import Address
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
import random
from app.services.userInteractor import get_eligible_gift_recipients


router = APIRouter(prefix="/orders", tags=["Orders"])


class OrderItemRequest(BaseModel):
    product_id: int
    product_name: str
    product_desc: str
    quantity: int
    price: Decimal


class AddressRequest(BaseModel):
    line1: str
    line2: Optional[str] = ""
    city: str
    province: str
    country: str


class CreateOrderRequest(BaseModel):
    user_id: int
    order_items: List[OrderItemRequest]
    address: Optional[AddressRequest] = None


@router.get("", response_model=dict)
def get_user_orders(user_id: str):
    """
    Get all orders for a specific user.
    """
    try:
        orders = load_orders(user_id)
        return {
            "user_id": user_id,
            "orders": [order.to_dict() for order in orders],
            "total_orders": len(orders)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}", response_model=dict)
def get_order(order_id: int, user_id: Optional[str] = None):
    """
    Get a specific order by order_id.
    If user_id is provided, searches only that user's orders (faster).
    If user_id is not provided, searches all users (admin use case).
    """
    try:
        order = get_order_by_id(order_id=order_id, user_id=user_id)
        
        if order is None:
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
        
        return order.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=dict)
def create_order(request: CreateOrderRequest):
    """
    Create a new order. Order ID is automatically assigned.
    """
    try:

        items = [
            OrderItem(
                product_id=item.product_id,
                product_name=item.product_name,
                product_desc=item.product_desc,
                quantity=item.quantity,
                price=item.price
            )
            for item in request.order_items
        ]
        
        address = None
        if request.address:
            address = Address(
                line1=request.address.line1,
                line2=request.address.line2,
                city=request.address.city,
                province=request.address.province,
                country=request.address.country
            )
        
        order = Order(
            user_id=request.user_id,
            order_items=items,
            address=address
        )
        
        result = add_order(user_id=str(request.user_id), order=order)
        
        return {
            "message": "Order created successfully",
            "order": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/gift", response_model=dict)
def create_gift_order(request: CreateOrderRequest):
    """
    Create a new gift order for random user.
    Selects a random non-admin user from the json except for themselves.
    Gift orders and non-refundable.
    Gifter doesnt see recipient details.
    """
    try:
        eligable_users = get_eligible_gift_recipients(str(request.user_id))

        if not eligable_users:
            raise HTTPException(status_code=400, detail="No eligable users to send gift to.")
        
        recipient = random.choice(eligable_users)
        recipient_id = int(recipient["user_id"])

        items = [
            OrderItem(
                product_id=item.product_id,
                product_name=item.product_name,
                product_desc=item.product_desc,
                quantity=item.quantity,
                price=item.price
            )
            for item in request.order_items
        ]
        
        address = None
        if request.address:
            address = Address(
                line1=request.address.line1,
                line2=request.address.line2,
                city=request.address.city,
                province=request.address.province,
                country=request.address.country
            )
        
        order = Order(
            user_id=recipient_id,
            order_items=items,
            address=address,
            is_gift=True,
            gifter_id=request.user_id
        )
        
        result = add_order(user_id=str(recipient_id), order=order)
        
        return {
            "message": "Gift created successfully",
            "order": result["order_id"]

        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
