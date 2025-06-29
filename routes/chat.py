from fastapi import Request, WebSocket, WebSocketDisconnect, APIRouter

from utils.connection_manager import ConnectionManager
from utils.templates_env import templates


manager = ConnectionManager()
router = APIRouter()


@router.get("/")
async def home(request: Request):
    user = request.cookies.get("user")
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@router.websocket("/ws")
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
