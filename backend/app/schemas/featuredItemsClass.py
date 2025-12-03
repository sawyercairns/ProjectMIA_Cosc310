from pydantic import BaseModel
from typing import List


class FeaturedItems:
    """
    FeaturedItems class to store and manage the list of featured product IDs
    """
    def __init__(self, featured_product_ids: List[str] = None):
        self._featured_product_ids = featured_product_ids if featured_product_ids is not None else []

    @property
    def featured_product_ids(self):
        return self._featured_product_ids
    
    @featured_product_ids.setter
    def featured_product_ids(self, ids: List[str]):
        self._featured_product_ids = ids

    def to_dict(self):
        return {
            "featured_product_ids": self._featured_product_ids
        }


class AddFeaturedItemRequest(BaseModel):
    product_id: str
    admin_email: str


class RemoveFeaturedItemRequest(BaseModel):
    product_id: str
    admin_email: str
