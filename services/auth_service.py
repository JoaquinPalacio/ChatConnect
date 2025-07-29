from fastapi import Request, Depends, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from datetime import timedelta
from db.database import get_session
from crud.users import get_user_by_username
from crud.users import create_user
from core.security import verify_password
from services.user_access import create_acces_token
from core.templates_env import templates


async def login_post(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    username = str(form.get("name"))
    password = str(form.get("password"))
    user = get_user_by_username(session, username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            request,
            "auth/login.html",
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


async def signup_post(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    username = str(form.get("name"))
    password = str(form.get("password"))
    confirm_password = form.get("confirmPassword")
    if password != confirm_password:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {"error": "Passwords do not match"},
            status_code=400,
        )
    db_user = get_user_by_username(session, username)
    if db_user:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
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


async def logout_get(request: Request):
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")

    for key in request.cookies:
        if key.startswith("room_") and key.endswith("_access"):
            response.delete_cookie(key)

    return response
