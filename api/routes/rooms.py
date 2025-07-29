from fastapi import APIRouter, Request, Depends
from sqlmodel import Session
from db.database import get_session
from core.connection_manager import ConnectionManager
from services.room_service import (
    rooms_get,
    room_id_get,
    room_password_post,
    create_room_get,
    room_post,
)

manager = ConnectionManager()
router = APIRouter()


@router.get("/rooms")
async def rooms(request: Request, session: Session = Depends(get_session)):
    return await rooms_get(request, session)


@router.get("/rooms/{room_id}")
async def room_id(
    request: Request, room_id: int, session: Session = Depends(get_session)
):
    return await room_id_get(request, room_id, session)


@router.post("/rooms/{room_id}/password")
async def room_password(
    request: Request, room_id: int, session: Session = Depends(get_session)
):
    return await room_password_post(request, room_id, session)


@router.get("/create_room")
async def rooms_create(request: Request, session: Session = Depends(get_session)):
    return await create_room_get(request, session)


@router.post("/create_room")
async def rooms_create_post(request: Request, session: Session = Depends(get_session)):
    return await room_post(request, session)
