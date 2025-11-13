import json
import os
from backend.app.schemas.wishListClass import WishList, WishListEntry
from pathlib import Path
from datetime import date

"""
This file is the functions that the user can interact with.

"""

path = Path(__file__).resolve().parents[1] / "data" / "wishlist.json"

def load_wishList(user_id: str) -> WishList:
    if not os.path.exists(path):
        raise FileNotFoundError("wishlist.json file not found")

    with open(path, "r") as f:
        data = json.load(f)

    user_wishList = data.get(user_id)

    if not user_wishList:
        empty_wishList = WishList(user_id = user_id, entries = [])
        _save_wishList(empty_wishList)
        return empty_wishList

    items = [
        WishListEntry(
            product_id = item["product_id"],
            date_added = date.fromisoformat(item["date_added"])
        )
        for item in user_wishList.get("entries", [])
    ]

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

    temp_path = Path(str(path) + ".tmp")
    with open(temp_path, "w") as f:
        json.dump(data, f, indent=4)

    os.replace(temp_path, path)


def add_entry(user_id: str, product_id: int):
    wishList = load_wishList(user_id)
    entry = WishListEntry(product_id = product_id, date_added = date.today())
    wishList.add_entry(entry)
    _save_wishList(wishList)
    return wishList.to_dict()

def remove_entry(user_id: str, product_id: int):
    wishList = load_wishList(user_id)
    wishList.remove_entry(product_id)
    _save_wishList(wishList)
    return wishList.to_dict()


