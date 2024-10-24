"""
Main module for handling FastAPI endpoints
and dependencies related to the blockchain.
"""

from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Form, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jose import jwt
import src.security as _security
import templates.pages as pages
import templates.validasi as validasi_tpl
from templates.components import tpl_print
from routes import (
    users,
    juleha,
    blockchain,
    peternak,
    ternak,
    rph,
    penyelia,
    pasar,
    lapak,
    transaksi,
    iot,
)
from src import models, schemas
from src.database import engine
import src.blockchain as bc
from src.database import SessionLocal
from controllers.crud import Crud

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
app.include_router(transaksi.routes)
app.include_router(iot.routes)
app.include_router(blockchain.routes)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/files", StaticFiles(directory="files"), name="files")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/dashboard", response_class=HTMLResponse)
async def index(
    user: Annotated[
        schemas.User, Depends(_security.get_current_user)
    ],
    db=Depends(get_db)
):
    match _security.get_role(user):
        case 0:
            page = pages.dashboard_page(user)
        case 1:
            page = pages.dashboard_page(user)
        case 2:
            validasi = db.query(models.Transaksi).filter(
                models.Transaksi.juleha_id == user.alias,
            ).all()
            table = validasi_tpl.validasi_table(validasi, "validasi_1")
            page = pages.table_page("Validasi Juleha", table, False)
        case 3:
            validasi = db.query(models.Transaksi).filter(
                models.Transaksi.penyelia_id == user.alias,
            ).all()
            table = validasi_tpl.validasi_table(validasi, "validasi_2")
            page = pages.table_page("Validasi Penyelia", table, False)
        case 4:
            transaksi = db.query(
                models.Transaksi, models.Pengiriman
            ).filter(
                models.Pengiriman.transaksi_id == models.Transaksi.id
            ).filter(
                models.Transaksi.lapak_id == user.alias
            ).all()
#            table = validasi_tpl.lapak_table(transaksi, "validasi_2")
#            page = pages.table_page("Validasi Penyelia", table, False)
            page = vars(transaksi[0][1])
        case _:
            page = "Not allowed"

    return str(page)


@app.put("/validasi/{validasi_id}", response_class=HTMLResponse)
def validasi(
    validasi_id: int,
    user=Depends(_security.get_current_user),
    db=Depends(get_db)
):
    validasi_ctrl = Crud(models.Transaksi, db)
    validasi = validasi_ctrl.get_by_id(validasi_id)

    if user.role == 2:
        validasi.validasi_1 = 1
    elif user.role == 3:
        validasi.validasi_2 = 1

    validasi_ctrl.update(validasi)

    return str(validasi_tpl.validated)


@app.get("/login", response_class=HTMLResponse)
def login_get():
    return HTMLResponse(
        str(pages.login_page())
    )


@app.post("/login")
async def login_post(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    _security.check_user(username, password, db)
    token = jwt.encode({"sub": username}, _security.secret_key)
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie("session", token)
    return response


@app.get("/logout", response_class=RedirectResponse)
async def logout():
    response = RedirectResponse("/login")
    response.delete_cookie("session")
    return response


@app.get("/insert")
def insert(
    node=None,
    humi=None,
    temp=None
):
    """
    TODO:
    * Filter node. Do not accept unregistered nodes
    """
    resp = {"node": node, "humi": humi, "temp": temp}
    chain = bc.Blockchain("./data/iot.db")
    chain.mine_block(resp)
    return chain.get_previous_block()


@app.get("/sensorbc")
def sensorbc():
    """
    TODO:
    * Filter node. Do not accept unregistered nodes
    """
    chain = bc.Blockchain("./data/iot.db")
    return chain.chain.items()


@app.get("/qr/{transaksi_id}")
def qr_gen(req: Request, transaksi_id: int):
    root = str(req.base_url)
    img = bc.qr_generator(f"{root}/blockchain/{transaksi_id}")
    return Response(content=img, media_type="image/png")


@app.get("/print/qr/{transaksi_id}", response_class=HTMLResponse)
def qr_print(req: Request, transaksi_id: int):
    return str(tpl_print(f"{req.base_url}qr/{transaksi_id}"))
