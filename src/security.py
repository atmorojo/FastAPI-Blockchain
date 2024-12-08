import hashlib
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from jose import jwt
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from controllers.user_ctrl import UserCrud
from src import schemas

cookie_sec = APIKeyCookie(name="session", auto_error=False)
secret_key = "ladadidadadida"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_user(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    user_ctrl = UserCrud(db)
    db_user = user_ctrl.get_user_by_username(username=username)
    if db_user is None:
        raise HTTPException(
            status_code=302,
            detail="Incorect username or password",
            # headers={"location": "/login"}
        )
    hashed_password = hash_password(password)
    if not hashed_password == db_user.password:
        raise HTTPException(
            status_code=302,
            detail="Incorect username or password",
            # headers={"location": "/login"}
        )


async def get_current_user(
    session: Annotated[str, Depends(cookie_sec)],
    db: Session = Depends(get_db),
):
    if session:
        user_ctrl = UserCrud(db)
        payload = jwt.decode(session, secret_key)
        user = user_ctrl.get_user_by_username(payload["sub"])
        if user:
            return user

    return False


def current_user_validation(user, password):
    hashed_password = hash_password(password)
    print(hashed_password == user.password)
    return hashed_password == user.password


def is_admin(user=Depends(get_current_user)):
    if get_role(user) == 1:
        return user
    else:
        return False


def is_super_admin(user=Depends(get_current_user)):
    if get_role(user) == 0:
        return user
    else:
        return False


def get_role(user):
    if not user:
        return False
    return user.role.role


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
