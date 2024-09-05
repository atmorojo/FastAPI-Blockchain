from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from jose import jwt
from pydantic import BaseModel
from src.database import SessionLocal, engine
from controllers import user_ctrl

cookie_sec = APIKeyCookie(name="session")
secret_key = "ladadidadadida"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(BaseModel):
    username: str
    email: str | None = None
    role: str | None = None
    is_active: bool | None = None


class UserInDB(User):
    hashed_password: str


def check_user(username: str, password: str):
    user = user_ctrl.get_user_by_username(next(get_db()), username)
    if user is None:
        raise HTTPException(
            status_code=302,
            detail="Incorect username or password",
            # headers={"location": "/login"}
        )
    if not password == user.hashed_password:
        raise HTTPException(
            status_code=302,
            detail="Incorect username or password",
            # headers={"location": "/login"}
        )


async def get_current_user(
    session: Annotated[str, Depends(cookie_sec)]
):
    try:
        payload = jwt.decode(session, secret_key)
        print(payload["sub"])
        user = user_ctrl.get_user_by_username(next(get_db()), payload["sub"])
        return user
    except Exception:
        raise HTTPException(
            status_code=302,
            detail="Invalid authentication credentials",
            # headers={"location": "/login"},
        )


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.is_active:
        return current_user
    else:
        raise HTTPException(
            status_code=302,
            detail="Inactive user",
            # headers={"location": "/login"}
        )
