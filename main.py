from fastapi import (
    FastAPI,
    Request,
    WebSocket,
    WebSocketDisconnect,
    status,
    HTTPException,
    Depends,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from db import engine, get_session
from utils import verify_password, create_acces_token
from sqlmodel import SQLModel
from typing import Dict
from contextlib import asynccontextmanager
from crud import get_user_by_username, create_user
from schemas import UserCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[websocket] = username

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            del self.active_connections[websocket]

    async def broadcast(self, message: str):
        for connection in self.active_connections.keys():
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def home(request: Request):
    user = request.cookies.get("user")
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    username = websocket.cookies.get("user", "Anon")
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} disconnected")


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login_post(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    username = form.get("name")
    password = form.get("password")
    user = get_user_by_username(session, username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"},
            status_code=401,
        )
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="user", value=username, httponly=True)
    return response


@app.post("/signup")
async def signup_post(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    username = form.get("name")
    password = form.get("password")
    confirm_password = form.get("confirmPassword")
    if password != confirm_password:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Passwords do not match"},
            status_code=400,
        )
    db_user = get_user_by_username(session, username)
    if db_user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Username already registered"},
            status_code=400,
        )
    create_user(session, username, password)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="user", value=username, httponly=True)
    return response


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="user")
    return response
