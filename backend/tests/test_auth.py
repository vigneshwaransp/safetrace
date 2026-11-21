from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.audit_log import AuditLog
from app.core.security import verify_password


def test_user_registration(client: TestClient, db_session: Session):
    payload = {
        "email": "sarah.survivor@example.com",
        "password": "StrongPassword123!",
        "full_name": "Sarah Doe",
        "role": "USER",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["role"] == "USER"
    assert "password" not in data

    # Verify user in database has Argon2 hashed password
    user = db_session.query(User).filter(User.email == payload["email"]).first()
    assert user is not None
    assert user.hashed_password.startswith("$argon2")
    assert verify_password(payload["password"], user.hashed_password)

    # Verify audit log was written
    audit = db_session.query(AuditLog).filter(AuditLog.user_id == user.id).first()
    assert audit is not None
    assert audit.action == "USER_REGISTERED"


def test_duplicate_registration_fails(client: TestClient):
    payload = {
        "email": "duplicate@example.com",
        "password": "StrongPassword123!",
    }
    resp1 = client.post("/api/v1/auth/register", json=payload)
    assert resp1.status_code == 201

    resp2 = client.post("/api/v1/auth/register", json=payload)
    assert resp2.status_code == 400
    assert "already exists" in resp2.json()["detail"]


def test_user_login_and_token_flow(client: TestClient):
    email = "login.test@example.com"
    password = "CorrectPassword123!"
    client.post("/api/v1/auth/register", json={"email": email, "password": password})

    # Test successful login
    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    assert token_data["token_type"] == "bearer"

    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]

    # Test /auth/me with access token
    headers = {"Authorization": f"Bearer {access_token}"}
    me_resp = client.get("/api/v1/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == email

    # Test token refresh
    refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 200
    new_token = refresh_resp.json()
    assert "access_token" in new_token


def test_invalid_login_credentials(client: TestClient):
    email = "invalid.test@example.com"
    password = "Password123!"
    client.post("/api/v1/auth/register", json={"email": email, "password": password})

    # Wrong password
    bad_pass = client.post("/api/v1/auth/login", json={"email": email, "password": "WrongPassword!"})
    assert bad_pass.status_code == 401

    # Non-existent email
    bad_email = client.post("/api/v1/auth/login", json={"email": "nobody@example.com", "password": password})
    assert bad_email.status_code == 401
