import pytest
from datetime import date
from backend.app.schemas.wishListClass import WishList, WishListEntry
from pathlib import Path
from backend.app.services.wishListInteractor import _save_wishList, load_wishList, remove_entry, add_entry


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
Integration Tests
"""

import backend.app.services.wishListInteractor as interactor

# Temp JSON in the same folder
TEST_JSON_PATH = Path(__file__).parent / "test_wishlist.json"
interactor.path = TEST_JSON_PATH 

@pytest.fixture(autouse=True)
def cleanup():
    if TEST_JSON_PATH.exists():
        TEST_JSON_PATH.unlink()
    TEST_JSON_PATH.write_text("{}")
    yield
    if TEST_JSON_PATH.exists():
        TEST_JSON_PATH.unlink()


def test_save_and_load_wishlist():
    wl = WishList(user_id = "user21")
    entry = WishListEntry(product_id=101, date_added=date.today())
    wl.add_entry(entry)

    _save_wishList(wl)
    loaded_wl = load_wishList("user21")

    assert loaded_wl.user_id == "user21"
    assert len(loaded_wl.entries) == 1
    assert loaded_wl.entries[0].product_id == 101


# Looking to see if adding entrys work plus no duplicate entrys
def test_add_entry_integration():
    add_entry("user21", 101)
    wl = load_wishList("user21")
    assert len(wl.entries) == 1
    assert wl.entries[0].product_id == 101

    add_entry("user21", 101)
    wl = load_wishList("user21")
    assert len(wl.entries) == 1


def test_remove_entry_integration():
    add_entry("user21", 101)
    add_entry("user21", 102)

    remove_entry("user21", 101)
    wl = load_wishList("user21")
    assert len(wl.entries) == 1
    assert wl.entries[0].product_id == 102