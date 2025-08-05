from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_websocket_broadcast_global():
    with (
        client.websocket_connect("/ws/global") as client1,
        client.websocket_connect("/ws/global") as client2,
    ):
        client1.send_text("Mensaje de prueba")
        data = client2.receive_text()
        assert "Mensaje de prueba" in data


def test_websocket_broadcast_specific_room():
    with (
        client.websocket_connect("/ws/1") as client1,
        client.websocket_connect("/ws/1") as client2,
    ):
        client1.send_text("Mensaje de sala de prueba")
        data = client2.receive_text()
        assert "Mensaje de sala de prueba" in data
