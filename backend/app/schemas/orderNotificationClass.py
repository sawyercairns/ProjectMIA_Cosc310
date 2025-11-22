from app.schemas.notificationClass import Notification


class OrderNotification(Notification):
    
    def __init__(self,
                 notification_id: int,
                 user_id: int,
                 order_id: int,
                 total_price: float,
                 item_count: int,
                 created_at: str = None):
        super().__init__(notification_id, user_id, "order_complete", created_at)
        self._order_id = order_id
        self._total_price = total_price
        self._item_count = item_count
    
    @property
    def order_id(self):
        return self._order_id
    
    @property
    def total_price(self):
        return self._total_price
    
    @property
    def item_count(self):
        return self._item_count
    
    def get_message(self) -> str:
        item_text = "item" if self._item_count == 1 else "items"
        return f"Order #{self._order_id} confirmed! {self._item_count} {item_text} totaling ${self._total_price:.2f}. Thank you for your purchase!"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "order_id": self._order_id,
            "total_price": self._total_price,
            "item_count": self._item_count
        })
        return data
