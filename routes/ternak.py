from fastapi import APIRouter, HTTPException, Form, Request, File, UploadFile, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
import aiofiles

from sqlalchemy.orm import Session
from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import templates.pages as pages
import templates.ternak as ternak_view
from templates.components import date_range
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(prefix="/ternak")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ternak_db = Crud(models.Ternak, next(get_db()))


@routes.post("/")
async def create_ternak(
    img: UploadFile = File(...),
    bobot: str = Form(...),
    jenis: str = Form(...),
    peternak_id: int = Form(...),
):
    waktu_daftar = datetime.now().strftime("%Y-%m-%d")
    last_no_antri = ternak_db.get_latest_field("no_antri", "waktu_daftar", waktu_daftar)
    ternak = models.Ternak(
        bobot=bobot,
        jenis=jenis,
        peternak_id=peternak_id,
        waktu_daftar=waktu_daftar,
        no_antri=((int(last_no_antri.no_antri)
                   if last_no_antri is not None
                   else 0) + 1)
    )
    ternak = ternak_db.create(ternak)

    if img.filename != "":
        ternak.img = ternak.id
        out_file_path = "./files/img_ternak/" + str(ternak.id)
        async with aiofiles.open(out_file_path, "wb") as out_file:
            while content := await img.read(1024):
                await out_file.write(content)
    ternak_db.update(ternak)
    return RedirectResponse("/ternak/", status_code=302)


@routes.get("/new", response_class=HTMLResponse)
def new_ternak(db: Session = Depends(get_db)):
    peternaks = Crud(models.Peternak, db).get()
    return str(
        pages.detail_page(
            "Ternak",
            ternak_view.ternak_form(
                peternaks=peternaks, lock=False
            ),
        )
    )


@routes.get("/", response_class=HTMLResponse)
def read_ternaks(skip: int = 0, limit: int = 100):
    tgl = datetime.now().strftime("%Y-%m-%d")
    ternaks = ternak_db.get_by_date("waktu_daftar", tgl, tgl)
    return str(
        pages.table_page(
            "Ternak",
            ternak_view.ternaks_table(ternaks),
            date_filter=date_range("/ternak/"),
        )
    )


@routes.put("/", response_class=HTMLResponse)
def read_ternaks_by_date(
    sejak=Form(...),
    sampai=Form(...),
):
    ternaks = ternak_db.get_by_date("waktu_daftar", sejak, sampai)
    return str(ternak_view.ternaks_table(ternaks))


@routes.get("/{ternak_id}", response_class=HTMLResponse)
def read_ternak(
    ternak_id: int,
):
    ternak = ternak_db.get_by_id(ternak_id)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(
        pages.detail_page("Ternak", ternak_view.ternak_form(ternak=ternak, lock=True))
    )


@routes.get("/edit/{ternak_id}", response_class=HTMLResponse)
def edit_ternak(
    req: Request,
    ternak_id: int,
    db: Session = Depends(get_db),
):
    ternak = ternak_db.get_by_id(ternak_id)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    peternaks = Crud(models.Peternak, db).get()
    form = ternak_view.ternak_form(
        ternak, peternaks=peternaks, lock=False
    )
    if req.headers.get("HX-Request"):
        return str(form)
    else:
        return str(pages.detail_page("Ternak", form))


@routes.get("/proses/edit/{ternak_id}", response_class=HTMLResponse)
def proses_ternak(
    req: Request,
    ternak_id: int,
    db: Session = Depends(get_db),
):
    ternak = ternak_db.get_by_id(ternak_id)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    julehas = Crud(models.Juleha, db).get()
    penyelias = Crud(models.Penyelia, db).get()
    form = ternak_view.sembelih_form(
        ternak, julehas=julehas, penyelias=penyelias, lock=False
    )
    if req.headers.get("HX-Request"):
        return str(form)
    else:
        return str(pages.detail_page("Ternak", form))




@routes.delete("/{ternak_id}", response_class=HTMLResponse)
def remove_ternak(ternak_id: int):
    ternak = ternak_db.get_by_id(ternak_id)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    ternaks = ternak_db.remove(ternak)
    return str(ternak_view.ternaks_table(ternaks))


@routes.put("/{ternak_id}", response_class=HTMLResponse)
async def update_ternak(
    ternak_id: int,
    bobot: str = Form(...),
    jenis: str = Form(...),
    peternak_id: int = Form(...),
    img: UploadFile = Form(None),
):
    ternak = ternak_db.get_by_id(ternak_id)
    ternak.bobot = bobot
    ternak.jenis = jenis
    ternak.peternak_id = peternak_id

    if img is not None:
        ternak.img = ternak.id
        out_file_path = "./files/img_ternak/" + str(ternak.id)
        async with aiofiles.open(out_file_path, "wb") as out_file:
            while content := await img.read(1024):
                await out_file.write(content)
    ternak = ternak_db.update(ternak)
    return str(ternak_view.ternak_form(ternak, lock=True))


@routes.put("/proses/{ternak_id}", response_class=HTMLResponse)
def put_proses_ternak(
    req: Request,
    ternak_id: int,
    penyelia_id: int = Form(...),
    juleha_id: int = Form(...),
    karkas: str = Form(...),
    kesehatan: str = Form(...),
    waktu_sembelih: str = Form(None),
    db: Session = Depends(get_db),
):
    ternak = ternak_db.get_by_id(ternak_id)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    ternak.penyelia_id = penyelia_id
    ternak.juleha_id = juleha_id
    ternak.karkas = karkas
    ternak.kesehatan = kesehatan
    if ternak.waktu_sembelih is None:
        ternak.waktu_sembelih = datetime.now().strftime("%Y-%m-%d")
    else:
        ternak.waktu_sembelih = waktu_sembelih

    ternak = ternak_db.update(ternak)
    form = ternak_view.sembelih_form(ternak, lock=True)
    if req.headers.get("HX-Request"):
        return str(form)
    else:
        return str(pages.detail_page("Ternak", form))


@routes.get("/proses/{ternak_id}", response_class=HTMLResponse)
def proses_ternak_review(
    ternak_id: int,
    db: Session = Depends(get_db),
):
    ternak = ternak_db.get_by_id(ternak_id)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")

    form = ternak_view.sembelih_form(ternak, lock=True)
    return str(pages.detail_page("Ternak", form))
