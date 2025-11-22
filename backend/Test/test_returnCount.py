# Uses Mocking to test returnCount.py

import pytest
from app.schemas.userClass import User
from app.services.returnCount import trackUserReturns
from app.schemas.orderClass import Order



def test_admin_returnCount(mocker):
    user_id = 9999999

    mock_get = mocker.patch(
        "app.services.returnCount.load_orders"
    )

    mock_get.return_value = [
        Order(user_id=101, order_id=1, returned=True),  
        Order(user_id=101, order_id=2, returned=False),
        Order(user_id=101, order_id=3, returned=True),
    ]

    admin_user = User(
        user_id=1,
        user_password="pass",
        email="admin@test.com",
        is_admin=True
    )

    count = trackUserReturns(admin_user, user_id)

    assert count == 2



def test_nonAdmin_returnCount(mocker):
    user_id = 9999999

    mocker.patch(
        "app.services.returnCount.load_orders",
        return_value=[]
    )

    customer = User(
        user_id=1,
        user_password="pass",
        email="admin@test.com",
        is_admin=False
    )

    with pytest.raises(PermissionError, match="Access denied, only admins can view return stats."):
        trackUserReturns(customer, user_id)
