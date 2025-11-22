import pytest
from datetime import date
from app.schemas.reviewClass import Review
from app.services.reviewInteractor import create_review, remove_review, get_reviews, update_review

def test_get_reviews():
    assert len(get_reviews(9150)) > 0
    assert len(get_reviews(-1)) == 0

def test_create_and_remove_review():
    rev = Review(0, 9151, 10, date.today(), 5, 100, "Test", "Testing")
    create_review(rev)
    r = get_reviews(9151)
    assert len(r) == 1
    remove_review(int(r[0]["review_id"]))
    r = get_reviews(9151)
    assert len(r) == 0

def test_update_review():
    rev = Review(0, 999999, 10, date.today(), 4, 50, "Test", "Test")
    create_review(rev)

    update_review(999999, 10, rating=5, title="Updated Test", body="Updated Testing")
    r = get_reviews(999999)
    assert len(r) == 1
    assert r[0]["rating"] == 5
    assert r[0]["title"] == "Updated Test"
    assert r[0]["body"] == "Updated Testing"

    remove_review(int(r[0]["review_id"]))

def test_update_nonexisting_review():
    with pytest.raises(ValueError):
        update_review(12345678999, 10, rating=5)