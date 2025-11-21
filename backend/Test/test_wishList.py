import pytest
from datetime import date
from app.schemas.wishListClass import WishList, WishListEntry
from app.services.wishListInteractor import _save_wishList, load_wishList, remove_entry, add_entry


"""
Unit tests
"""

def test_wishlist_entry_creation():
    entry = WishListEntry(product_id=101, date_added = date.today())
    assert entry.product_id == 101
    assert isinstance(entry.date_added, date)


def test_wishlist_add_entry():
    wl = WishList(user_id = "user21")
    entry1 = WishListEntry(product_id=101, date_added = date.today())
    wl.add_entry(entry1)
    
    assert len(wl.entries) == 1
    assert wl.entries[0].product_id == 101

    # Adding duplicate should not increase length
    wl.add_entry(entry1)
    assert len(wl.entries) == 1


def test_wishlist_remove_entry():
    wl = WishList(user_id = "user21")
    entry1 = WishListEntry(product_id=101, date_added = date.today())
    entry2 = WishListEntry(product_id=102, date_added = date.today())
    wl.add_entry(entry1)
    wl.add_entry(entry2)

    wl.remove_entry(101)
    assert len(wl.entries) == 1
    assert wl.entries[0].product_id == 102


"""
Integration Tests (using mocking)
"""


def test_save_and_load_wishlist(mocker):
    """Test saving and loading wishlist with mocked file operations"""
    user_id = "user21"
    today = date.today()
    
    mock_load = mocker.patch("app.services.wishListInteractor.load_json")
    mock_load.return_value = {}
    
    mock_write = mocker.patch("app.services.wishListInteractor.write_to_json")
    
    mock_exists = mocker.patch("app.services.wishListInteractor.os.path.exists")
    mock_exists.return_value = True
    
    wl = WishList(user_id=user_id)
    entry = WishListEntry(product_id=101, date_added=today)
    wl.add_entry(entry)
    
    _save_wishList(wl)
    
    mock_write.assert_called_once()
    written_data = mock_write.call_args[0][1]
    assert user_id in written_data
    assert len(written_data[user_id]["entries"]) == 1
    

    mock_load.return_value = written_data
    

    loaded_wl = load_wishList(user_id)
    assert loaded_wl.user_id == user_id
    assert len(loaded_wl.entries) == 1
    assert loaded_wl.entries[0].product_id == 101


def test_add_entry_integration(mocker):
    """Test adding entries with mocked file operations"""
    user_id = "user21"
    
    mock_exists = mocker.patch("app.services.wishListInteractor.os.path.exists")
    mock_exists.return_value = True
   
    mock_load = mocker.patch("app.services.wishListInteractor.load_json")
    mock_load.return_value = {}
    
    mock_write = mocker.patch("app.services.wishListInteractor.write_to_json")

    add_entry(user_id, 101)
    
    written_data = mock_write.call_args[0][1]
    assert len(written_data[user_id]["entries"]) == 1
    assert written_data[user_id]["entries"][0]["product_id"] == 101
    
    mock_load.return_value = written_data
    
    add_entry(user_id, 101)
    
    written_data = mock_write.call_args[0][1]
    assert len(written_data[user_id]["entries"]) == 1


def test_remove_entry_integration(mocker):
    """Test removing entries with mocked file operations"""
    user_id = "user21"
    today = date.today()
    
    mock_exists = mocker.patch("app.services.wishListInteractor.os.path.exists")
    mock_exists.return_value = True
    
    initial_data = {
        user_id: {
            "entries": [
                {"product_id": 101, "date_added": today.isoformat()},
                {"product_id": 102, "date_added": today.isoformat()}
            ]
        }
    }
    mock_load = mocker.patch("app.services.wishListInteractor.load_json")
    mock_load.return_value = initial_data
    
    mock_write = mocker.patch("app.services.wishListInteractor.write_to_json")
    

    remove_entry(user_id, 101)

    mock_write.assert_called_once()
    written_data = mock_write.call_args[0][1]
    assert len(written_data[user_id]["entries"]) == 1
    assert written_data[user_id]["entries"][0]["product_id"] == 102


def test_add_entry_limit(mocker):
    """Test that adding more than 10 entries raises an error"""
    user_id = "user21"
    today = date.today()
    
    mock_exists = mocker.patch("app.services.wishListInteractor.os.path.exists")
    mock_exists.return_value = True

    entries = [
        {"product_id": 100 + i, "date_added": today.isoformat()}
        for i in range(10)
    ]
    mock_data = {
        user_id: {
            "entries": entries
        }
    }
    mock_load = mocker.patch("app.services.wishListInteractor.load_json")
    mock_load.return_value = mock_data
    
    mock_write = mocker.patch("app.services.wishListInteractor.write_to_json")

    with pytest.raises(ValueError, match="Too many entries in wishlist."):
        add_entry(user_id, 999)
    
    mock_write.assert_not_called()