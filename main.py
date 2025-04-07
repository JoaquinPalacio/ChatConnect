from fastapi import (
    FastAPI,
    Request,
    WebSocket,
    WebSocketDisconnect,
    Form,
    status,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from models import User
from db import engine
from utils import verify_password, get_password_hash
from typing import Dict

app = FastAPI()
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
async def login_post(
    request: Request, name: str = Form(...), password: str = Form(...)
):
    with Session(engine) as session:
        statement = select(User).where(User.name == name)
        user = session.exec(statement).first()
        if not user or not verify_password(password, user.password):
            return templates.TemplateResponse(
                "login.html", {"request": request, "error": "Credenciales inválidas"}
            )
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user", value=name)
    return response


@app.get("/signup")
async def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup")
async def signup_post(
    request: Request,
    name: str = Form(...),
    password: str = Form(...),
    confirmPassword: str = Form(...),
):
    if password != confirmPassword:
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Las contraseñas no coinciden"}
        )
    hashed_password = get_password_hash(password)
    user = User(name=name, password=hashed_password)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
