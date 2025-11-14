import pytest
import pytest_mock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.schemas.userClass import User
from backend.app.services.userInteractor import get_user

client = TestClient(app)

def test_validation_router(mocker):
    mock_validation = mocker.patch("backend.app.routers.userRouter.get_user")
    mock_validation.return_value = User(0,"password","email@email.com")
    r = client.get("/login?email=Manav&password=test")
    assert r.text == "\"VALID USER\""

    mock_validation.return_value = None
    r = client.get("/login?email=Jimmy&password=NotAPassword")
    assert r.text == "\"INVALID USERNAME OR PASSWORD\""

def test_add_remove_user():
    r = client.post("/login?email=e@e.com&password=p")
    u = get_user("e@e.com", "p")
    assert u is not None
    r = client.delete("/login" + str(u.user_id) + "?email=admin@admin.com&password=password")
    u = get_user("e@e.com", "p")
    assert u is None

def test_add_remove_admin():
    r = client.post("/login/admin?auth_email=admin@admin.com&auth_password=password&email=e@e.com&password=p")
    u = get_user("e@e.com", "p")
    assert u is not None
    r = client.delete("/login" + str(u.user_id) + "?email=admin@admin.com&password=password")
    u = get_user("e@e.com", "p")
    assert u is None