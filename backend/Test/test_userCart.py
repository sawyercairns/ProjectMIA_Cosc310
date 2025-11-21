import pytest
import decimal
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.productClass import Product
from app.schemas.orderItemClass import OrderItem
from app.schemas.cartClass import Cart

client = TestClient(app)



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


# ---- Test delete_item function ----
def test_delete_item_success(mocker):
    """Test successful deletion of an item from cart"""
    user_id = "123"
    product_id = "1"

    mock_cart_data = {
        user_id: {
            "cart_value": "29.98",
            "cart_items": [
                {
                    "product_id": 1,
                    "product_name": "USB Cable",
                    "product_desc": "Durable cable",
                    "quantity": 2,
                    "price": "14.99"
                }
            ]
        }
    }
    
    mock_load = mocker.patch("app.services.cartInteractor.load_json")
    mock_load.return_value = mock_cart_data
    
    mock_write = mocker.patch("app.services.cartInteractor.write_to_json")
    
    from app.services.cartInteractor import delete_item
    
    result = delete_item(user_id, product_id)
    
    assert result["cart_value"] == "0.00"
    assert len(result["cart_items"]) == 0
    
    mock_write.assert_called_once()


def test_delete_item_not_found(mocker):
    """Test deletion fails when product not in cart"""
    user_id = "123"
    product_id = "999" 
    
    mock_cart_data = {
        user_id: {
            "cart_value": "14.99",
            "cart_items": [
                {
                    "product_id": 1,
                    "product_name": "USB Cable",
                    "product_desc": "Durable cable",
                    "quantity": 1,
                    "price": "14.99"
                }
            ]
        }
    }
    
    mock_load = mocker.patch("app.services.cartInteractor.load_json")
    mock_load.return_value = mock_cart_data
    
    from app.services.cartInteractor import delete_item

    with pytest.raises(ValueError, match="Product with id 999 not found in cart"):
        delete_item(user_id, product_id)


def test_delete_item_invalid_product_id(mocker):
    """Test deletion fails with invalid product_id format"""
    user_id = "123"
    product_id = "invalid_id"
    
    mock_cart_data = {
        user_id: {
            "cart_value": "14.99",
            "cart_items": [
                {
                    "product_id": 1,
                    "product_name": "USB Cable",
                    "product_desc": "Durable cable",
                    "quantity": 1,
                    "price": "14.99"
                }
            ]
        }
    }
    
    mock_load = mocker.patch("app.services.cartInteractor.load_json")
    mock_load.return_value = mock_cart_data
    
    from app.services.cartInteractor import delete_item
    
    with pytest.raises(ValueError, match="Invalid product_id"):
        delete_item(user_id, product_id)


def test_delete_item_multiple_items(mocker):
    """Test deletion removes only the specified item"""
    user_id = "123"
    product_id = "2"
    
    mock_cart_data = {
        user_id: {
            "cart_value": "39.98",
            "cart_items": [
                {
                    "product_id": 1,
                    "product_name": "USB Cable",
                    "product_desc": "Durable cable",
                    "quantity": 1,
                    "price": "14.99"
                },
                {
                    "product_id": 2,
                    "product_name": "Charger",
                    "product_desc": "Fast charger",
                    "quantity": 1,
                    "price": "24.99"
                }
            ]
        }
    }
    
    mock_load = mocker.patch("app.services.cartInteractor.load_json")
    mock_load.return_value = mock_cart_data

    mock_write = mocker.patch("app.services.cartInteractor.write_to_json")
    
    from app.services.cartInteractor import delete_item
 
    result = delete_item(user_id, product_id)

    assert len(result["cart_items"]) == 1
    assert result["cart_items"][0]["product_id"] == 1
    assert result["cart_value"] == "14.99"

    mock_write.assert_called_once()



# ---- Test delete_item endpoint ----
def test_delete_item_endpoint_success(mocker):
    """Test DELETE /cart/items endpoint successfully deletes item"""
    user_id = "123"
    product_id = "1"
    
    mock_delete = mocker.patch("app.routers.cartRouter.delete_item")
    mock_delete.return_value = {
        "cart_value": "0.00",
        "cart_items": []
    }
    
    response = client.delete(f"/cart/items?user_id={user_id}&product_id={product_id}")
    
    assert response.status_code == 200
    assert response.json()["cart_value"] == "0.00"
    assert len(response.json()["cart_items"]) == 0
    
    mock_delete.assert_called_once_with(user_id, product_id)
