"""
Main module for handling FastAPI endpoints
and dependencies related to the blockchain.
"""

from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import json
import src.security as _security
import templates.pages as pages
import templates.validasi as validasi_tpl
import templates.blockchain as bc_tpl
from templates.components import tpl_print
from datetime import datetime as dt
from zoneinfo import ZoneInfo
from routes import (
    report,
    auth,
    blockchain,
    iot,
    juleha,
    lapak,
    pasar,
    penyelia,
    peternak,
    rph,
    ternak,
    transaksi,
    users,
)
from src import models, schemas
from src.database import engine
import src.blockchain as bc
from src.database import SessionLocal, get_db
from controllers.crud import Crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.routes)
app.include_router(users.routes)
app.include_router(juleha.routes)
app.include_router(peternak.routes)
app.include_router(rph.routes)
app.include_router(report.routes)
app.include_router(ternak.routes)
app.include_router(penyelia.routes)
app.include_router(pasar.routes)
app.include_router(lapak.routes)
app.include_router(transaksi.routes)
app.include_router(iot.routes)
app.include_router(blockchain.routes)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/files", StaticFiles(directory="files"), name="files")


@app.get("/", response_class=HTMLResponse)
def landing():
    landing_file = Path("static/index.html").read_text()
    return landing_file


@app.get("/dashboard", response_class=HTMLResponse)
async def index(
    user: Annotated[schemas.User, Depends(_security.get_current_user)],
    db=Depends(get_db),
):
    today = dt.now().strftime("%Y-%m-%d")
    if not user:
        return RedirectResponse("/login")

    match _security.get_role(user):
        case 0:
            page = pages.dashboard_page(role=_security.get_role(user), user=user)
        case 1:
            page = pages.dashboard_page(role=_security.get_role(user), user=user)
        case 2:
            validasi = (
                db.query(models.Ternak)
                .filter(models.Ternak.waktu_sembelih == today)
                .filter(
                    models.Ternak.penyelia_id == user.role.acting_as,
                )
                .all()
            )
            table = validasi_tpl.validasi_table(validasi, "validasi_1")
            page = pages.table_page(
                title="Validasi Penyelia", datatable=table, button=False, role=user.role.role
            )
        case 3:
            validasi = (
                db.query(models.Ternak)
                .filter(models.Ternak.waktu_sembelih == today)
                .filter(
                    models.Ternak.juleha_id == user.role.acting_as,
                )
                .all()
            )
            table = validasi_tpl.validasi_table(validasi, "validasi_2")
            page = pages.table_page(
                title="Validasi Juleha", datatable=table, button=False, role=user.role.role
            )
        case 4:
            transaksi = (
                db.query(models.Transaksi)
                .filter(models.Transaksi.lapak_id == user.role.acting_as)
                .all()
            )
            table = bc_tpl.kiriman_table(transaksi)
            page = pages.table_page("Konfirmasi pengiriman", table, False, False)
        case _:
            page = "Not allowed"

    return str(page)


@app.get("/403", response_class=HTMLResponse)
def not_authorized():
    not_authorized_page = Path("static/403.html").read_text()
    return not_authorized_page


@app.get("/404", response_class=HTMLResponse)
def not_found():
    not_found_page = Path("static/404.html").read_text()
    return not_found_page


@app.put("/validasi/{validasi_id}", response_class=HTMLResponse)
def validasi(
    validasi_id: int, user=Depends(_security.get_current_user), db=Depends(get_db)
):
    validasi_ctrl = Crud(models.Ternak, db)
    transaksi_ctrl = Crud(models.Transaksi, db)
    validasi = validasi_ctrl.get_by_id(validasi_id)

    if user.role.role == 2:
        validasi.validasi_1 = 1
    elif user.role.role == 3:
        validasi.validasi_2 = 1

    validasi_ctrl.update(validasi)

    if validasi.validasi_1 == validasi.validasi_2 == 1:
        transaksi = transaksi_ctrl.get_by("ternak_id", validasi_id)
        _bc = bc.Blockchain()
        block = json.loads(_bc.get_by_transaction(transaksi.id)[0])
        block["status_validasi"] = "Tervalidasi Halal"
        print(block)
        _bc.mine_block(block)

    return str(validasi_tpl.validated)


@app.get("/insert")
def insert(node=None, humi=None, temp=None):
    """
    TODO:
    * Filter node. Do not accept unregistered nodes
    """
    resp = {"node": node, "humi": humi, "temp": temp}
    chain = bc.Blockchain("./data/iot.db")
    chain.mine_block(resp)
    return chain.get_previous_block()


@app.get("/sensor/end/{transaksi_id}")
def end_sensor(
    transaksi_id: int,
    db=Depends(get_db),
):
    trans_db = Crud(models.Transaksi, db)
    trans = trans_db.get_by_id(transaksi_id)
    iot_chain = bc.Blockchain("./data/iot.db")
    trans_chain = bc.Blockchain()
    if not trans:
        return "Not found"
    csa = iot_chain.end_delivery(trans.iot.node, trans.waktu_kirim.replace("T", " "))
    trans_block = json.loads(trans_chain.get_by_transaction(trans.id)[0])
    trans_block["waktu_selesai_kirim"] = dt.now(ZoneInfo("Asia/Jakarta")).strftime(
        "%Y-%m-%dT%H:%M"
    )
    trans_block["temp_min"] = csa[0][0]
    trans_block["temp_max"] = csa[0][1]
    trans_block["humi_min"] = csa[1][0]
    trans_block["humi_max"] = csa[1][1]
    trans_chain.mine_block(trans_block)
    trans.waktu_selesai_kirim = trans_block["waktu_selesai_kirim"]
    trans_db.update(trans)
    return {"success": "success"}


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
    img = bc.qr_generator(f"{root}blockchain/{transaksi_id}")
    return Response(content=img, media_type="image/png")


@app.get("/print/qr/{transaksi_id}", response_class=HTMLResponse)
def qr_print(req: Request, transaksi_id: int):
    return str(tpl_print(f"{req.base_url}qr/{transaksi_id}"))
