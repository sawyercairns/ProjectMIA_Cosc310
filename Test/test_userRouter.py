import pytest
import pytest_mock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.schemas.userClass import User

client = TestClient(app)

def test_validation_router(mocker):
    mock_validation = mocker.patch("backend.app.routers.userRouter.get_user")
    mock_validation.return_value = User(0,"password","email@email.com")
    r = client.get("/login?email=Manav&password=test")
    assert r.text == "\"VALID USER\""

    mock_validation.return_value = None
    r = client.get("/login?email=Jimmy&password=NotAPassword")
    assert r.text == "\"INVALID USERNAME OR PASSWORD\""