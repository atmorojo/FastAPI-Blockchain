from fastapi import (
    APIRouter, HTTPException, Form, Request
)
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import templates.pages as pages
import templates.transportasi as transportasi_view

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/transportasi"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


transportasi_db = Crud(models.Transportasi, next(get_db()))


@routes.get("/new", response_class=HTMLResponse)
def new_transportasi():
    rph = Crud(models.Rph, next(get_db())).get()
    return str(pages.detail_page(
        "transportasi",
        transportasi_view.transportasi_form(None, rph=rph)
    ))


@routes.post("/")
async def create_transportasi(
    name: str = Form(...),
    rph_id: str = Form(...),
):
    transportasi = models.Transportasi(
        nama=name,
        rph_id=rph_id,
    )
    transportasi_db.create(transportasi)
    return RedirectResponse("/transportasi", status_code=302)


# Read


@routes.get("/", response_class=HTMLResponse)
def read_transportasis(skip: int = 0, limit: int = 100):
    transportasis = transportasi_db.get(skip=skip, limit=limit)
    return str(pages.table_page(
        "transportasi",
        transportasi_view.transportasis_table(transportasis)
    ))


@routes.get("/{transportasi_id}", response_class=HTMLResponse)
def read_transportasi(transportasi_id: int):
    lock = True
    transportasi = transportasi_db.get_by_id(transportasi_id)
    if transportasi is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.detail_page(
        "transportasi",
        transportasi_view.transportasi_form(transportasi, lock)
    ))


# Update


@routes.get("/edit/{transportasi_id}", response_class=HTMLResponse)
def edit_transportasi(req: Request, transportasi_id: int):
    transportasi = transportasi_db.get_by_id(transportasi_id)
    rph = Crud(models.Rph, next(get_db())).get()
    if transportasi is None:
        raise HTTPException(status_code=404, detail="User not found")

    form = transportasi_view.transportasi_form(transportasi, rph)
    if req.headers.get('HX-Request'):
        return str(form)
    else:
        return str(pages.detail_page("transportasi", form))


@routes.put("/{transportasi_id}", response_class=HTMLResponse)
async def update_transportasi(
    transportasi_id: int,
    name: str = Form(...),
    rph_id: str = Form(...),
):
    lock = True
    transportasi = transportasi_db.get_by_id(transportasi_id)
    transportasi.nama = name
    transportasi.rph_id = rph_id

    transportasi = transportasi_db.update(transportasi)
    return str(transportasi_view.transportasi_form(transportasi, lock))


# Delete


@routes.delete("/{transportasi_id}", response_class=HTMLResponse)
def remove_transportasi(transportasi_id: int):
    transportasi = transportasi_db.get_by_id(transportasi_id)
    if transportasi is None:
        raise HTTPException(status_code=404, detail="User not found")
    transportasis = transportasi_db.remove(transportasi)
    return str(transportasi_view.transportasis_table(transportasis))
