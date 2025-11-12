import pytest
import decimal
from backend.app.schemas.productClass import Product
from backend.app.schemas.orderItemClass import OrderItem
from backend.app.schemas.cartClass import Cart



# ---- Test OrderItem ----
def test_order_item_creation():
    product = Product(
        product_id = 2,
        product_name = "USB Cable",
        product_desc = "Durable cable",
        price = 10.00
    )
    order_item = OrderItem.order_item(product, quantity=2)

    assert order_item._product_id == 2
    assert order_item._quantity == 2
    assert order_item._price == decimal.Decimal("10.00")

# ---- Test Cart ----
def test_cart_add_item():
    cart = Cart(user_id = "0", cart_items = [], cart_value = decimal.Decimal(0))
    product = Product(product_id = 3, product_name = "Charger", product_desc = "Fast charger", price=15.00)
    order_item = OrderItem.order_item(product, quantity = 1)

    cart._cart_items.append(order_item)
    cart._cart_value += order_item._price * order_item._quantity

    assert len(cart._cart_items) == 1
    assert cart._cart_value == decimal.Decimal("15.00")

# ---- Test Cart to_dict ----
def test_cart_to_dict():
    cart = Cart(user_id = "0", cart_items=[], cart_value=decimal.Decimal(0))
    result = cart.to_dict()

    assert isinstance(result, dict)
    assert "cart_value" in result
    assert "cart_items" in result
