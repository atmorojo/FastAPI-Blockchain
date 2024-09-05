from fastapi import (
    APIRouter, HTTPException, Form, Request
)
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import templates.ternak as pages

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/ternak"
)


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
    name: str = Form(...),
    bobot: str = Form(...),
    jenis: str = Form(...),
    kesehatan: str = Form(...),
    peternak_id: int = Form(...),
    juleha_id: int = Form(...),
):
    ternak = models.Ternak(
        name=name,
        bobot=bobot,
        jenis=jenis,
        kesehatan=kesehatan,
        peternak_id=peternak_id,
        juleha_id=juleha_id,
    )
    ternak_db.create(ternak)
    return RedirectResponse("/ternak", status_code=302)


@routes.get("/new", response_class=HTMLResponse)
def new_ternak():
    peternaks = Crud(models.Peternak, next(get_db())).get()
    julehas = Crud(models.Juleha, next(get_db())).get()
    return str(pages.ternak_detail(
        peternaks=peternaks,
        julehas=julehas,
        lock=False
    ))


@routes.get("/", response_class=HTMLResponse)
def read_ternaks(skip: int = 0, limit: int = 100):
    ternaks = ternak_db.get(skip=skip, limit=limit)
    return str(pages.ternaks_page(ternaks))


@routes.get("/{ternak_id}", response_class=HTMLResponse)
def read_ternak(ternak_id: int):
    ternak = ternak_db.get_by_id(ternak_id)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.ternak_detail(ternak, lock=True))


@routes.get("/edit/{ternak_id}", response_class=HTMLResponse)
def edit_ternak(req: Request, ternak_id: int):
    ternak = ternak_db.get_by_id(ternak_id)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    peternaks = Crud(models.Peternak, next(get_db())).get()
    julehas = Crud(models.Juleha, next(get_db())).get()
    if req.headers.get('HX-Request'):
        return str(pages.ternak_form(
            ternak, peternaks=peternaks, julehas=julehas, lock=False))
    else:
        return str(pages.ternak_detail(
            ternak, peternaks=peternaks, julehas=julehas, lock=False))


@routes.delete("/{ternak_id}", response_class=HTMLResponse)
def remove_ternak(ternak_id: int):
    ternak = ternak_db.get_by_id(ternak_id)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    ternaks = ternak_db.remove(ternak)
    return str(pages.ternaks_table(ternaks))


@routes.put("/{ternak_id}", response_class=HTMLResponse)
async def update_ternak(
    ternak_id: int,
    name: str = Form(...),
    bobot: str = Form(...),
    jenis: str = Form(...),
    kesehatan: str = Form(...),
    peternak_id: int = Form(...),
    juleha_id: int = Form(...),
):
    ternak = ternak_db.get_by_id(ternak_id)
    ternak.name = name
    ternak.bobot = bobot
    ternak.jenis = jenis
    ternak.kesehatan = kesehatan
    ternak.peternak_id = peternak_id
    ternak.juleha_id = juleha_id
    ternak = ternak_db.update(ternak)
    return str(pages.ternak_form(
        ternak, lock=True))
