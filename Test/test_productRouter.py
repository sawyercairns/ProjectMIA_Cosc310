import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
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
        assert "USB" in item["_product_name"]