from datetime import date
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.schemas.reviewClass import Review

client = TestClient(app)

def test_get_reviews():
    r = client.get("/reviews/9150")
    response = r.json()
    assert len(response) != 0
    for item in response:
        assert item["user_id"] == "9150"

def test_add_remove_reviews():
    r = client.post("/reviews?user_id=9151&product_id=100&rating=2.5&title=title&body=body")
    r = client.get("/reviews/9151")
    response = r.json()
    id = response[0]["review_id"]
    assert len(response) != 0
    r = client.delete("/reviews" + id + "?email=admin@admin.com&password=password")
    r = client.get("/reviews/9151")
    response = r.json()
    assert len(response) == 0

