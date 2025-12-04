from fastapi import APIRouter
from app.services.returnOrders import process_return

router = APIRouter(prefix="/returns")

@router.post("/{user_id}/{order_id}")
def return_order(user_id: str, order_id: int):
    return process_return(user_id, order_id)