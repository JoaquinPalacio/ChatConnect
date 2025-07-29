from datetime import datetime
import json
from core.connection_manager import ConnectionManager
from crud.users import get_user_by_username
from crud.chat import create_message
from models.room import Room
from sqlmodel import Session, select
from fastapi import WebSocket, WebSocketDisconnect

manager = ConnectionManager()


def get_room_id_by_name(session: Session, room_name: str) -> int | None:
    room = session.exec(select(Room).where(Room.name == room_name)).first()
    return room.id if room else None


async def handle_global_chat(websocket: WebSocket, username: str, session: Session):
    room_id = get_room_id_by_name(session, "global")
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            timestamp = datetime.now().strftime("%H:%M")
            message = {"username": username, "content": data, "timestamp": timestamp}
            await manager.broadcast(json.dumps(message))
            user = get_user_by_username(session, username)
            create_message(
                session,
                content=data,
                user_id=user.id if user else None,
                room_id=room_id,
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} disconnected")


async def handle_room_chat(
    websocket: WebSocket, room_id: int, username: str, session: Session
):
    await manager.connect(websocket, f"{room_id}:{username}")
    try:
        while True:
            data = await websocket.receive_text()
            timestamp = datetime.now().strftime("%H:%M")
            message = {"username": username, "content": data, "timestamp": timestamp}
            await manager.broadcast(json.dumps(message))
            user = get_user_by_username(session, username)
            create_message(
                session,
                content=data,
                user_id=user.id if user else None,
                room_id=room_id,
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
