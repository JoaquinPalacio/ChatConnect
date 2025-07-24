from fastapi import Request, WebSocket, WebSocketDisconnect, APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime
import json

from utils.connection_manager import ConnectionManager
from utils.crud import get_user_by_username, create_message, get_last_messages
from utils.templates_env import templates
from db.database import get_session
from db.models import Room


manager = ConnectionManager()
router = APIRouter()


@router.get("/")
async def home(request: Request, session: Session = Depends(get_session)):
    user = request.cookies.get("user")
    messages = get_last_messages(session, limit=30, room_id=1)
    return templates.TemplateResponse(
        request, "index.html", {"user": user, "messages": messages}
    )


@router.websocket("/ws/global")
async def websocket_endpoint(
    websocket: WebSocket, session: Session = Depends(get_session)
):
    username = websocket.cookies.get("user", "Anon")
    print(f"User {username} connected")
    room_name = "global"
    room = session.exec(select(Room).where(Room.name == room_name)).first()
    room_id = room.id if room else None
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            now = datetime.now()
            message = {
                "username": username,
                "content": data,
                "timestamp": now.strftime("%H:%M"),
            }
            await manager.broadcast(json.dumps(message))
            user = get_user_by_username(session, username)
            if user:
                create_message(session, content=data, user_id=user.id, room_id=room_id)
            else:
                create_message(session, content=data, user_id=None, room_id=room_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} disconnected")

