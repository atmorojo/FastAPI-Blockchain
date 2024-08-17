from fastapi import (
    APIRouter, HTTPException, UploadFile, Form, File, Request
)
from fastapi.responses import HTMLResponse, RedirectResponse
import aiofiles
from datetime import datetime

from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import templates.rph as pages

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/rph"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


rph_db = Crud(models.Rph, next(get_db()))


@routes.post("/")
async def create_rph(
    name: str = Form(...),
    alamat: str = Form(...),
    telepon: str = Form(...),
    status_sertifikasi: str = Form(...),
    file_sertifikasi: UploadFile = File(...),
):
    if file_sertifikasi.filename != "":
        out_file_path = './files/sert_rph/' + file_sertifikasi.filename
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await file_sertifikasi.read(1024):
                await out_file.write(content)

    rph = models.Rph(
        name=name,
        alamat=alamat,
        telepon=telepon,
        status_sertifikasi=status_sertifikasi,
        file_sertifikasi=file_sertifikasi.filename,
        waktu_upload=datetime.now()
    )
    rph_db.create(rph)
    return RedirectResponse("/rph", status_code=302)


@routes.get("/new", response_class=HTMLResponse)
def new_rph():
    return str(pages.rph_detail(lock=False))


@routes.get("/", response_class=HTMLResponse)
def read_rphs(skip: int = 0, limit: int = 100):
    rphs = rph_db.get(skip=skip, limit=limit)
    return str(pages.rphs_page(rphs))


@routes.get("/{rph_id}", response_class=HTMLResponse)
def read_rph(rph_id: int):
    rph = rph_db.get_by_id(rph_id)
    if rph is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.rph_detail(rph, lock=True))


@routes.get("/edit/{rph_id}", response_class=HTMLResponse)
def edit_rph(req: Request, rph_id: int):
    rph = rph_db.get_by_id(rph_id)
    lock = False
    if rph is None:
        raise HTTPException(status_code=404, detail="User not found")
    if req.headers.get('HX-Request'):
        return str(pages.rph_form(rph, lock))
    else:
        return str(pages.rph_detail(rph, lock))


@routes.delete("/{rph_id}", response_class=HTMLResponse)
def remove_rph(rph_id: int):
    rph = rph_db.get_by_id(rph_id)
    if rph is None:
        raise HTTPException(status_code=404, detail="User not found")
    rphs = rph_db.remove(rph)
    return str(pages.rphs_table(rphs))


@routes.put("/{rph_id}", response_class=HTMLResponse)
async def update_rph(
    rph_id: int,
    name: str = Form(...),
    alamat: str = Form(...),
    telepon: str = Form(...),
    status_sertifikasi: str = Form(...),
    file_sertifikasi: UploadFile = File(None)  # Remember to give that None
):
    rph = rph_db.get_by_id(rph_id)
    rph.name = name
    rph.alamat = alamat
    rph.telepon = telepon
    rph.status_sertifikasi = status_sertifikasi

    if file_sertifikasi is not None:
        rph.file_sertifikasi = file_sertifikasi.filename
        rph.waktu_upload = datetime.now()
        out_file_path = './files/sert_rph/' + file_sertifikasi.filename
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await file_sertifikasi.read(1024):
                await out_file.write(content)
    rph = rph_db.update(rph)
    return str(pages.rph_form(rph, lock=True))
