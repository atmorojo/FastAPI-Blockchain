from fastapi import (
    APIRouter, HTTPException, Form, Request
)
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import src.blockchain as bc
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


class Blockdata:
    def __init__(
        self,
        id_transaksi,
        rph_name,
        lapak_name,
        peternak_name,
        jumlah,
        waktu_sembelih,
        id_csa=None,
        waktu_kirim=None,
        temp_min=None,
        temp_max=None,
        humi_min=None,
        humi_max=None,
        status_validasi=None,
    ):
        self.id_transaksi = id_transaksi
        self.id_csa = id_csa
        self.rph_name = rph_name
        self.lapak_name = lapak_name
        self.peternak_name = peternak_name
        self.jumlah = jumlah
        self.waktu_sembelih = waktu_sembelih
        self.waktu_kirim = waktu_kirim
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.humi_min = humi_min
        self.humi_max = humi_max
        self.status_validasi = status_validasi


transaksi_db = Crud(models.Transaksi, next(get_db()))
pengiriman_db = Crud(models.Pengiriman, next(get_db()))

chain = bc.Blockchain()


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
    iot_id: int = Form(...),
    waktu_kirim: str = Form(...),
):
    transaksi = models.Transaksi(
        jumlah=jumlah,
        lapak_id=lapak_id,
        transportasi_id=transportasi_id,
        penyelia_id=penyelia_id,
        juleha_id=juleha_id,
        ternak_id=ternak_id,
    )

    transaksi = transaksi_db.create(transaksi)

    pengiriman = models.Pengiriman(
        transaksi_id=transaksi.id,
        iot_id=iot_id,
        waktu_kirim=waktu_kirim,
        status_kirim="dikirim"
    )

    pengiriman = pengiriman_db.create(pengiriman)

    block = Blockdata(
        id_transaksi=transaksi.id,
        rph_name=transaksi.transportasi.rph.name,
        lapak_name=transaksi.lapak.name,
        peternak_name=transaksi.ternak.peternak.name,
        jumlah=transaksi.jumlah,
        waktu_sembelih=transaksi.ternak.waktu_sembelih,
        waktu_kirim=pengiriman.waktu_kirim
    )
    chain.mine_block(block.__dict__)
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
