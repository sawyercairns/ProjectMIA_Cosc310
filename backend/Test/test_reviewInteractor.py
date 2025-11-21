
from datetime import date
from app.schemas.reviewClass import Review
from app.services.reviewInteractor import create_review, remove_review, get_reviews

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
