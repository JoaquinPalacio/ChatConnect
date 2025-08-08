from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from db.database import get_session
from core.templates_env import templates
from services.auth_service import login_user, signup_user

router = APIRouter()


@router.get("/login")
async def login_get(request: Request):
    if request.cookies.get("access_token"):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(request, "auth/login.html")


@router.post("/login")
async def login_post(request: Request, session: Session = Depends(get_session)):
    if request.cookies.get("access_token"):
        return RedirectResponse(url="/", status_code=302)
    return await login_user(request, session)


@router.post("/signup")
async def signup_post(request: Request, session: Session = Depends(get_session)):
    if request.cookies.get("access_token"):
        return RedirectResponse(url="/", status_code=302)
    return await signup_user(request, session)


@router.get("/logout")
async def logout_get(request: Request):
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token", path="/")

    for key in request.cookies:
        if key.startswith("room_") and key.endswith("_access"):
            response.delete_cookie(key, path="/")

    return response
