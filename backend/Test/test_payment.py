import pytest
from app.schemas.paymentClass import Payment

# ===== UNIT TESTS =====

def test_payment_creation():
    """Test creating a payment object with valid data"""
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
    """Test updating payment info with valid data"""
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
    """Test that empty fields raise ValueError"""
    payment = Payment(
        user_id="user21",
        card_number="6800000000000000",
        CVV="123",
        expiration_date="12/26"
    )
    
    with pytest.raises(ValueError, match="All fields .* are required"):
        payment.update_payment_info(card_number="", CVV="456", expiration_date="01/30")

def test_update_payment_card_number_non_numeric():
    """Test that non-numeric card number raises ValueError"""
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    
    with pytest.raises(ValueError, match="Card number must contain only digits"):
        payment.update_payment_info(card_number="41111111abcd1111", CVV="123", expiration_date="12/26")


def test_update_payment_card_number_too_long():
    """Test that card number longer than 19 digits raises ValueError"""
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    
    with pytest.raises(ValueError, match="Card number must be between 13 and 19 digits"):
        payment.update_payment_info(card_number="41111111111111111111", CVV="123", expiration_date="12/26")


def test_update_payment_cvv_invalid_length():
    """Test that CVV with invalid length raises ValueError"""
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    
    with pytest.raises(ValueError, match="CVV must be 3 or 4 digits"):
        payment.update_payment_info(card_number="4111111111111111", CVV="12", expiration_date="12/26")


def test_update_payment_expiration_missing_slash():
    """Test that expiration date without slash raises ValueError"""
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    
    with pytest.raises(ValueError, match="Expiration date must be in MM/YY format"):
        payment.update_payment_info(card_number="4111111111111111", CVV="123", expiration_date="1226")

def test_update_payment_expiration_invalid_format():
    """Test that expiration date with wrong format raises ValueError"""
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    
    with pytest.raises(ValueError, match="Expiration date must be in MM/YY format"):
        payment.update_payment_info(card_number="4111111111111111", CVV="123", expiration_date="12/26/2025")


def test_update_payment_expiration_invalid_month():
    """Test that month greater than 12 raises ValueError"""
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    
    with pytest.raises(ValueError, match="Month must be between 01 and 12"):
        payment.update_payment_info(card_number="4111111111111111", CVV="123", expiration_date="13/26")


def test_update_payment_expiration_invalid_year_length():
    """Test that year with wrong length raises ValueError"""
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    
    with pytest.raises(ValueError, match="Year must be 2 digits"):
        payment.update_payment_info(card_number="4111111111111111", CVV="123", expiration_date="12/2026")


# ===== INTEGRATION TESTS =====

import app.services.paymentInteractor as interactor

def test_save_and_load_payment(mocker):
    """Test saving and loading payment data using mocked file operations"""
    mock_data = {}
    mock_load = mocker.patch("app.services.paymentInteractor.load_json")
    mock_load.return_value = mock_data
    mock_write = mocker.patch("app.services.paymentInteractor.write_to_json")
    
    payment = Payment(
        user_id="user21",
        card_number="4111111111111111",
        CVV="123",
        expiration_date="12/26"
    )
    
    interactor._save_payment(payment)
    
    # Verify write was called with correct data
    mock_write.assert_called_once()
    updated_data = mock_write.call_args[0][1]
    assert "user21" in updated_data
    assert updated_data["user21"]["card_number"] == "4111111111111111"
    assert updated_data["user21"]["CVV"] == "123"
    assert updated_data["user21"]["expiration_date"] == "12/26"

def test_load_payment(mocker):
    """Test loading payment data for a specific user"""
    mock_data = {
        "user21": {
            "user_id": "user21",
            "card_number": "4111111111111111",
            "CVV": "123",
            "expiration_date": "12/26"
        }
    }
    mock_load = mocker.patch("app.services.paymentInteractor.load_json")
    mock_load.return_value = mock_data
    
    loaded_payment = interactor.load_payment("user21")
    assert loaded_payment.user_id == "user21"
    assert loaded_payment.card_number == "4111111111111111"
    assert loaded_payment.CVV == "123"
    assert loaded_payment.expiration_date == "12/26"

def test_update_payment_info_integration(mocker):
    """Test updating payment info and saving to file"""
    mock_data = {
        "user21": {
            "user_id": "user21",
            "card_number": "4111111111111111",
            "CVV": "123",
            "expiration_date": "12/26"
        }
    }
    mock_load = mocker.patch("app.services.paymentInteractor.load_json")
    mock_load.return_value = mock_data
    mock_write = mocker.patch("app.services.paymentInteractor.write_to_json")
    
    payment = interactor.load_payment("user21")
    payment.update_payment_info(card_number="5500000000000000", CVV="456", expiration_date="01/30")
    interactor._save_payment(payment)
    
    # Verify the data was updated correctly
    updated_data = mock_write.call_args[0][1]
    assert updated_data["user21"]["card_number"] == "5500000000000000"
    assert updated_data["user21"]["CVV"] == "456"
    assert updated_data["user21"]["expiration_date"] == "01/30"

def test_load_payment_user_not_found(mocker):
    """Test loading payment for non-existent user returns empty payment"""
    mock_data = {}
    mock_load = mocker.patch("app.services.paymentInteractor.load_json")
    mock_load.return_value = mock_data
    
    payment = interactor.load_payment("nonexistent_user")
    assert payment.user_id == "nonexistent_user"
    assert payment.card_number == ""
    assert payment.CVV == ""
    assert payment.expiration_date == "MM/YY"