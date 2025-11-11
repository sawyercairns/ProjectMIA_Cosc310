import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.productInteractor import get_products_filtered, remove_product
import json

client = TestClient(app)

def test_get_products():
    r = client.get("/products?category=test&keyword=test2&maxPrice=100")
    assert r.status_code == 200
    
    r = client.get("/products?maxPrice=100")
    assert r.status_code == 200
    response = r.json()
    for item in response:
        assert item["_price"] <= 100
    

    r = client.get("/products?keyword=USB")
    assert r.status_code == 200
    response = r.json()
    for item in response:
        assert "usb" in item["_product_name"].lower()

def test_create_and_remove_product(mocker):
    mock_validation = mocker.patch("backend.app.routers.productRouter.user_is_admin")
    mock_validation.return_value = True
    r = client.post("/products?username=u&password=p&product_name=UNIQUETESTNAME&description=d&price=14")
    assert r.text == "\"PRODUCT CREATED\""

    product_to_remove = get_products_filtered(keywords="UNIQUETESTNAME", max_price=15)
    mock_validation.return_value = False
    r = client.post("/products?username=u&password=p&product_name=n&description=d&price=14")
    assert r.text == "\"CREATION FAILED\""

    r = client.delete("/products?username=u&password=p&id=" + str(product_to_remove[0].product_id))
    assert len(get_products_filtered(keywords="UNIQUETESTNAME", max_price=15)) > 0
    
    mock_validation.return_value = True
    r = client.delete("/products?username=u&password=p&id=" + str(product_to_remove[0].product_id))
    assert len(get_products_filtered(keywords="UNIQUETESTNAME", max_price=15)) == 0

    