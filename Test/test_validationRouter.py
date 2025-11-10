import pytest
import pytest_mock
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_validation_router(mocker):
    mock_validation = mocker.patch("backend.app.routers.userSignInRouter.user_is_valid")
    mock_validation.return_value = True
    r = client.get("/loginManav?password=test")
    assert r.text == "\"VALID USER\""

    mock_validation.return_value = False
    r = client.get("/loginJimmy?password=NotAPassword")
    assert r.text == "\"INVALID USERNAME OR PASSWORD\""