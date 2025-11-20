# Loading and saving return status to pastOrders.json

import json
import os
from pathlib import Path
from backend.app.services.Interactor import load_json, write_to_json
orders_path = Path(__file__).resolve().parents[1] / "data" / "pastOrders.json"

def get_orders(user_id:str):
    if not os.path.exists(orders_path):
        return []
    
    data = load_json(orders_path.name)

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

    write_to_json(orders_path.name, data)