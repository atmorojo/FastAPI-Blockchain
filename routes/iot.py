from fastapi import (
    APIRouter, HTTPException, Form, Request
)
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models
from controllers.crud import Crud
from src.database import SessionLocal, engine
import templates.pages as pages
import templates.iot as iot_view

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/iot"
)

# Fields:
# Int       id
# Int       rph_id
# String    node


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


iot_db = Crud(models.IoT, next(get_db()))


@routes.get("/new", response_class=HTMLResponse)
def new_iot():
    rph = Crud(models.Rph, next(get_db())).get()
    return str(pages.detail_page(
        "iot",
        iot_view.iot_form(rph=rph)
    ))


@routes.post("/")
async def create_iot(
    node: str = Form(...),
    rph_id: int = Form(...),
):
    iot = models.IoT(
        node=node,
        rph_id=rph_id,
    )
    iot_db.create(iot)
    return RedirectResponse("/iot", status_code=302)


# Read


@routes.get("/", response_class=HTMLResponse)
def read_iots(skip: int = 0, limit: int = 100):
    iots = iot_db.get(skip=skip, limit=limit)
    return str(pages.table_page(
        "IoT",
        iot_view.iots_table(iots)
    ))


@routes.get("/{iot_id}", response_class=HTMLResponse)
def read_iot(iot_id: int):
    lock = True
    iot = iot_db.get_by_id(iot_id)
    if iot is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.detail_page(
        "iot",
        iot_view.iot_form(iot=iot, lock=lock)
    ))


# Update


@routes.get("/edit/{iot_id}", response_class=HTMLResponse)
def edit_iot(req: Request, iot_id: int):
    iot = iot_db.get_by_id(iot_id)
    rph = Crud(models.Rph, next(get_db())).get()
    if iot is None:
        raise HTTPException(status_code=404, detail="User not found")

    form = iot_view.iot_form(iot=iot, rph=rph)
    if req.headers.get('HX-Request'):
        return str(form)
    else:
        return str(pages.detail_page("IoT", form))


@routes.put("/{iot_id}", response_class=HTMLResponse)
async def update_iot(
    iot_id: int,
    node: str = Form(...),
    rph_id: int = Form(...),
):
    lock = True
    iot = iot_db.get_by_id(iot_id)
    iot.node = node
    iot.rph_id = rph_id

    iot = iot_db.update(iot)
    return str(iot_view.iot_form(iot, lock))


# Delete


@routes.delete("/{iot_id}", response_class=HTMLResponse)
def remove_iot(iot_id: int):
    iot = iot_db.get_by_id(iot_id)
    if iot is None:
        raise HTTPException(status_code=404, detail="User not found")
    iots = iot_db.remove(iot)
    return str(iot_view.iots_table(iots))
