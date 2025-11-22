import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.userClass import User
from app.services.productInteractor import get_products_filtered, remove_product
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
    mock_validation = mocker.patch("app.routers.productRouter.authenticate_admin")
    mock_validation.return_value = User(0,"password","email@email.com", is_admin= True)
    r = client.post("/products?email=u&password=p&product_name=UNIQUETESTNAME&description=d&price=14")
    assert r.text == "\"PRODUCT CREATED\""

    product_to_remove = get_products_filtered(keywords="UNIQUETESTNAME", max_price=15)
    
    from fastapi import HTTPException
    mock_validation.side_effect = HTTPException(status_code=403, detail="Admin access required")
    r = client.post("/products?email=u&password=p&product_name=n&description=d&price=14")
    assert r.status_code == 403

    r = client.delete("/products?email=u&password=p&id=" + str(product_to_remove[0].product_id))
    assert r.status_code == 403
    
    mock_validation.side_effect = None
    mock_validation.return_value = User(0,"password","email@email.com", is_admin= True)
    r = client.delete("/products?email=u&password=p&id=" + str(product_to_remove[0].product_id))
    assert len(get_products_filtered(keywords="UNIQUETESTNAME", max_price=15)) == 0

    