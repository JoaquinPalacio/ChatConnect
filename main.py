from fastapi import FastAPI, Request, status
from sqlmodel import SQLModel, select
from contextlib import asynccontextmanager
from api import auth, chat, rooms
from db.database import engine, get_session
from models.room import Room
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.security import access_not_auth
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    session = next(get_session())
    try:
        room = session.exec(select(Room).where(Room.name == "global")).first()
        if not room:
            public_room = Room(name="global", is_private=False, owner_id=None)
            session.add(public_room)
            session.commit()
        yield
    finally:
        session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(rooms.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return access_not_auth(request)
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
