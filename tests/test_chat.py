from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_websocket_broadcast():
    with (
        client.websocket_connect("/ws") as client1,
        client.websocket_connect("/ws") as client2,
    ):
        client1.send_text("Mensaje de prueba")
        data = client2.receive_text()
        assert "Mensaje de prueba" in data
