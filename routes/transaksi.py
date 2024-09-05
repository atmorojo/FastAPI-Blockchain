from fastapi import (
    APIRouter, HTTPException, Form, Request
)
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import templates.pages as pages
import templates.transaksi as transaksi_view

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/transaksi"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


transaksi_db = Crud(models.Transaksi, next(get_db()))


@routes.get("/new", response_class=HTMLResponse)
def new_transaksi():
    transportasi = Crud(models.Transportasi, next(get_db())).get()
    lapak = Crud(models.Lapak, next(get_db())).get()
    penyelia = Crud(models.Penyelia, next(get_db())).get()
    juleha = Crud(models.Juleha, next(get_db())).get()
    ternak = Crud(models.Ternak, next(get_db())).get()
    return str(pages.detail_page(
        "Transaksi",
        transaksi_view.transaksi_form(
            transportasi=transportasi,
            lapak=lapak,
            penyelia=penyelia,
            juleha=juleha,
            ternak=ternak,
        )
    ))


@routes.post("/")
async def create_transaksi(
    jumlah: str = Form(...),
    lapak_id: int = Form(...),
    transportasi_id: int = Form(...),
    penyelia_id: int = Form(...),
    juleha_id: int = Form(...),
    ternak_id: int = Form(...),
):
    transaksi = models.Transaksi(
        jumlah=jumlah,
        lapak_id=lapak_id,
        transportasi_id=transportasi_id,
        penyelia_id=penyelia_id,
        juleha_id=juleha_id,
        ternak_id=ternak_id,
    )
    transaksi_db.create(transaksi)
    return RedirectResponse("/transaksi", status_code=302)


# Read


@routes.get("/", response_class=HTMLResponse)
def read_transaksis(skip: int = 0, limit: int = 100):
    transaksis = transaksi_db.get(skip=skip, limit=limit)
    return str(pages.table_page(
        "Transaksi",
        transaksi_view.transaksis_table(transaksis)
    ))


@routes.get("/{transaksi_id}", response_class=HTMLResponse)
def read_transaksi(transaksi_id: int):
    lock = True
    transaksi = transaksi_db.get_by_id(transaksi_id)
    if transaksi is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.detail_page(
        "transaksi",
        transaksi_view.transaksi_form(transaksi=transaksi, lock=lock)
    ))


# Update


@routes.get("/edit/{transaksi_id}", response_class=HTMLResponse)
def edit_transaksi(req: Request, transaksi_id: int):
    transaksi = transaksi_db.get_by_id(transaksi_id)
    transportasi = Crud(models.Transportasi, next(get_db())).get()
    lapak = Crud(models.Lapak, next(get_db())).get()
    penyelia = Crud(models.Penyelia, next(get_db())).get()
    juleha = Crud(models.Juleha, next(get_db())).get()
    ternak = Crud(models.Ternak, next(get_db())).get()
    if transaksi is None:
        raise HTTPException(status_code=404, detail="User not found")

    form = transaksi_view.transaksi_form(
        transaksi=transaksi,
        transportasi=transportasi,
        lapak=lapak,
        penyelia=penyelia,
        juleha=juleha,
        ternak=ternak,
    )
    if req.headers.get('HX-Request'):
        return str(form)
    else:
        return str(pages.detail_page("Transaksi", form))


@routes.put("/{transaksi_id}", response_class=HTMLResponse)
async def update_transaksi(
    transaksi_id: int,
    jumlah: str = Form(...),
    lapak_id: int = Form(...),
    transportasi_id: int = Form(...),
    penyelia_id: int = Form(...),
    juleha_id: int = Form(...),
    ternak_id: int = Form(...),
):
    lock = True
    transaksi = transaksi_db.get_by_id(transaksi_id)
    transaksi.jumlah = jumlah
    transaksi.lapak_id = lapak_id
    transaksi.transportasi_id = transportasi_id
    transaksi.penyelia_id = penyelia_id
    transaksi.juleha_id = juleha_id
    transaksi.ternak_id = ternak_id

    transaksi = transaksi_db.update(transaksi)
    return str(transaksi_view.transaksi_form(transaksi, lock))


# Delete


@routes.delete("/{transaksi_id}", response_class=HTMLResponse)
def remove_transaksi(transaksi_id: int):
    transaksi = transaksi_db.get_by_id(transaksi_id)
    if transaksi is None:
        raise HTTPException(status_code=404, detail="User not found")
    transaksis = transaksi_db.remove(transaksi)
    return str(transaksi_view.transaksis_table(transaksis))
