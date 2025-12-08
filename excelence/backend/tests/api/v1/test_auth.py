from fastapi.testclient import TestClient
import pytest
from gotrue.errors import AuthApiError

def test_login_success(client: TestClient, mocker):
    mocker.patch(
        "app.db.session.supabase.auth.sign_in_with_password",
        return_value={
            "access_token": "fake_token",
            "token_type": "bearer",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "ValidPassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "fake_token"
    assert data["token_type"] == "bearer"


def test_login_failure(client: TestClient, mocker):
    mocker.patch(
        "app.db.session.supabase.auth.sign_in_with_password",
        side_effect=AuthApiError("Invalid login credentials", 400, "invalid_credentials"),
    )

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid login credentials"
