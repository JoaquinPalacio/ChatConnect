from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_signup_and_login():
    with TestClient(app) as client:
        # Signup
        res = client.post(
            "/signup",
            data={"name": "testuser1", "password": "pass", "confirmPassword": "pass"},
            follow_redirects=False,
        )
        assert res.status_code == 302

        # Login
        res = client.post(
            "/login",
            data={"name": "testuser", "password": "pass"},
            follow_redirects=False,
        )
        assert res.status_code == 302
        assert "set-cookie" in res.headers
