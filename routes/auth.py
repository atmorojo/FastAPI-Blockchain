from typing import Annotated
from fastapi import APIRouter, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from jose import jwt

from src import models, security, schemas
from sqlalchemy.orm import Session
from src.database import engine, get_db

import templates.pages as pages

models.Base.metadata.create_all(bind=engine)

routes = APIRouter()


@routes.get("/login", response_class=HTMLResponse)
def login_get(
    user: Annotated[schemas.User, Depends(security.get_current_user)],
):
    if not user:
        return HTMLResponse(str(pages.login_page()))
    else:
        return RedirectResponse("/dashboard", status_code=302)


@routes.post("/login")
async def login_post(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    security.check_user(username, password, db)
    token = jwt.encode({"sub": username}, security.secret_key)
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie("session", token)
    return response


@routes.get("/logout", response_class=RedirectResponse)
async def logout():
    response = RedirectResponse("/login")
    response.delete_cookie("session")
    return response
