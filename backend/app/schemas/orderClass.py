from typing import List
import decimal
from datetime import datetime
from app.schemas.orderItemClass import OrderItem
from app.schemas.addressClass import Address


class Order:
    """
    Order class to represent a customer's order.
    Contains a list of OrderItems and delivery address.
    Order ID is auto-assigned and immutable.
    """
    
    def __init__(self,
                 user_id: int,
                 order_items: List[OrderItem] = None,
                 address: Address = None,
                 order_date: str = None,
                 order_id: int = None):
        
        if order_id is None:
            from app.services.orderInteractor import get_next_order_id
            self._order_id = get_next_order_id()
        else:
            # Only used when reconstructing from JSON
            self._order_id = order_id
            
        self.user_id = user_id
        self.order_items = order_items if order_items is not None else []
        self.address = address
        self.order_date = order_date or datetime.now().isoformat()
        self._total_price = self.calculate_total_price()
    
    #  -- order_id --
    @property
    def order_id(self):
        return self._order_id
    
    # -- user_id --
    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: int):
        if value < 0:
            raise ValueError("user_id must be non-negative")
        self._user_id = value
    
    # -- order_items --
    @property
    def order_items(self):
        return self._order_items
    
    @order_items.setter
    def order_items(self, value: List[OrderItem]):
        self._order_items = value if value is not None else []
    
    # -- address --
    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, value: Address):
        self._address = value
    
    # -- order_date --
    @property
    def order_date(self):
        return self._order_date
    
    @order_date.setter
    def order_date(self, value: str):
        self._order_date = value
    
    # -- total_price --
    @property
    def total_price(self):
        return self._total_price
    
    @total_price.setter
    def total_price(self, value):
        self._total_price = decimal.Decimal(str(value))

    def calculate_total_price(self) -> decimal.Decimal:
        """
        Calculate total price of the order based on its items.
        """
        total = decimal.Decimal("0.00")
        for item in self.order_items:
            total += item.price * item.quantity
        return total
    
    def is_returnable(self, order_id: int) -> bool:
        """
        Check if an order can be returned
        """
        # TODO: Implement return policy logic
        return True

    def to_dict(self):
        """
        Convert Order to dictionary for JSON serialization.
        """
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "order_items": [item.to_dict() for item in self.order_items],
            "address": self.address.to_dict() if self.address else None,
            "order_date": self.order_date,
            "total_price": str(self.total_price)
        }

