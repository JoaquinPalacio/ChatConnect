from fastapi import Request, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from models.user import User
from db.database import get_session
from crud.rooms import create_room, get_room_by_id, get_room_id_by_name
from crud.chat import get_last_30_messages
from core.templates_env import templates
from core.security import (
    verify_password,
    verify_room_access_token,
    make_room_access_token_response,
)


async def access_room_by_id(
    request: Request, user: User, room_id: int, session: Session = Depends(get_session)
):
    room = get_room_by_id(session, room_id)
    if room is None:
        return room_not_found(request, user)

    if room.is_private:
        token = request.cookies.get(f"room_{room_id}_access")
        if not token or not verify_room_access_token(
            token, room_id, user.username if user else "Anon"
        ):
            if user and user.id == room.owner_id:
                return make_room_access_token_response(
                    room_id, user.username, f"/rooms/{room_id}"
                )
            return templates.TemplateResponse(
                "rooms/room_password.html",
                {
                    "request": request,
                    "user": user.username if user else None,
                    "room": room,
                },
            )

    messages = get_last_30_messages(session, limit=30, room_id=room_id)
    return templates.TemplateResponse(
        "rooms/room_id.html",
        {
            "request": request,
            "user": user.username if user else None,
            "room": room,
            "messages": messages,
        },
    )


async def access_private_room(
    request: Request, user: User, room_id: int, session: Session = Depends(get_session)
):
    room = get_room_by_id(session, room_id)
    if room is None:
        return room_not_found(request, user)

    form = await request.form()
    password = str(form.get("password"))
    if room.hashed_password and verify_password(password, room.hashed_password):
        return make_room_access_token_response(
            room_id, user.username if user else "Anon", f"/rooms/{room_id}"
        )

    return templates.TemplateResponse(
        "rooms/room_password.html",
        {
            "request": request,
            "user": user.username if user else None,
            "room": room,
            "error": "Invalid password",
        },
    )


async def room_post(
    request: Request, user: User, session: Session = Depends(get_session)
):
    form = await request.form()
    if user is None:
        return RedirectResponse(url="/login", status_code=302)

    name = str(form.get("name"))
    is_private = (
        form.get("isPrivate") == "on" if form.get("isPrivate") is not None else False
    )
    password = str(form.get("password")) if is_private else None

    existing_room_id = get_room_id_by_name(session, name)

    if existing_room_id is not None:
        return templates.TemplateResponse(
            "rooms/create_room.html",
            {
                "request": request,
                "user": user.username,
                "error": "Room name already exists",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    room = create_room(session, name, user.id, is_private, password)

    if room.is_private:
        assert room.id is not None
        return make_room_access_token_response(
            room.id, user.username, f"/rooms/{room.id}"
        )

    messages = get_last_30_messages(session, limit=30, room_id=room.id)
    return templates.TemplateResponse(
        "rooms/room_id.html",
        {
            "request": request,
            "user": user.username,
            "room": room,
            "messages": messages,
        },
    )


def room_not_found(request: Request, user):
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "user": user.username if user else None},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def require_ajax(request: Request):
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
