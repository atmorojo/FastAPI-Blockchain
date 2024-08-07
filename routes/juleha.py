from fastapi import Depends, APIRouter, HTTPException, UploadFile, Form, File, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
import aiofiles
from datetime import datetime

from src import models
from controllers import juleha_ctrl
from src.database import SessionLocal, engine
import templates.juleha as pages

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/julehas"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@routes.post("/")
async def create_juleha(
    name: str = Form(...),
    masa_sertifikat: str = Form(...),
    nomor_sertifikat: str = Form(...),
    file_sertifikat: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if file_sertifikat.filename != "":
        out_file_path = './files/sertifikat/' + file_sertifikat.filename
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await file_sertifikat.read(1024):
                await out_file.write(content)

    juleha = models.Juleha(
        name=name,
        nomor_sertifikat=nomor_sertifikat,
        masa_sertifikat=masa_sertifikat,
        upload_sertifikat=file_sertifikat.filename,
        waktu_upload=datetime.now()
    )
    juleha_ctrl.create_juleha(db=db, juleha=juleha)
    return RedirectResponse("/julehas", status_code=302)


@routes.get("/new", response_class=HTMLResponse)
def new_juleha():
    return str(pages.juleha_detail(lock=False))


@routes.get("/", response_class=HTMLResponse)
def read_julehas(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    julehas = juleha_ctrl.get_julehas(db, skip=skip, limit=limit)
    return str(pages.julehas_page(julehas))


@routes.get("/{juleha_id}", response_class=HTMLResponse)
def read_juleha(juleha_id: int, db: Session = Depends(get_db)):
    db_juleha = juleha_ctrl.get_juleha(db, juleha_id=juleha_id)
    if db_juleha is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.juleha_detail(db_juleha, lock=True))


@routes.get("/edit/{juleha_id}", response_class=HTMLResponse)
def edit_juleha(req: Request, juleha_id: int, db: Session = Depends(get_db)):
    db_juleha = juleha_ctrl.get_juleha(db, juleha_id=juleha_id)
    if db_juleha is None:
        raise HTTPException(status_code=404, detail="User not found")
    if req.headers.get('HX-Request'):
        return str(pages.juleha_form(db_juleha, lock=False))
    else:
        return str(pages.juleha_detail(db_juleha, lock=False))


@routes.delete("/{juleha_id}", response_class=HTMLResponse)
def remove_juleha(
    juleha_id: int,
    db: Session = Depends(get_db)
):
    db_juleha = juleha_ctrl.get_juleha(db, juleha_id=juleha_id)
    if db_juleha is None:
        raise HTTPException(status_code=404, detail="User not found")
    julehas = juleha_ctrl.rm_juleha(db, db_juleha)
    return str(pages.julehas_table(julehas))


@routes.put("/{juleha_id}", response_class=HTMLResponse)
async def update_juleha(
    juleha_id: int,
    db: Session = Depends(get_db),
    name: str = Form(...),
    nomor_sertifikat: str = Form(...),
    masa_sertifikat: str = Form(...),
    file_sertifikat: UploadFile = File(None),
):
    juleha = juleha_ctrl.get_juleha(db, juleha_id)
    juleha.name = name
    juleha.nomor_sertifikat = nomor_sertifikat
    juleha.masa_sertifikat = masa_sertifikat

    if file_sertifikat is not None:
        juleha.upload_sertifikat = file_sertifikat.filename
        juleha.waktu_upload = datetime.now()
        out_file_path = './files/sertifikat/' + file_sertifikat.filename
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await file_sertifikat.read(1024):
                await out_file.write(content)
    db.commit()
    db.refresh(juleha)
    return str(pages.juleha_form(juleha, lock=True))
