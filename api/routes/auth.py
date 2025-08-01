from fastapi import APIRouter, Request, Depends
from sqlmodel import Session
from db.database import get_session
from core.templates_env import templates
from services.auth_service import login_post, signup_post, logout_get

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(request, "auth/login.html")


@router.post("/login")
async def login_user(request: Request, session: Session = Depends(get_session)):
    return await login_post(request, session)


@router.post("/signup")
async def signup(request: Request, session: Session = Depends(get_session)):
    return await signup_post(request, session)


@router.get("/logout")
async def logout(request: Request):
    return await logout_get(request)
