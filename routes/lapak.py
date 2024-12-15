from fastapi import APIRouter, HTTPException, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models, security
from controllers.crud import Crud
from src.database import SessionLocal, engine
import templates.pages as pages
import templates.lapak as lapak_view

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/lapak",
    dependencies=[Depends(security.auth_rph)]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


lapak_db = Crud(models.Lapak, next(get_db()))


@routes.get("/new", response_class=HTMLResponse)
def new_lapak():
    pasar = Crud(models.Pasar, next(get_db())).get()
    return str(pages.detail_page("lapak", lapak_view.lapak_form(pasar=pasar)))


@routes.post("/")
async def create_lapak(
    name: str = Form(...),
    no_lapak: int = Form(...),
    pasar_id: int = Form(...),
):
    lapak = models.Lapak(
        name=name,
        no_lapak=no_lapak,
        pasar_id=pasar_id,
    )
    lapak_db.create(lapak)
    return RedirectResponse("/lapak", status_code=302)


# Read


@routes.get("/", response_class=HTMLResponse)
def read_lapaks(skip: int = 0, limit: int = 100):
    lapaks = lapak_db.get(skip=skip, limit=limit)
    return str(pages.table_page("Lapak", lapak_view.lapaks_table(lapaks)))


@routes.get("/{lapak_id}", response_class=HTMLResponse)
def read_lapak(lapak_id: int):
    lock = True
    lapak = lapak_db.get_by_id(lapak_id)
    if lapak is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(
        pages.detail_page("lapak", lapak_view.lapak_form(lapak=lapak, lock=lock))
    )


# Update


@routes.get("/edit/{lapak_id}", response_class=HTMLResponse)
def edit_lapak(req: Request, lapak_id: int):
    lapak = lapak_db.get_by_id(lapak_id)
    pasar = Crud(models.Pasar, next(get_db())).get()
    if lapak is None:
        raise HTTPException(status_code=404, detail="User not found")

    form = lapak_view.lapak_form(lapak=lapak, pasar=pasar)
    if req.headers.get("HX-Request"):
        return str(form)
    else:
        return str(pages.detail_page("Lapak", form))


@routes.put("/{lapak_id}", response_class=HTMLResponse)
async def update_lapak(
    lapak_id: int,
    name: str = Form(...),
    no_lapak: str = Form(...),
    pasar_id: int = Form(...),
):
    lock = True
    lapak = lapak_db.get_by_id(lapak_id)
    lapak.nama = name
    lapak.no_lapak = no_lapak
    lapak.pasar_id = pasar_id

    lapak = lapak_db.update(lapak)
    return str(lapak_view.lapak_form(lapak, lock))


# Delete


@routes.delete("/{lapak_id}", response_class=HTMLResponse)
def remove_lapak(lapak_id: int):
    lapak = lapak_db.get_by_id(lapak_id)
    if lapak is None:
        raise HTTPException(status_code=404, detail="User not found")
    lapaks = lapak_db.remove(lapak)
    return str(lapak_view.lapaks_table(lapaks))
