import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

#TODO: For now, this just makes sure that requests can be made, with filters.
# Update tests to ensure these categories and filters return as expected as these methods are implemented

def test_get_products():
    r = client.get("/products?categories=test&keywords=test2&maxPrice=100")
    assert r.status_code == 200
    r = client.get("/products?maxPrice=100")
    assert r.status_code == 200
    r = client.get("/products?keywords=test2&maxPrice=100")
    assert r.status_code == 200
    r = client.get("/products?categories=test&maxPrice=100")
    assert r.status_code == 200