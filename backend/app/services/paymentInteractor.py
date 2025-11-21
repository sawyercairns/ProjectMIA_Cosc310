import json
import os
from app.schemas.paymentClass import Payment
from pathlib import Path
from datetime import date
from app.services.Interactor import load_json, write_to_json

"""
This file is the functions that the user can interact with.

"""

path = Path(__file__).resolve().parents[1] / "data" / "payment.json"

def load_payment(user_id: str) -> Payment:
    if not os.path.exists(path):
        raise FileNotFoundError("payment.json file not found")
    
    data = load_json(path.name)

    user_payment = data.get(user_id)

    if user_payment:
        return Payment(
            user_id = user_id,
            card_number = user_payment["card_number"],
            CVV = user_payment["CVV"],
            expiration_date = user_payment["expiration_date"]
        )
    else:
        return Payment(
            user_id = user_id,
            card_number = "",
            CVV = "",
            expiration_date = "MM/YY"
        )


def _save_payment(payment: Payment):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    user_id = payment.user_id
    data[user_id] = {
        "card_number": payment.card_number,
        "CVV": payment.CVV,
        "expiration_date": payment.expiration_date
    }

    write_to_json(path.name, data)


def update_payment(user_id: str, card_number: str, CVV: str, expiration_date: date):
    """Update a user's payment info (all fields required)."""
    user_payment = load_payment(user_id)
    user_payment.update_payment_info(card_number, CVV, expiration_date)
    _save_payment(user_payment)
    return user_payment.to_dict()


