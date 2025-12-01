# Test file for returnOrders.py
import json
from datetime import datetime, timedelta
import os
import pytest

from app.services import returnOrders
from app.services.orderInteractor import path, save_orders, load_orders
from app.schemas.orderClass import Order
from app.services.Interactor import write_to_json

def test_return():
    user_id = 99999999
    temp_order_id = 9999999
   
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
    else:
        data = {}
       
    original = data.get(str(user_id), [])

# Add a temporary fake order for testing purposes.
    temp_order = Order(  
        user_id=user_id,  
        order_id=temp_order_id,  
        order_date=(datetime.now() - timedelta(days=8)).isoformat(),  
        returned=False  
    )


    save_orders(str(user_id), original + [temp_order])


    # Restore original data after test
    result = returnOrders.process_return(user_id, temp_order_id)
    assert result is True


    # Check that the order's returned status is now True
    updated_orders = load_orders(str(user_id))
    temp_order_updated = next(o for o in updated_orders if o.order_id == temp_order_id)
    assert temp_order_updated.returned is True


    # Remove the temporary order
    cleaned_orders = [o for o in updated_orders if o.order_id != temp_order_id]
    save_orders(str(user_id), cleaned_orders)

    write_to_json("orders.json", data)
     