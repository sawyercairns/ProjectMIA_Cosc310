# Test file for returnOrders.py
import json
from datetime import datetime, timedelta
import os
import pytest

from app.services import returnOrders
from app.services import pastOrdersInteractor
from app.services.returnOrders import process_return

def test_return():
    user_id = "pytest_user"
    temp_order_id = 9999999

    path = pastOrdersInteractor.orders_path
    with open(path, "r") as f:
        data = json.load(f)

    original = data.get(user_id, [])

# Add a temporary fake order for testing purposes.
    temp_order = {
        "order_id":temp_order_id,
        "date": (datetime.now() - timedelta(days=8)).isoformat(),
        "returned": False,
        "payment_method": "vise",
        "items": [],
        "total": "0.00"
    }

    data[user_id] = original + [temp_order]

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Test result for returnOrder.py
    result = process_return(user_id, temp_order_id)
    assert result is True

    updated = pastOrdersInteractor.get_orders(user_id)
    assert updated[-1]["returned"] is True

# Remove temporary fake order
    restored = [ o for o in updated if o["order_id"] != temp_order_id]
    data[user_id] = restored

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
     