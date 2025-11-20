# Loading and saving return status to pastOrders.json

import json
import os
from pathlib import Path
orders_path = Path(__file__).resolve().parents[1] / "data" / "pastOrders.json"

def get_orders(user_id:str):
    if not os.path.exists(orders_path):
        return []
    
    with open(orders_path, "r") as f:
        data = json.load(f)

    return data.get(user_id, [])

def save_orders(user_id:str, orders:list):
    if os.path.exists(orders_path):
        with open(orders_path, "r") as f:
            try:
                data = json.load(f)
            except:
                data = {}
    else:
        data={}
    data[user_id] = orders

    with open(orders_path, "w") as f:
        json.dump(data, f, indent=2)