import decimal
import pytest
from app.services.addRandomToCart import add_random_product
from app.schemas.orderItemClass import OrderItem

def test_add_random_product_mocker(mocker):
    fake_user_id = "fake_user_123"

    # Mock json.load to return some real products (or minimal fake products)
    fake_products = [
        {
            "product_id": "1",
            "product_name": "Test Product",
            "product_desc": "Test Description",
            "price": 9.99
        },
        {
            "product_id": "2",
            "product_name": "Test Product 2",
            "product_desc": "Test Description 2",
            "price": 9.98
        },
        {
            "product_id": "3",
            "product_name": "Test Product 3",
            "product_desc": "Test Description 3",
            "price": 9.97
        }
    ]

    mocker.patch("app.services.addRandomToCart.json.load", return_value=fake_products)
    mock_add_item = mocker.patch("app.services.addRandomToCart.add_item")

    add_random_product(fake_user_id)

    called_user_id, called_order_item = mock_add_item.call_args[0]
    assert called_user_id == fake_user_id
    assert called_order_item.quantity == 1



def test_add_random_product_no_products(mocker):
    fake_user_id = "fake_user_123"

    # Mock json.load to return some real products (or minimal fake products)
    fake_products = []

    mocker.patch("app.services.addRandomToCart.json.load", return_value=fake_products)

    with pytest.raises(ValueError):
        add_random_product(fake_user_id)