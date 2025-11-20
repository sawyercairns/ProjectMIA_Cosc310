# Processes for returns includes checking for order, time frame, refund status, marking an order as returned.

import os
from datetime import datetime, timedelta
from backend.app.services.pastOrdersInteractor import save_orders, get_orders


def check_if_order_exists(userid:str, orderid:int):
    orders = get_orders(userid)
    for order in orders:
        if order["order_id"] == orderid:
            return order
    return None

def check_time_return_window(orderdate:str) -> bool:
    ordertime = datetime.fromisoformat(orderdate)
    return ((datetime.now() - ordertime) <= timedelta(days=30))

def not_refunded(order:dict) -> bool:
    return not order.get("returned", False)

'''
# PLACEHOLDER for how we're gonna simulate returns
def make_payment_refund():

    return True
'''
                 
def update_refund_status(userid:str, orderid: int):
    orders = get_orders(userid)
    for order in orders:
        if order["order_id"] == orderid:
            order["returned"] = True
            break
    save_orders(userid, orders)




# Actually processing a return using the above methods
def process_return(userid:str, orderid:int):
    order = check_if_order_exists(userid, orderid)
    if not order:
        print("Order not found.")
        return False

    if not check_time_return_window(order["date"]):
        print("Order exceeds 30 day return window")
        return False
    
    if not not_refunded(order):
        print("Order has already been returned.")
        return False
    
    # We'd now use the make_payment_refund to refund the payment to the client
    # Empty placeholder for now for payment

    update_refund_status(userid, orderid)
    print("Order refunded successfully.")
    return True



