from fastapi import APIRouter, Request, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from datetime import datetime
import json

from db.database import get_session
from db.models.room import Room
from utils.crud import (
    get_user_by_username,
    create_room,
    create_message,
    get_last_messages,
    get_username_from_request,
    get_username_from_cookies,
    verify_room_access_token,
)
from utils.templates_env import templates
from utils.security import verify_password, create_room_access_token
from utils.connection_manager import ConnectionManager


manager = ConnectionManager()
router = APIRouter()


@router.get("/rooms")
async def rooms(request: Request, session: Session = Depends(get_session)):
    user = get_user_by_username(session, str(get_username_from_request(request)))
    rooms = session.exec(select(Room)).all()
    return templates.TemplateResponse(
        "rooms.html",
        {"request": request, "user": user.username if user else None, "rooms": rooms},
    )


@router.get("/rooms/{room_id}")
async def room_id(
    request: Request, room_id: int, session: Session = Depends(get_session)
):
    user = get_user_by_username(session, str(get_username_from_request(request)))
    room = session.get(Room, room_id)
    messages = get_last_messages(session, limit=30, room_id=room_id)
    if room is None:
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "user": user.username if user else None},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if room.is_private:
        token = request.cookies.get(f"room_{room_id}_access")
        if not token or not verify_room_access_token(
            token, room_id, user.username if user else "Anon"
        ):
            return templates.TemplateResponse(
                "room_password.html",
                {
                    "request": request,
                    "user": user.username if user else None,
                    "room": room,
                },
            )
    return templates.TemplateResponse(
        "room_id.html",
        {
            "request": request,
            "user": user.username if user else None,
            "room": room,
            "messages": messages,
        },
    )


@router.post("/rooms/{room_id}/password")
async def room_password(
    request: Request, room_id: int, session: Session = Depends(get_session)
):
    user = get_user_by_username(session, str(get_username_from_request(request)))
    room = session.get(Room, room_id)
    if room is None:
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "user": user.username if user else None},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    form = await request.form()
    password = str(form.get("password"))
    if room.hashed_password and verify_password(password, room.hashed_password):
        response = RedirectResponse(url=f"/rooms/{room_id}", status_code=302)
        token = create_room_access_token(room_id, user.username if user else "Anon")
        response.set_cookie(
            key=f"room_{room_id}_access",
            value=token,
            httponly=True,
            max_age=60 * 30,
            samesite="lax",
        )
        return response
    return templates.TemplateResponse(
        "room_password.html",
        {
            "request": request,
            "user": user.username if user else None,
            "room": room,
            "error": "Invalid password",
        },
    )


@router.websocket("/ws/{room_id}")
async def websocket_room(
    websocket: WebSocket, room_id: int, session: Session = Depends(get_session)
):
    username = get_username_from_cookies(websocket.cookies)
    await manager.connect(websocket, f"{room_id}:{username}")
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


@router.get("/create_room")
async def rooms_create(request: Request, session: Session = Depends(get_session)):
    user = get_user_by_username(session, str(get_username_from_request(request)))
    return templates.TemplateResponse(
        "create_room.html",
        {"request": request, "user": user.username if user else None},
    )


@router.post("/create_room")
async def rooms_create_post(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    user = get_user_by_username(session, str(get_username_from_request(request)))
    if user is None:
        response = RedirectResponse(url="/login", status_code=302)
        return response
    name = str(form.get("name"))
    is_private = (
        form.get("isPrivate") == "on" if form.get("isPrivate") is not None else False
    )
    password = str(form.get("password")) if is_private else None
    create_room(session, name, user.id, is_private, password)
    response = RedirectResponse(url="/rooms/", status_code=302)
    return response
