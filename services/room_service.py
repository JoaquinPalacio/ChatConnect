from fastapi import Request, Depends, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from db.database import get_session
from models.room import Room
from crud.rooms import create_room
from services.room_access import verify_room_access_token, create_room_access_token
from crud.users import (
    get_user_by_username,
    get_username_from_request,
)
from crud.chat import get_last_30_messages
from core.templates_env import templates
from core.security import verify_password


async def rooms_get(request: Request, session: Session = Depends(get_session)):
    user = get_user_by_username(session, str(get_username_from_request(request)))
    rooms = session.exec(select(Room)).all()
    return templates.TemplateResponse(
        "rooms/rooms.html",
        {"request": request, "user": user.username if user else None, "rooms": rooms},
    )


async def room_id_get(
    request: Request, room_id: int, session: Session = Depends(get_session)
):
    user = get_user_by_username(session, str(get_username_from_request(request)))
    room = session.get(Room, room_id)
    messages = get_last_30_messages(session, limit=30, room_id=room_id)
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
            if user and user.id == room.owner_id:
                room_token = create_room_access_token(room_id, user.username)
                response = RedirectResponse(url=f"/rooms/{room_id}", status_code=302)
                response.set_cookie(
                    key=f"room_{room_id}_access",
                    value=room_token,
                    httponly=True,
                    max_age=60 * 30,
                    samesite="lax",
                )
                return response
            return templates.TemplateResponse(
                "rooms/room_password.html",
                {
                    "request": request,
                    "user": user.username if user else None,
                    "room": room,
                },
            )
    return templates.TemplateResponse(
        "rooms/room_id.html",
        {
            "request": request,
            "user": user.username if user else None,
            "room": room,
            "messages": messages,
        },
    )


async def room_password_post(
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
        "rooms/room_password.html",
        {
            "request": request,
            "user": user.username if user else None,
            "room": room,
            "error": "Invalid password",
        },
    )


async def create_room_get(request: Request, session: Session = Depends(get_session)):
    user = get_user_by_username(session, str(get_username_from_request(request)))
    return templates.TemplateResponse(
        "rooms/create_room.html",
        {"request": request, "user": user.username if user else None},
    )


async def room_post(request: Request, session: Session = Depends(get_session)):
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
