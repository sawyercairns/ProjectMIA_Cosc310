import json
import os
from app.schemas.wishListClass import WishList, WishListEntry
from pathlib import Path
from datetime import date
from app.services.Interactor import load_json, write_to_json
from datetime import datetime

"""
This file is the functions that the user can interact with.

"""

# Configuration constants
MAX_WISHLIST_ENTRIES = 10

path = Path(__file__).resolve().parents[1] / "data" / "wishlist.json"

def load_wishList(user_id: str) -> WishList:
    
    data = load_json(path.name)

    user_wishList = data.get(user_id)

    if not user_wishList:
        empty_wishList = WishList(user_id = user_id, entries = [])
        _save_wishList(empty_wishList)
        return empty_wishList

    items = []
    for item in user_wishList.get("entries", []):
        date_value = item.get("date_added") or item.get("added_at")
        if date_value is None:
            raise ValueError("Wishlist entry missing date information")
        if isinstance(date_value, date):
            parsed_date = date_value
        else:
            try:
                parsed_date = date.fromisoformat(date_value)
            except ValueError:
                parsed_date = datetime.fromisoformat(date_value).date()
        items.append(
            WishListEntry(
                product_id = item["product_id"],
                date_added = parsed_date
            )
        )

    return WishList(user_id = user_id, entries = items)


def _save_wishList(wishList: WishList):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    user_id = str(wishList._user_id)
    data[user_id] = wishList.to_dict()

    write_to_json(path.name, data)


def add_entry(user_id: str, product_id: int):
    wishList = load_wishList(user_id)
    entries_count = len(wishList.entries)

    if entries_count >= MAX_WISHLIST_ENTRIES:
        raise ValueError(f"Wishlist limit exceeded. Maximum {MAX_WISHLIST_ENTRIES} entries allowed.")

    entry = WishListEntry(product_id = product_id, date_added = date.today())
    wishList.add_entry(entry)
    _save_wishList(wishList)
    return wishList.to_dict()

def remove_entry(user_id: str, product_id: int):
    wishList = load_wishList(user_id)
    wishList.remove_entry(product_id)
    _save_wishList(wishList)
    return wishList.to_dict()


