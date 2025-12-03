from datetime import date
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.reviewClass import Review

client = TestClient(app)

def test_get_reviews():
    r = client.get("/reviews/9150")
    response = r.json()
    assert len(response) != 0
    for item in response:
        assert item["user_id"] == "9150"

def test_add_remove_reviews():
    # Clean up any existing reviews first
    r = client.get("/reviews/9151")
    existing = r.json()
    for review in existing:
        client.delete("/reviews/" + str(review["review_id"]) + "?email=admin@admin.com&password=password")
    
    r = client.post("/reviews?user_id=9151&product_id=100&rating=2.5&title=title&body=body")
    r = client.get("/reviews/9151")
    response = r.json()
    id = response[0]["review_id"]
    assert len(response) == 1
    r = client.delete("/reviews/" + str(id) + "?email=admin@admin.com&password=password")
    r = client.get("/reviews/9151")
    response = r.json()
    assert len(response) == 0

