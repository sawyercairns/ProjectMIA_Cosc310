
from backend.app.schemas.productClass import Product
from datetime import date
from typing import List, Optional

class WishListEntry:
    def __init__(self, product_id: int, date_added: date):
        self._product_id = product_id
        self._date_added = date_added

    @property
    def product_id(self):
        return self._product_id

    @property
    def date_added(self):
        return self._date_added

    def to_dict(self):
        return {
            "product_id": self._product_id,
            "date_added": self._date_added.isoformat()
        }
        
class WishList:
    def __init__(self, user_id: str, entries: Optional[List[WishListEntry]] = None):
        self._user_id = user_id
        self._entries = entries or []

    @property
    def user_id(self):
        return self._user_id
    @property
    def entries(self):
        return self._entries

    def add_entry(self, entry: WishListEntry):
        if not any(e.product_id == entry.product_id for e in self._entries):
            self._entries.append(entry)

    def remove_entry(self, product_id: int):
        self._entries = [e for e in self._entries if e.product_id != product_id]


    def to_dict(self):
        return {
            "entries": [entry.to_dict() for entry in self._entries]
        }