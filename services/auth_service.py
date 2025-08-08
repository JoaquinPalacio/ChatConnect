from fastapi import Request, Depends
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from datetime import timedelta
from db.database import get_session
from crud.users import get_user_by_username, create_user
from core.security import verify_password, create_acces_token
from core.templates_env import templates


async def login_user(request: Request, session: Session = Depends(get_session)):
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


async def signup_user(request: Request, session: Session = Depends(get_session)):
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
