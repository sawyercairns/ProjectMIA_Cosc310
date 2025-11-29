# Processes for returns includes checking for order, time frame, refund status, marking an order as returned.

import os
from datetime import datetime, timedelta
from app.services.orderInteractor import load_orders, save_orders

# Configuration constants
RETURN_WINDOW_DAYS = 30


def check_if_order_exists(userid:str, orderid:int):
    # Deprecated: use check_if_order_exists_in_orders instead
    raise NotImplementedError("Use check_if_order_exists_in_orders with orders param")

def check_if_order_exists_in_orders(orders, orderid:int):
    for order in orders:
        if order.order_id == orderid:
            return order
    return None
def check_time_return_window(orderdate:str) -> bool:
    ordertime = datetime.fromisoformat(orderdate)
    return ((datetime.now() - ordertime) <= timedelta(days=RETURN_WINDOW_DAYS))


def not_refunded(order) -> bool:
    return not order.returned


'''
# PLACEHOLDER for how we're gonna simulate returns
def make_payment_refund():

    return True
'''
                 
def update_refund_status(userid:str, orders, orderid: int):
    for order in orders:
         if order.order_id == orderid:  
            order.returned = True
            break
    save_orders(userid, orders)




# Actually processing a return using the above methods
def process_return(userid:str, orderid:int):
    orders = load_orders(userid)
    order = check_if_order_exists_in_orders(orders, orderid)
    if not order:
        print("Order not found.")
        return False
    
    if order.is_gift:
        print("Gift orders are non-refundable.")
        return False


    if not check_time_return_window(order.order_date):
        print(f"Order exceeds {RETURN_WINDOW_DAYS} day return window")
        return False
   
    if not not_refunded(order):
        print("Order has already been returned.")
        return False
   
    # We'd now use the make_payment_refund to refund the payment to the client
    # Empty placeholder for now for payment

    update_refund_status(userid, orders, orderid)
    print("Order refunded successfully.")
    return True



