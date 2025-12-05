from app.schemas.notificationClass import Notification


class WishlistAddedNotification(Notification):
    """Notification for when an item is added to user's wishlist."""
    
    def __init__(self,
                 notification_id: int,
                 user_id: int,
                 product_id: int,
                 product_name: str,
                 price: float,
                 created_at: str = None):
        super().__init__(notification_id, user_id, "wishlist_added", created_at)
        self._product_id = product_id
        self._product_name = product_name
        self._price = price
    
    @property
    def product_id(self):
        return self._product_id
    
    @property
    def product_name(self):
        return self._product_name
    
    @property
    def price(self):
        return self._price
    
    def get_message(self) -> str:
        return f"'{self._product_name}' has been added to your wishlist! Current price: ${self._price:.2f}"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "product_id": self._product_id,
            "product_name": self._product_name,
            "price": self._price
        })
        return data
