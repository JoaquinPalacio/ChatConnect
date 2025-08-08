from fastapi import APIRouter, Request, Depends, Query
from sqlmodel import Session
from db.database import get_session
from core.connection_manager import ConnectionManager
from services.room_service import (
    access_room_by_id,
    access_private_room,
    room_post,
    require_ajax,
)
from crud.rooms import search_rooms
from crud.users import get_current_user
from models.user import User
from core.templates_env import templates

manager = ConnectionManager()
router = APIRouter()


@router.get("/rooms")
async def rooms_get(
    request: Request,
    q: str | None = Query(None, description="Search query for room names"),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    rooms = await search_rooms(session, q)
    return templates.TemplateResponse(
        "rooms/rooms.html",
        {
            "request": request,
            "user": user.username if user else None,
            "rooms": rooms,
            "q": q,
        },
    )


@router.get("/api/rooms")
async def api_rooms(
    q: str | None = Query(None),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
    _: None = Depends(require_ajax),
):
    rooms = await search_rooms(session, q)
    return [{"id": room.id, "name": room.name} for room in rooms]


@router.get("/rooms/{room_id:int}")
async def room_id_get(
    request: Request,
    room_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return await access_room_by_id(request, user, room_id, session)


@router.post("/rooms/{room_id:int}/password")
async def room_password_post(
    request: Request,
    room_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return await access_private_room(request, user, room_id, session)


@router.get("/rooms/create")
async def rooms_create_get(
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "rooms/create_room.html",
        {"request": request, "user": user.username if user else None},
    )


@router.post("/rooms/create")
async def rooms_create_post(
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return await room_post(request, user, session)
