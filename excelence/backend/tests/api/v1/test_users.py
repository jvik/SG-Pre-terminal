from fastapi.testclient import TestClient


def test_create_user_success(client: TestClient, mocker):
    mocker.patch(
        "app.db.session.supabase.auth.sign_up",
        return_value={
            "access_token": "fake_token",
            "token_type": "bearer",
            "user": {"email": "test@example.com"},
        },
    )
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "test@example.com", "password": "ValidPassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["user"]["email"] == "test@example.com"


def test_create_user_existing_email(client: TestClient, mocker):
    mocker.patch(
        "app.db.session.supabase.auth.sign_up",
        side_effect=Exception("User already exists"),
    )

    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "test1@example.com", "password": "ValidPassword123"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "User already exists"
