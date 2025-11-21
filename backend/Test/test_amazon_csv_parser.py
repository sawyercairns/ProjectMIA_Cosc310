# Testing amazon_csv_parser.py
# Created by: Dan Williams
# Reviewed by: 

import pytest
import json
from pathlib import Path
from datetime import date
try:
    from app.repositories.amazon_csv_parser import (
        parse_amazon_csv,
        save_products_json,
        save_users_json,
        save_reviews_json,
        _num,
        _inr_to_cad,
        DATA_DIR
    )
    from app.schemas.productClass import Product
    from app.schemas.userClass import User
    from app.schemas.reviewClass import Review
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from app.repositories.amazon_csv_parser import (
        parse_amazon_csv,
        save_products_json,
        save_users_json,
        save_reviews_json,
        _num,
        _inr_to_cad,
        DATA_DIR
    )
    from app.schemas.productClass import Product
    from app.schemas.userClass import User
    from app.schemas.reviewClass import Review


def test_num_conversion():
    """Test numeric string parsing with various formats."""
    assert _num("₹1,234.56") == 1234.56
    assert _num("$99.99") == 99.99
    assert _num("1234") == 1234.0
    assert _num("") == 0.0
    assert _num(None) == 0.0
    assert _num("-50.25") == -50.25


def test_inr_to_cad_conversion():
    """Test INR to CAD currency conversion."""
    assert _inr_to_cad(1000) == 16.0  
    assert _inr_to_cad(0) == 0.0
    assert _inr_to_cad(62.5) == 1.0
    assert _inr_to_cad(100) == 1.6


def test_parse_amazon_csv_returns_tuples():
    """Test that parse_amazon_csv returns three lists."""
    products, users, reviews = parse_amazon_csv()
    
    assert isinstance(products, list)
    assert isinstance(users, list)
    assert isinstance(reviews, list)


def test_save_products_json_creates_file(tmp_path, monkeypatch):
    """Test that save_products_json creates a JSON file."""
    # Create test product
    test_product = Product(
        product_id=1,
        product_name="Test Product",
        product_desc="Test Description",
        price=10.0,
        discount_price=8.0,
        discount_percent=20.0
    )
    
    # Use tmp directory
    monkeypatch.setattr('app.repositories.amazon_csv_parser.DATA_DIR', tmp_path)
    
    save_products_json([test_product])
    
    output_file = tmp_path / "products.json"
    assert output_file.exists(), "products.json should be created"
    
    # Verify JSON structure
    with output_file.open() as f:
        data = json.load(f)
    
    assert len(data) == 1
    assert data[0]["product_id"] == "1"
    assert data[0]["product_name"] == "Test Product"


def test_save_users_json_creates_file(tmp_path, monkeypatch):
    """Test that save_users_json creates a JSON file."""
    test_user = User(
        user_id=101,
        user_password="test",
        email="test@test.com",
        first_name="John"
    )
    
    monkeypatch.setattr('app.repositories.amazon_csv_parser.DATA_DIR', tmp_path)
    
    save_users_json([test_user])
    
    output_file = tmp_path / "users.json"
    assert output_file.exists(), "users.json should be created"
    
    with output_file.open() as f:
        data = json.load(f)
    
    assert len(data) == 1
    assert data[0]["user_id"] == "101"
    assert data[0]["first_name"] == "John"


def test_save_reviews_json_creates_file(tmp_path, monkeypatch):
    """Test that save_reviews_json creates a JSON file."""
    test_review = Review(
        review_id=1,
        user_id=101,
        product_id=1,
        created_at=date(2025, 10, 28),
        rating=4.5,
        likes=0,
        title="Great product",
        body="Really enjoyed this"
    )
    
    monkeypatch.setattr('app.repositories.amazon_csv_parser.DATA_DIR', tmp_path)
    
    save_reviews_json([test_review])
    
    output_file = tmp_path / "reviews.json"
    assert output_file.exists(), "reviews.json should be created"
    
    with output_file.open() as f:
        data = json.load(f)
    
    assert len(data) == 1
    assert data[0]["review_id"] == "1"
    assert data[0]["title"] == "Great product"
