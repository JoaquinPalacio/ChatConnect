from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from datetime import timedelta
from db.database import get_session
from utils.crud import get_user_by_username, create_user
from utils.security import verify_password, create_acces_token
from utils.templates_env import templates


router = APIRouter()


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.post("/login")
async def login_post(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    username = str(form.get("name"))
    password = str(form.get("password"))
    user = get_user_by_username(session, username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Invalid credentials"},
            status_code=401,
        )
    access_token = create_acces_token(
        data={"sub": user.username}, expires_delta=timedelta(hours=2)
    )
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=7200,
        samesite="lax",
    )
    return response


@router.post("/signup")
async def signup_post(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    username = str(form.get("name"))
    password = str(form.get("password"))
    confirm_password = form.get("confirmPassword")
    if password != confirm_password:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Passwords do not match"},
            status_code=400,
        )
    db_user = get_user_by_username(session, username)
    if db_user:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Username already registered"},
            status_code=400,
        )
    create_user(session, username, password)
    response = RedirectResponse(url="/", status_code=302)
    access_token = create_acces_token(
        data={"sub": username}, expires_delta=timedelta(hours=2)
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=7200,
        samesite="lax",
    )
    return response


@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")

    for key in request.cookies:
        if key.startswith("room_") and key.endswith("_access"):
            response.delete_cookie(key)

    return response
