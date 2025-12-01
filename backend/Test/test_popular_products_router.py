import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_popular_router(mocker):
    r = client.get("/products/popularProducts")
    assert r.status_code == 200

    mock = mocker.patch("app.routers.productRouter.get_popular_products")
    mock.return_value = {"Number 1": 3, "Number 2": 2, "Number 1": 1}
    r = client.get("/products/popularProducts")
    assert r.json() == {"Number 1": 3, "Number 2": 2, "Number 1": 1}