from fastapi import APIRouter
from backend.app.services.returnOrders import process_return

router = APIRouter(prefix="/returns")

@router.post("/{user_id}/{order_id}")
def return_order(userid:str, orderid:int):
    return process_return(userid, orderid)