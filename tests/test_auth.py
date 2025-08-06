from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)


def test_signup_and_login():
    username = f"usertest_{uuid.uuid4().hex[:8]}"
    password = "pass"
    with TestClient(app) as client:
        # Signup
        res = client.post(
            "/signup",
            data={"name": username, "password": password, "confirmPassword": password},
            follow_redirects=True,
        )
        assert res.status_code == 302 or res.status_code == 200

        # Login
        res = client.post(
            "/login",
            data={"name": username, "password": password},
            follow_redirects=True,
        )
        assert res.status_code == 302 or res.status_code == 200
        assert "access_token" in client.cookies
