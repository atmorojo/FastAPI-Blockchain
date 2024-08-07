from fastapi import (
    Depends, APIRouter, HTTPException, Form, Request
)
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models
from controllers import peternak_ctrl
from src.database import SessionLocal, engine
import templates.peternak as pages

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/peternaks"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@routes.post("/")
async def create_peternak(
    name: str = Form(...),
    alamat: str = Form(...),
    status_usaha: str = Form(...),
    db: Session = Depends(get_db)
):
    peternak = models.Peternak(
        name=name,
        alamat=alamat,
        status_usaha=status_usaha,
    )
    peternak_ctrl.create_peternak(db=db, peternak=peternak)
    return RedirectResponse("/peternaks", status_code=302)


@routes.get("/new", response_class=HTMLResponse)
def new_peternak():
    return str(pages.peternak_detail(lock=False))


@routes.get("/", response_class=HTMLResponse)
def read_peternaks(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    peternaks = peternak_ctrl.get_peternaks(db, skip=skip, limit=limit)
    return str(pages.peternaks_page(peternaks))


@routes.get("/{peternak_id}", response_class=HTMLResponse)
def read_peternak(peternak_id: int, db: Session = Depends(get_db)):
    db_peternak = peternak_ctrl.get_peternak(db, peternak_id=peternak_id)
    if db_peternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.peternak_detail(db_peternak, lock=True))


@routes.get("/edit/{peternak_id}", response_class=HTMLResponse)
def edit_peternak(req: Request, peternak_id: int, db: Session = Depends(get_db)):
    db_peternak = peternak_ctrl.get_peternak(db, peternak_id=peternak_id)
    if db_peternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    if req.headers.get('HX-Request'):
        return str(pages.peternak_form(db_peternak, lock=False))
    else:
        return str(pages.peternak_detail(db_peternak, lock=False))


@routes.delete("/{peternak_id}", response_class=HTMLResponse)
def remove_peternak(
    peternak_id: int,
    db: Session = Depends(get_db)
):
    db_peternak = peternak_ctrl.get_peternak(db, peternak_id=peternak_id)
    if db_peternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    peternaks = peternak_ctrl.rm_peternak(db, db_peternak)
    return str(pages.peternaks_table(peternaks))


@routes.put("/{peternak_id}", response_class=HTMLResponse)
async def update_peternak(
    peternak_id: int,
    db: Session = Depends(get_db),
    name: str = Form(...),
    alamat: str = Form(...),
    status_usaha: str = Form(...),
):
    peternak = peternak_ctrl.get_peternak(db, peternak_id)
    peternak.name = name
    peternak.alamat = alamat
    peternak.status_usaha = status_usaha
    db.commit()
    db.refresh(peternak)
    return str(pages.peternak_form(peternak, lock=True))
