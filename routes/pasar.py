from fastapi import (
    APIRouter, HTTPException, Form, Request
)
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import templates.pages as pages
import templates.pasar as pasar_view

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/pasar"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pasar_db = Crud(models.Pasar, next(get_db()))


@routes.get("/new", response_class=HTMLResponse)
def new_pasar():
    return str(pages.detail_page(
        "Pasar",
        pasar_view.pasar_form(None)
    ))


@routes.post("/")
async def create_pasar(
    name: str = Form(...),
    alamat: str = Form(...),
):
    pasar = models.Pasar(
        name=name,
        alamat=alamat,
    )
    pasar_db.create(pasar)
    return RedirectResponse("/pasar", status_code=302)


# Read


@routes.get("/", response_class=HTMLResponse)
def read_pasars(skip: int = 0, limit: int = 100):
    pasars = pasar_db.get(skip=skip, limit=limit)
    return str(pages.table_page(
        "Pasar",
        pasar_view.pasars_table(pasars)
    ))


@routes.get("/{pasar_id}", response_class=HTMLResponse)
def read_pasar(pasar_id: int):
    lock = True
    pasar = pasar_db.get_by_id(pasar_id)
    if pasar is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.detail_page(
        "Pasar",
        pasar_view.pasar_form(pasar, lock)
    ))


# Update


@routes.get("/edit/{pasar_id}", response_class=HTMLResponse)
def edit_pasar(req: Request, pasar_id: int):
    pasar = pasar_db.get_by_id(pasar_id)
    if pasar is None:
        raise HTTPException(status_code=404, detail="User not found")

    form = pasar_view.pasar_form(pasar)
    if req.headers.get('HX-Request'):
        return str(form)
    else:
        return str(pages.detail_page("Pasar", form))


@routes.put("/{pasar_id}", response_class=HTMLResponse)
async def update_pasar(
    pasar_id: int,
    name: str = Form(...),
    alamat: str = Form(...),
):
    lock = True
    pasar = pasar_db.get_by_id(pasar_id)
    pasar.name = name
    pasar.alamat = alamat

    pasar = pasar_db.update(pasar)
    return str(pasar_view.pasar_form(pasar, lock))


# Delete


@routes.delete("/{pasar_id}", response_class=HTMLResponse)
def remove_pasar(pasar_id: int):
    pasar = pasar_db.get_by_id(pasar_id)
    if pasar is None:
        raise HTTPException(status_code=404, detail="User not found")
    pasars = pasar_db.remove(pasar)
    return str(pasar_view.pasars_table(pasars))
