from fastapi import (
    APIRouter, HTTPException, UploadFile, Form, File, Request
)
from fastapi.responses import HTMLResponse, RedirectResponse
import aiofiles
from datetime import datetime

from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import templates.penyelia as pages

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/penyelia"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


penyelia_db = Crud(models.Penyelia, next(get_db()))


@routes.get("/new", response_class=HTMLResponse)
def new_penyelia():
    rph = Crud(models.Rph, next(get_db())).get()
    return str(pages.penyelia_detail(
        rph=rph,
        lock=False
    ))


@routes.post("/")
async def create_penyelia(
    nip: str = Form(...),
    name: str = Form(...),
    status: str = Form(...),
    tgl_berlaku: str = Form(...),
    rph_id: int = Form(...),
    file_sk: UploadFile = File(...),
):
    if file_sk.filename != "":
        out_file_path = './files/sk_penyelia/' + file_sk.filename
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await file_sk.read(1024):
                await out_file.write(content)

    penyelia = models.Penyelia(
        nip=nip,
        name=name,
        status=status,
        tgl_berlaku=tgl_berlaku,
        rph_id=rph_id,
        file_sk=file_sk.filename,
    )
    penyelia_db.create(penyelia)
    return RedirectResponse("/penyelia", status_code=302)


# Read


@routes.get("/", response_class=HTMLResponse)
def read_penyelias(skip: int = 0, limit: int = 100):
    penyelias = penyelia_db.get(skip=skip, limit=limit)
    return str(pages.penyelias_page(penyelias))


@routes.get("/{penyelia_id}", response_class=HTMLResponse)
def read_penyelia(penyelia_id: int):
    penyelia = penyelia_db.get_by_id(penyelia_id)
    if penyelia is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.penyelia_detail(penyelia, lock=True))


# Update


@routes.get("/edit/{penyelia_id}", response_class=HTMLResponse)
def edit_penyelia(req: Request, penyelia_id: int):
    penyelia = penyelia_db.get_by_id(penyelia_id)
    rph = Crud(models.Rph, next(get_db())).get()
    lock = False
    if penyelia is None:
        raise HTTPException(status_code=404, detail="User not found")
    if req.headers.get('HX-Request'):
        return str(pages.penyelia_form(penyelia, rph, lock))
    else:
        return str(pages.penyelia_detail(penyelia, rph, lock))


@routes.put("/{penyelia_id}", response_class=HTMLResponse)
async def update_penyelia(
    penyelia_id: int,
    nip: str = Form(...),
    name: str = Form(...),
    status: str = Form(...),
    tgl_berlaku: str = Form(...),
    rph_id: int = Form(...),
    file_sk: UploadFile = File(None)  # Remember to give that None
):
    penyelia = penyelia_db.get_by_id(penyelia_id)
    penyelia.nip = nip
    penyelia.name = name
    penyelia.status = status
    penyelia.tgl_berlaku = tgl_berlaku
    penyelia.rph_id = rph_id

    if file_sk is not None:
        penyelia.file_sk = file_sk.filename
        out_file_path = './files/sk_penyelia/' + file_sk.filename
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await file_sk.read(1024):
                await out_file.write(content)
    penyelia = penyelia_db.update(penyelia)
    rph = Crud(models.Rph, next(get_db())).get()
    return str(pages.penyelia_form(penyelia, rph, lock=True))


# Delete


@routes.delete("/{penyelia_id}", response_class=HTMLResponse)
def remove_penyelia(penyelia_id: int):
    penyelia = penyelia_db.get_by_id(penyelia_id)
    if penyelia is None:
        raise HTTPException(status_code=404, detail="User not found")
    penyelias = penyelia_db.remove(penyelia)
    return str(pages.penyelias_table(penyelias))
