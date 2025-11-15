from backend.app.schemas.orderClass import Order
from backend.app.schemas.orderItemClass import OrderItem
from backend.app.schemas.addressClass import Address
import pytest
import decimal


def test_order_auto_increment():
    """
    Test that order_id is automatically assigned when not provided.
    Note: This reads from orders.json but does NOT save, so it doesn't 
    affect the actual order counter in the file.
    """
    item1 = OrderItem(1, "Product", "Description", 1, 10.99)
    
    order = Order(
        user_id=101,
        order_items=[item1]
    )
    
    assert order.order_id is not None
    assert order.order_id >= 1
    assert order.user_id == 101


def test_order_creation_full():
    addr = Address("123 Main St", "Apt 4B", "Vancouver", "BC", "Canada")
    item1 = OrderItem(1, "Test Product", "Description", 2, 10.99)
    
    order = Order(
        user_id=101,
        order_items=[item1],
        address=addr,
        order_id=1  
    )
    
    assert order.order_id == 1
    assert order.user_id == 101
    assert len(order.order_items) == 1
    assert order.address.line1 == "123 Main St"
    assert order.total_price == decimal.Decimal("21.98")
    assert order.order_date is not None


def test_minimal_order():
    order = Order(user_id=102, order_id=2)
    
    assert order.order_id == 2
    assert order.user_id == 102
    assert order.order_items == []
    assert order.address is None
    assert order.total_price == decimal.Decimal("0")


def test_order_multiple_items():
    item1 = OrderItem(1, "Product 1", "Desc 1", 2, 10.99)
    item2 = OrderItem(2, "Product 2", "Desc 2", 1, 25.50)
    item3 = OrderItem(3, "Product 3", "Desc 3", 3, 5.00)
    
    order = Order(
        user_id=103,
        order_items=[item1, item2, item3],
        order_id=3
    )
    
    assert len(order.order_items) == 3
    assert order.total_price == decimal.Decimal("62.48")


def test_user_id_validation():
    order = Order(user_id=101, order_id=1)
    assert order.user_id == 101
    
    with pytest.raises(ValueError, match="user_id must be non-negative"):
        order.user_id = -1


def test_order_to_dict():
    addr = Address("456 Oak Ave", "", "Toronto", "ON", "Canada")
    item1 = OrderItem(10, "Widget", "A useful widget", 3, 15.99)
    
    order = Order(
        user_id=105,
        order_items=[item1],
        address=addr,
        order_date="2025-11-13T10:30:00",
        order_id=10
    )
    
    result = order.to_dict()
    
    assert result["order_id"] == 10
    assert result["user_id"] == 105
    assert len(result["order_items"]) == 1
    assert result["order_items"][0]["product_id"] == 10
    assert result["order_items"][0]["product_name"] == "Widget"
    assert result["order_items"][0]["quantity"] == 3
    assert result["address"]["line1"] == "456 Oak Ave"
    assert result["address"]["city"] == "Toronto"
    assert result["order_date"] == "2025-11-13T10:30:00"
    assert result["total_price"] == "47.97"


def test_order_items_setter():
    order = Order(user_id=108, order_id=13)
    assert order.order_items == []
    
    item1 = OrderItem(1, "Product", "Desc", 1, 5.99)
    order.order_items = [item1]
    
    assert len(order.order_items) == 1
    assert order.order_items[0]._product_id == 1


def test_address_setter():
    order = Order(user_id=109, order_id=14)
    assert order.address is None
    
    addr = Address("999 Elm St", "Unit 5", "Montreal", "QC", "Canada")
    order.address = addr
    
    assert order.address.line1 == "999 Elm St"
    assert order.address.city == "Montreal"


def test_total_price_setter():
    order = Order(user_id=110, order_id=15)
    
    order.total_price = 99.99
    assert order.total_price == decimal.Decimal("99.99")
    
    order.total_price = "150.50"
    assert order.total_price == decimal.Decimal("150.50")
    
    order.total_price = 200
    assert order.total_price == decimal.Decimal("200")

def test_order_date():
    order = Order(user_id=111, order_id=16)

    assert order.order_date is not None
    
    custom_date = "2025-12-25T12:00:00"
    order.order_date = custom_date
    assert order.order_date == custom_date
