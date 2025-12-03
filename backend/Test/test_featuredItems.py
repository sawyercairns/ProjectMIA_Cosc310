import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.featuredItemsClass import FeaturedItems
from app.services.featuredItemsInteractor import get_featured_items, add_featured_item, remove_featured_item

client = TestClient(app)


"""
Unit Tests
"""

def test_featured_items_creation():
    """Test creating a FeaturedItems instance"""
    featured = FeaturedItems(featured_product_ids=["101", "102", "103"])
    assert len(featured.featured_product_ids) == 3
    assert "101" in featured.featured_product_ids


def test_featured_items_empty_creation():
    """Test creating an empty FeaturedItems instance"""
    featured = FeaturedItems()
    assert len(featured.featured_product_ids) == 0
    assert featured.featured_product_ids == []


def test_featured_items_to_dict():
    """Test FeaturedItems to_dict method"""
    featured = FeaturedItems(featured_product_ids=["101", "102"])
    result = featured.to_dict()
    assert "featured_product_ids" in result
    assert result["featured_product_ids"] == ["101", "102"]


def test_featured_items_setter():
    """Test setting featured_product_ids"""
    featured = FeaturedItems()
    featured.featured_product_ids = ["201", "202"]
    assert len(featured.featured_product_ids) == 2
    assert "201" in featured.featured_product_ids


"""
Integration Tests
"""

def test_get_featured_items_empty(mocker):
    """Test getting featured items when list is empty"""
    mock_load = mocker.patch("app.services.featuredItemsInteractor.load_json")
    mock_load.return_value = {"featured_product_ids": []}
    
    featured = get_featured_items()
    
    mock_load.assert_called_once_with("featuredItems.json")
    assert len(featured.featured_product_ids) == 0


def test_add_featured_item_success(mocker):
    """Test successfully adding a product to featured items"""
    mock_load = mocker.patch("app.services.featuredItemsInteractor.load_json")
    mock_load.return_value = {"featured_product_ids": ["100"]}
    
    mock_write = mocker.patch("app.services.featuredItemsInteractor.write_to_json")
    
    featured = add_featured_item("200")
    
    mock_write.assert_called_once()
    written_data = mock_write.call_args[0][1]
    assert "200" in written_data["featured_product_ids"]
    assert "100" in written_data["featured_product_ids"]
    assert len(written_data["featured_product_ids"]) == 2


def test_add_featured_item_duplicate(mocker):
    """Test adding a duplicate product raises ValueError"""
    mock_load = mocker.patch("app.services.featuredItemsInteractor.load_json")
    mock_load.return_value = {"featured_product_ids": ["100", "200"]}
    
    with pytest.raises(ValueError, match="already in featured items"):
        add_featured_item("100")


def test_remove_featured_item_success(mocker):
    """Test successfully removing a product from featured items"""
    mock_load = mocker.patch("app.services.featuredItemsInteractor.load_json")
    mock_load.return_value = {"featured_product_ids": ["100", "200", "300"]}
    
    mock_write = mocker.patch("app.services.featuredItemsInteractor.write_to_json")
    
    featured = remove_featured_item("200")
    
    mock_write.assert_called_once()
    written_data = mock_write.call_args[0][1]
    assert "200" not in written_data["featured_product_ids"]
    assert "100" in written_data["featured_product_ids"]
    assert "300" in written_data["featured_product_ids"]
    assert len(written_data["featured_product_ids"]) == 2


def test_remove_featured_item_not_found(mocker):
    """Test removing a non-existent product raises ValueError"""
    mock_load = mocker.patch("app.services.featuredItemsInteractor.load_json")
    mock_load.return_value = {"featured_product_ids": ["100", "200"]}
    
    with pytest.raises(ValueError, match="not in featured items"):
        remove_featured_item("999")


"""
API Router Tests
"""

def test_get_featured_endpoint(mocker):
    """Test GET /featured endpoint"""
    mock_load = mocker.patch("app.services.featuredItemsInteractor.load_json")
    mock_load.return_value = {"featured_product_ids": ["100", "200"]}
    
    response = client.get("/featured")
    
    assert response.status_code == 200
    data = response.json()
    assert "featured_product_ids" in data
    assert len(data["featured_product_ids"]) == 2


def test_add_featured_endpoint_success(mocker):
    """Test POST /featured endpoint with admin user"""
    def mock_load_json(filename):
        if filename == "featuredItems.json":
            return {"featured_product_ids": []}
        elif filename == "users.json":
            return [{"email": "admin@admin.com", "is_admin": True}]
        return {}
    
    mocker.patch("app.services.Interactor.load_json", side_effect=mock_load_json)
    
    mock_write = mocker.patch("app.services.featuredItemsInteractor.write_to_json")
    
    response = client.post("/featured", json={
        "product_id": "300",
        "admin_email": "admin@admin.com"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Product added" in data["message"]


def test_remove_featured_endpoint_success(mocker):
    """Test DELETE /featured/{product_id} endpoint with admin user"""
    def mock_load_json(filename):
        if filename == "featuredItems.json":
            return {"featured_product_ids": ["100", "200"]}
        elif filename == "users.json":
            return [{"email": "admin@admin.com", "is_admin": True}]
        return {}
    
    mocker.patch("app.services.Interactor.load_json", side_effect=mock_load_json)
    
    mock_write = mocker.patch("app.services.featuredItemsInteractor.write_to_json")
    
    response = client.delete("/featured/100?admin_email=admin@admin.com")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "removed" in data["message"]

