from fastapi import (
    Depends, APIRouter, HTTPException, Form, Request
)
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models
from controllers import crud as ternak_db
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


@routes.post("/")
async def create_ternak(
    bobot: str = Form(...),
    jenis: str = Form(...),
    kesehatan: str = Form(...),
    peternak_id: int = Form(...),
    juleha_id: int = Form(...),
    db: Session = Depends(get_db)
):
    ternak = models.Ternak(
        bobot=bobot,
        jenis=jenis,
        kesehatan=kesehatan,
        peternak_id=peternak_id,
        juleha_id=juleha_id,
    )
    ternak_db.create(ternak, db=db)
    return RedirectResponse("/ternak", status_code=302)


@routes.get("/new", response_class=HTMLResponse)
def new_ternak(
    db: Session = Depends(get_db),
):
    peternaks = ternak_db.get(models.Peternak, db)
    julehas = ternak_db.get(models.Juleha, db)
    return str(pages.ternak_detail(
        peternaks=peternaks,
        julehas=julehas,
        lock=False
    ))


@routes.get("/", response_class=HTMLResponse)
def read_ternaks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    ternaks = ternak_db.get(models.Ternak, db, skip=skip, limit=limit)
    return str(pages.ternaks_page(ternaks))


@routes.get("/{ternak_id}", response_class=HTMLResponse)
def read_ternak(ternak_id: int, db: Session = Depends(get_db)):
    ternak = ternak_db.get_by_id(models.Ternak, ternak_id, db)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.ternak_detail(ternak, lock=True))


@routes.get("/edit/{ternak_id}", response_class=HTMLResponse)
def edit_ternak(req: Request, ternak_id: int, db: Session = Depends(get_db)):
    ternak = ternak_db.get_by_id(models.Ternak,  ternak_id, db)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    peternaks = ternak_db.get(models.Peternak, db)
    julehas = ternak_db.get(models.Juleha, db)
    if req.headers.get('HX-Request'):
        return str(pages.ternak_form(
            ternak, peternaks=peternaks, julehas=julehas, lock=False))
    else:
        return str(pages.ternak_detail(
            ternak, peternaks=peternaks, julehas=julehas, lock=False))


@routes.delete("/{ternak_id}", response_class=HTMLResponse)
def remove_ternak(
    ternak_id: int,
    db: Session = Depends(get_db)
):
    ternak = ternak_db.get_by_id(models.Ternak, ternak_id, db)
    if ternak is None:
        raise HTTPException(status_code=404, detail="User not found")
    ternaks = ternak_db.remove(models.Ternak, ternak, db)
    return str(pages.ternaks_table(ternaks))


@routes.put("/{ternak_id}", response_class=HTMLResponse)
async def update_ternak(
    ternak_id: int,
    bobot: str = Form(...),
    jenis: str = Form(...),
    kesehatan: str = Form(...),
    peternak_id: int = Form(...),
    juleha_id: int = Form(...),
    db: Session = Depends(get_db)
):
    ternak = ternak_db.get_by_id(models.Ternak, ternak_id, db)
    ternak.bobot = bobot
    ternak.jenis = jenis
    ternak.kesehatan = kesehatan
    ternak.peternak_id = peternak_id
    ternak.juleha_id = juleha_id
    db.commit()
    db.refresh(ternak)
    return str(pages.ternak_form(
        ternak, lock=True))
