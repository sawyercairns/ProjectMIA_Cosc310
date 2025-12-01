import pytest
from app.schemas.paymentClass import Payment
from pathlib import Path

"""Unit Tests"""

def test_payment_creation():
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    
    assert payment.user_id == "user21"
    assert payment.card_number == "4111111111111111"
    assert payment.CVV == "123"
    assert payment.expiration_date == "12/26"

def test_update_payment_info_success():
    payment = Payment(
        user_id="user21",
        card_number="5200000000000000",
        CVV="123",
        expiration_date="12/26"
    )
    
    payment.update_payment_info(card_number="6400000000000000", CVV="456", expiration_date="01/30")
    assert payment.card_number == "6400000000000000"
    assert payment.CVV == "456"
    assert payment.expiration_date == "01/30"

def test_update_payment_info_missing_field():
    payment = Payment(
        user_id="user21",
        card_number="6800000000000000",
        CVV="123",
        expiration_date="12/26"
    )
    
    with pytest.raises(ValueError):
        payment.update_payment_info(card_number="", CVV="456", expiration_date="01/30")


"""Integration Tests"""

import app.services.paymentInteractor as interactor

TEST_JSON_PATH = Path(__file__).parent / "test_payment.json"
interactor.path = TEST_JSON_PATH  

@pytest.fixture(autouse=True)
def cleanup():
    if TEST_JSON_PATH.exists():
        TEST_JSON_PATH.unlink()
    TEST_JSON_PATH.write_text("{}") 
    yield
    if TEST_JSON_PATH.exists():
        TEST_JSON_PATH.unlink()

def test_save_and_load_payment():
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    
    interactor._save_payment(payment)
    
    loaded_payment = interactor.load_payment("user21")
    assert loaded_payment.user_id == "user21"
    assert loaded_payment.card_number == "4111111111111111"
    assert loaded_payment.CVV == "123"
    assert loaded_payment.expiration_date == "12/26"

def test_update_payment_info_integration():
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    interactor._save_payment(payment)
    
    payment.update_payment_info(card_number="5500000000000000", CVV="456", expiration_date="01/30")
    interactor._save_payment(payment)
    
    loaded_payment = interactor.load_payment("user21")
    assert loaded_payment.card_number == "5500000000000000"
    assert loaded_payment.CVV == "456"
    assert loaded_payment.expiration_date == "01/30"