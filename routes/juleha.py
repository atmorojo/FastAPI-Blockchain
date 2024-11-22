from fastapi import APIRouter, HTTPException, UploadFile, Form, File, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import aiofiles
from datetime import datetime

from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import templates.pages as pages
import templates.juleha as tpl_juleha

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(prefix="/juleha")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


juleha_db = Crud(models.Juleha, next(get_db()))


@routes.post("/")
async def create_juleha(
    name: str = Form(...),
    masa_sertifikat: str = Form(...),
    nomor_sertifikat: str = Form(...),
    file_sertifikat: UploadFile = File(...),
):
    juleha = models.Juleha(
        name=name,
        nomor_sertifikat=nomor_sertifikat,
        masa_sertifikat=masa_sertifikat,
        waktu_upload=datetime.now(),
    )

    juleha = juleha_db.create(juleha)

    if file_sertifikat.filename != "":
        juleha.upload_sertifikat = juleha.id
        out_file_path = "./files/sertifikat/" + str(juleha.id)
        async with aiofiles.open(out_file_path, "wb") as out_file:
            while content := await file_sertifikat.read(1024):
                await out_file.write(content)
        juleha_db.update(juleha)

    return RedirectResponse("/juleha/", status_code=302)


@routes.get("/new", response_class=HTMLResponse)
def new_juleha():
    return str(pages.detail_page("juleha", tpl_juleha.juleha_form()))


@routes.get("/", response_class=HTMLResponse)
def read_julehas(skip: int = 0, limit: int = 100):
    julehas = juleha_db.get(skip=skip, limit=limit)
    return str(pages.table_page("Juleha", tpl_juleha.julehas_table(julehas)))


@routes.get("/{juleha_id}", response_class=HTMLResponse)
def read_juleha(juleha_id: int):
    juleha = juleha_db.get_by_id(juleha_id)
    lock = True
    if juleha is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.detail_page("juleha", tpl_juleha.juleha_form(juleha, lock)))


@routes.get("/edit/{juleha_id}", response_class=HTMLResponse)
def edit_juleha(req: Request, juleha_id: int):
    juleha = juleha_db.get_by_id(juleha_id)
    if juleha is None:
        raise HTTPException(status_code=404, detail="User not found")
    form = tpl_juleha.juleha_form(juleha)
    if req.headers.get("HX-Request"):
        return str(form)
    else:
        return str(pages.detail_page("juleha", form))


@routes.delete("/{juleha_id}", response_class=HTMLResponse)
def remove_juleha(juleha_id: int):
    juleha = juleha_db.get_by_id(juleha_id)
    if juleha is None:
        raise HTTPException(status_code=404, detail="User not found")
    julehas = juleha_db.remove(juleha)
    return str(tpl_juleha.julehas_table(julehas))


@routes.put("/{juleha_id}", response_class=HTMLResponse)
async def update_juleha(
    juleha_id: int,
    name: str = Form(...),
    nomor_sertifikat: str = Form(...),
    masa_sertifikat: str = Form(...),
    file_sertifikat: UploadFile = File(None),
):
    lock = True
    juleha = juleha_db.get_by_id(juleha_id)
    juleha.name = name
    juleha.nomor_sertifikat = nomor_sertifikat
    juleha.masa_sertifikat = masa_sertifikat

    if file_sertifikat is not None:
        juleha.upload_sertifikat = juleha.id
        juleha.waktu_upload = datetime.now()
        out_file_path = "./files/sertifikat/" + str(juleha.id)
        async with aiofiles.open(out_file_path, "wb") as out_file:
            while content := await file_sertifikat.read(1024):
                await out_file.write(content)

    juleha = juleha_db.update(juleha)
    return str(tpl_juleha.juleha_form(juleha, lock))
