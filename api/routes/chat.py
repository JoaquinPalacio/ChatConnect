from fastapi import Request, WebSocket, APIRouter, Depends
from sqlmodel import Session

from core.connection_manager import ConnectionManager
from crud.users import (
    get_username_from_cookies,
    get_username_from_request,
)
from crud.chat import get_last_30_messages
from core.templates_env import templates
from db.database import get_session
from services.chat_service import handle_global_chat, handle_room_chat


manager = ConnectionManager()
router = APIRouter()


@router.get("/")
async def home(request: Request, session: Session = Depends(get_session)):
    user = get_username_from_request(request)
    messages = get_last_30_messages(session, limit=30, room_id=1)
    return templates.TemplateResponse(
        request, "index.html", {"user": user, "messages": messages}
    )


@router.websocket("/ws/global")
async def websocket_endpoint(
    websocket: WebSocket, session: Session = Depends(get_session)
):
    username = get_username_from_cookies(websocket.cookies)
    await handle_global_chat(websocket, username, session)


@router.websocket("/ws/{room_id}")
async def websocket_room(
    websocket: WebSocket, room_id: int, session: Session = Depends(get_session)
):
    username = get_username_from_cookies(websocket.cookies)
    await handle_room_chat(websocket, room_id, username, session)
