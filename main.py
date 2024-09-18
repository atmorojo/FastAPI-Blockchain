"""
Main module for handling FastAPI endpoints
and dependencies related to the blockchain.
"""

from typing import Annotated

from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jose import jwt
import src.security as _security
import templates.pages as pages
from routes import (
    users,
    juleha,
    blockchain,
    peternak,
    ternak,
    rph,
    penyelia,
    pasar,
    transportasi,
    lapak,
    transaksi,
    iot,
)
from src import models
from src.database import engine
import src.blockchain as bc

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.routes)
app.include_router(juleha.routes)
app.include_router(peternak.routes)
app.include_router(rph.routes)
app.include_router(ternak.routes)
app.include_router(penyelia.routes)
app.include_router(pasar.routes)
app.include_router(lapak.routes)
app.include_router(transportasi.routes)
app.include_router(transaksi.routes)
app.include_router(iot.routes)
app.include_router(blockchain.routes)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/files", StaticFiles(directory="files"), name="files")


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
    _security.check_user(username, password)
    token = jwt.encode({"sub": username}, _security.secret_key)
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie("session", token)
    return response


@app.get("/insert")
def insert(
    node: str = None,
    humi=None,
    temp=None
):
    resp = {"node": node, "humi": humi, "temp": temp}
    chain = bc.Blockchain("./data/iot.db")
    chain.mine_block(resp)
    return chain.get_previous_block()
