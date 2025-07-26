from fastapi import FastAPI
from db.database import engine, get_session
from sqlmodel import SQLModel, select
from contextlib import asynccontextmanager
from db.models.room import Room
from routes import auth, chat, rooms


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
