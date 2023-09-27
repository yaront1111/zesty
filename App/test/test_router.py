import pytest
import jwt
import datetime
from App.app.router import app

JWT_SECRET_KEY = "test_api"
CODE_NAME = "test"
def test_health_check():
    """Test the health check endpoint."""
    response = app.test_client().get("/health")
    assert response.status_code == 200


def test_get_token():
    """Test the token generation endpoint."""
    response = app.test_client().get("/token")
    assert response.status_code == 200
