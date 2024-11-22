from fastapi import APIRouter, HTTPException, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import src.blockchain as bc
import templates.pages as pages
import templates.transaksi as tpl_transaksi
from sqlalchemy.orm import Session
from src.security import current_user_validation, get_current_user

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(prefix="/transaksi")


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
        rph_name,
        lapak_name,
        peternak_name,
        juleha_name,
        jumlah,
        waktu_sembelih,
        waktu_kirim,
        id_transaksi,
        id_csa=None,
        temp_min=None,
        temp_max=None,
        humi_min=None,
        humi_max=None,
        status_validasi=None,
        waktu_selesai_kirim=None,
    ):
        self.id_transaksi = id_transaksi
        self.id_csa = id_csa
        self.rph_name = rph_name
        self.lapak_name = lapak_name
        self.peternak_name = peternak_name
        self.juleha_name = juleha_name
        self.jumlah = jumlah
        self.waktu_sembelih = waktu_sembelih
        self.waktu_kirim = waktu_kirim
        self.waktu_selesai_kirim = waktu_selesai_kirim
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.humi_min = humi_min
        self.humi_max = humi_max
        self.status_validasi = status_validasi


transaksi_db = Crud(models.Transaksi, next(get_db()))
chain = bc.Blockchain()


# TABLE PAGE
@routes.get("/", response_class=HTMLResponse)
def table_transaksis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transaksi = Crud(models.Transaksi, db).get(skip=skip, limit=limit)
    table = tpl_transaksi.transaksis_table(transaksi)
    page = pages.table_page("Transaksi", table)
    return str(page)


# NEW PAGE
@routes.get("/new", response_class=HTMLResponse)
def new_transaksi(db: Session = Depends(get_db)):
    lapak = Crud(models.Lapak, db).get()
    ternak = Crud(models.Ternak, db).get()
    iot = Crud(models.IoT, db).get()

    return str(
        pages.detail_page(
            "Transaksi",
            tpl_transaksi.transaksi_form(lapak=lapak, ternak=ternak, iot=iot),
        )
    )


# POST ENDPOINT
@routes.post("/")
async def create_transaksi(
    jumlah: str = Form(...),
    lapak_id: int = Form(...),
    ternak_id: int = Form(...),
    iot_id: int = Form(None),
    waktu_kirim: str = Form(None),
):
    transaksi = models.Transaksi(
        jumlah=jumlah,
        lapak_id=lapak_id,
        ternak_id=ternak_id,
        iot_id=iot_id,
        waktu_kirim=waktu_kirim,
        status_kirim="dikirim",
    )

    transaksi = transaksi_db.create(transaksi)

    block = Blockdata(
        id_transaksi=transaksi.id,
        rph_name=transaksi.ternak.penyelia.rph.name,
        lapak_name=transaksi.lapak.name,
        peternak_name=transaksi.ternak.peternak.name,
        juleha_name=transaksi.ternak.juleha.name,
        jumlah=transaksi.jumlah,
        waktu_sembelih=transaksi.ternak.waktu_sembelih,
        waktu_kirim=transaksi.waktu_kirim,
    )
    chain.mine_block(block.__dict__)
    return RedirectResponse("/transaksi", status_code=302)


# DETAIL PAGE
@routes.get("/{transaksi_id}", response_class=HTMLResponse)
def read_transaksi(transaksi_id: int):
    lock = True
    transaksi = transaksi_db.get_by_id(transaksi_id)

    if transaksi is None:
        raise HTTPException(status_code=404, detail="User not found")

    return str(
        pages.detail_page(
            "transaksi", tpl_transaksi.transaksi_form(transaksi=transaksi, lock=lock)
        )
    )


# Edit Page
@routes.get("/edit/{transaksi_id}", response_class=HTMLResponse)
def edit_transaksi(req: Request, transaksi_id: int, db: Session = Depends(get_db)):
    transaksi = transaksi_db.get_by_id(transaksi_id)
    lapak = Crud(models.Lapak, db).get()
    ternak = Crud(models.Ternak, db).get()
    iot = Crud(models.IoT, db).get()

    if transaksi is None:
        raise HTTPException(status_code=404, detail="User not found")

    form = tpl_transaksi.transaksi_form(
        transaksi=transaksi,
        lapak=lapak,
        ternak=ternak,
        iot=iot,
    )
    if req.headers.get("HX-Request"):
        return str(form)
    else:
        return str(pages.detail_page("Transaksi", form))


# PUT ENDPOINT
@routes.put("/{transaksi_id}", response_class=HTMLResponse)
async def update_transaksi(
    transaksi_id: int,
    jumlah: str = Form(...),
    lapak_id: int = Form(...),
    ternak_id: int = Form(...),
    iot_id: int = Form(...),
    waktu_kirim: str = Form(...),
    db: Session = Depends(get_db),
):
    lock = True

    transaksi = transaksi_db.get_by_id(transaksi_id)
    transaksi.jumlah = jumlah
    transaksi.lapak_id = lapak_id
    transaksi.ternak_id = ternak_id
    transaksi.iot_id = iot_id
    transaksi = transaksi_db.update(transaksi)

    block = Blockdata(
        id_transaksi=transaksi.id,
        rph_name=transaksi.ternak.penyelia.rph.name,
        lapak_name=transaksi.lapak.name,
        peternak_name=transaksi.ternak.peternak.name,
        juleha_name=transaksi.ternak.juleha.name,
        jumlah=transaksi.jumlah,
        waktu_sembelih=transaksi.ternak.waktu_sembelih,
        waktu_kirim=transaksi.waktu_kirim,
    )
    chain.mine_block(block.__dict__)

    return str(
        tpl_transaksi.transaksi_form(
            transaksi,
            lock,
        )
    )


# Delete


@routes.post("/{rm_transaksi_id}", response_class=HTMLResponse)
def remove_transaksi(
    rm_transaksi_id: int,
    password: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not current_user_validation(current_user, password):
        return str(tpl_transaksi.unauthorized("/transaksi/"))
    transaksi = transaksi_db.get_by_id(rm_transaksi_id)
    if transaksi is None:
        raise HTTPException(status_code=404, detail="User not found")
    transaksis = transaksi_db.remove(transaksi)
    return str(tpl_transaksi.transaksis_table(transaksis))
