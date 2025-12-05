from app.schemas.notificationClass import Notification


class WishlistDiscountNotification(Notification):
    """Notification for when a product in user's wishlist goes on sale."""
    
    def __init__(self,
                 notification_id: int,
                 user_id: int,
                 product_id: int,
                 product_name: str,
                 old_price: float,
                 new_price: float,
                 created_at: str = None):
        super().__init__(notification_id, user_id, "wishlist_discount", created_at)
        self._product_id = product_id
        self._product_name = product_name
        self._old_price = old_price
        self._new_price = new_price
    
    @property
    def product_id(self):
        return self._product_id
    
    @property
    def product_name(self):
        return self._product_name
    
    @property
    def old_price(self):
        return self._old_price
    
    @property
    def new_price(self):
        return self._new_price
    
    @property
    def discount_percent(self):
        if self._old_price > 0:
            return round((1 - self._new_price / self._old_price) * 100)
        return 0
    
    def get_message(self) -> str:
        return f"🎉 '{self._product_name}' is now on sale! Was ${self._old_price:.2f}, now ${self._new_price:.2f} ({self.discount_percent}% off)"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "product_id": self._product_id,
            "product_name": self._product_name,
            "old_price": self._old_price,
            "new_price": self._new_price,
            "discount_percent": self.discount_percent
        })
        return data
