from fastapi import FastAPI
from db.database import engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from routes import auth, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(chat.router)
