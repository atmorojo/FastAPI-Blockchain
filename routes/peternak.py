from fastapi import APIRouter, HTTPException, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models, security
from controllers.crud import Crud
from src.database import SessionLocal, engine
from templates.pages import detail_page as tpl_detail, table_page as tpl_list
from templates.peternak import peternak_form as tpl_form, peternak_table as tpl_table

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/peternak",
    dependencies=[Depends(security.auth_rph)]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


peternak_db = Crud(models.Peternak, next(get_db()))


# Views


@routes.get("/", response_class=HTMLResponse)
def read_peternaks(skip: int = 0, limit: int = 100):
    peternaks = peternak_db.get(skip=skip, limit=limit)
    return str(tpl_list("Peternak", tpl_table(peternaks)))


@routes.get("/new", response_class=HTMLResponse)
def new_peternak():
    return str(tpl_detail("Peternak", tpl_form(lock=False)))


@routes.get("/{peternak_id}", response_class=HTMLResponse)
def read_peternak(peternak_id: int):
    lock = True
    peternak = peternak_db.get_by_id(peternak_id)
    if peternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(tpl_detail("Peternak", tpl_form(peternak, lock)))


@routes.get("/edit/{peternak_id}", response_class=HTMLResponse)
def edit_peternak(req: Request, peternak_id: int):
    lock = False
    peternak = peternak_db.get_by_id(peternak_id)
    if peternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    form = tpl_form(peternak, lock)
    if req.headers.get("HX-Request"):
        return str(form)
    else:
        return str(tpl_detail("Peternak", form))


# Data Manipulation


@routes.post("/")
async def create_peternak(
    name: str = Form(...),
    alamat: str = Form(...),
    status_usaha: str = Form(...),
):
    peternak = models.Peternak(
        name=name,
        alamat=alamat,
        status_usaha=status_usaha,
    )
    peternak_db.create(peternak)
    return RedirectResponse("/peternak", status_code=302)


@routes.delete("/{peternak_id}", response_class=HTMLResponse)
def remove_peternak(peternak_id: int):
    peternak = peternak_db.get_by_id(peternak_id)
    if peternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    peternaks = peternak_db.remove(peternak)
    return str(tpl_table(peternaks))


@routes.put("/{peternak_id}", response_class=HTMLResponse)
async def update_peternak(
    peternak_id: int,
    name: str = Form(...),
    alamat: str = Form(...),
    status_usaha: str = Form(...),
):
    peternak = peternak_db.get_by_id(peternak_id)
    peternak.name = name
    peternak.alamat = alamat
    peternak.status_usaha = status_usaha
    peternak = peternak_db.update(peternak)
    return str(tpl_form(peternak, lock=True))
