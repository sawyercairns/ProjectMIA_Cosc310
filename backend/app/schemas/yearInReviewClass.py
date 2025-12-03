import decimal
from typing import Optional


class YearInReview:
    def __init__(self,
                 user_id: int,
                 year: int,
                 total_spent: decimal.Decimal = None,
                 total_orders: int = 0,
                 avg_order_amount: decimal.Decimal = None,
                 items_purchased: int = 0,
                 reviews_written: int = 0,
                 likes_received: int = 0,
                 biggest_order: decimal.Decimal = None,
                 orders_returned: int = 0):
        
        self.user_id = user_id
        self.year = year
        self._total_spent = total_spent if total_spent is not None else decimal.Decimal("0.00")
        self._total_orders = total_orders
        self._avg_order_amount = avg_order_amount if avg_order_amount is not None else decimal.Decimal("0.00")
        self._items_purchased = items_purchased
        self._reviews_written = reviews_written
        self._likes_received = likes_received
        self._biggest_order = biggest_order if biggest_order is not None else decimal.Decimal("0.00")
        self._orders_returned = orders_returned
    
    # -- user_id --
    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: int):
        if value < 0:
            raise ValueError("user_id must be non-negative")
        self._user_id = value
    
    # -- year --
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, value: int):
        if value < 2000 or value > 2100:
            raise ValueError("year must be between 2000 and 2100")
        self._year = value
    
    # -- total_spent --
    @property
    def total_spent(self):
        return self._total_spent
    
    @total_spent.setter
    def total_spent(self, value):
        self._total_spent = decimal.Decimal(str(value))
    
    # -- total_orders --
    @property
    def total_orders(self):
        return self._total_orders
    
    @total_orders.setter
    def total_orders(self, value: int):
        if value < 0:
            raise ValueError("total_orders cannot be negative")
        self._total_orders = value
    
    # -- avg_order_amount --
    @property
    def avg_order_amount(self):
        return self._avg_order_amount
    
    @avg_order_amount.setter
    def avg_order_amount(self, value):
        self._avg_order_amount = decimal.Decimal(str(value))
    
    # -- items_purchased --
    @property
    def items_purchased(self):
        return self._items_purchased
    
    @items_purchased.setter
    def items_purchased(self, value: int):
        if value < 0:
            raise ValueError("items_purchased cannot be negative")
        self._items_purchased = value
    
    # -- reviews_written --
    @property
    def reviews_written(self):
        return self._reviews_written
    
    @reviews_written.setter
    def reviews_written(self, value: int):
        if value < 0:
            raise ValueError("reviews_written cannot be negative")
        self._reviews_written = value
    
    # -- likes_received --
    @property
    def likes_received(self):
        return self._likes_received
    
    @likes_received.setter
    def likes_received(self, value: int):
        if value < 0:
            raise ValueError("likes_received cannot be negative")
        self._likes_received = value
    
    # -- biggest_order --
    @property
    def biggest_order(self):
        return self._biggest_order
    
    @biggest_order.setter
    def biggest_order(self, value):
        self._biggest_order = decimal.Decimal(str(value))
    
    # -- orders_returned --
    @property
    def orders_returned(self):
        return self._orders_returned
    
    @orders_returned.setter
    def orders_returned(self, value: int):
        if value < 0:
            raise ValueError("orders_returned cannot be negative")
        self._orders_returned = value
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "year": self.year,
            "total_spent": str(self.total_spent),
            "total_orders": self.total_orders,
            "avg_order_amount": str(self.avg_order_amount),
            "items_purchased": self.items_purchased,
            "reviews_written": self.reviews_written,
            "likes_received": self.likes_received,
            "biggest_order": str(self.biggest_order),
            "orders_returned": self.orders_returned
        }
