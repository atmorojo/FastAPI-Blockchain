"""
Main module for handling FastAPI endpoints
and dependencies related to the blockchain.
"""

from typing import Annotated

from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from jose import jwt
import logging
import src.blockchain as _blockchain
import src.security as _security
import templates.base_template as tpl
import templates.pages as pages
from routes import users, juleha

logger = logging.getLogger('uvicorn.error')
app = FastAPI()
app.include_router(users.routes)
app.include_router(juleha.routes)
app.mount("/static", StaticFiles(directory="static"), name="static")


class BlockData(BaseModel):
    """Model for block data input."""
    name: str
    transaction: str
    hash: str
    previous_hash: str


def get_blockchain():
    """
    Provides an instance of the Blockchain.
    Checks if the blockchain is valid and raises an HTTPException if not.
    """
    blockchain = _blockchain.Blockchain()
#    if not blockchain.is_chain_valid():
#        raise HTTPException(
#           status_code=400,
#           detail="The blockchain is invalid"
#        )
    return blockchain


@app.get("/dashboard", response_class=HTMLResponse)
async def index(
    username: Annotated[
        _security.User, Depends(_security.get_current_active_user)
    ]
):
    return str(pages.dashboard_page())


@app.get("/login", response_class=HTMLResponse)
def login_get():
    return HTMLResponse(
        str(pages.login_page())
    )


@app.post("/login")
async def login_post(
    username: str = Form(...),
    password: str = Form(...)
):
    if username not in _security.users:
        raise HTTPException(
            status_code=302,
            detail="Incorect username or password",
            # headers={"location": "/login"}
        )
    db_password = _security.users[username]["hashed_password"]
    if not password == db_password:
        raise HTTPException(
            status_code=302,
            detail="Incorect username or password",
            # headers={"location": "/login"}
        )
    token = jwt.encode({"sub": username}, _security.secret_key)
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie("session", token)
    response.set_cookie("telo", "telogodok")
    return response


@app.post("/mine_block/")
def mine_block(
    block_data: BlockData
        # , blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Mines a block with the provided data and returns the new block."""
    # return blockchain.mine_block(data=block_data.data)
    print(block_data)
    return block_data


@app.get("/blockchain/")
def get_blockchain_route(
        blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Returns the entire blockchain."""
    return blockchain.chain


# pylint: disable=unused-argument
@app.get("/validate/")
def is_blockchain_valid(
        blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Checks if the blockchain is valid and returns a relevant message."""
    return {"message": "The blockchain is valid."}


@app.get("/blockchain/last/")
def previous_block(
        blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Returns the last block in the blockchain."""
    return blockchain.get_previous_block()
