from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from jose import jwt
from pydantic import BaseModel

cookie_sec = APIKeyCookie(name="session")
secret_key = "ladadidadadida"

users = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_current_user(
    session: Annotated[str, Depends(cookie_sec)]
):
    try:
        payload = jwt.decode(session, secret_key)
        user = users[payload["sub"]]
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
    if (current_user["disabled"] is False):
        return current_user
    else:
        raise HTTPException(
            status_code=302,
            detail="Inactive user",
            headers={"location": "/login"}
        )
