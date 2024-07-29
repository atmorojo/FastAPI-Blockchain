from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

from src import crud, models, schemas
from src.database import SessionLocal, engine
import templates.pages as pages

models.Base.metadata.create_all(bind=engine)

routes = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@routes.post("/julehas/", response_model=schemas.Juleha)
def create_juleha(
        juleha: schemas.Juleha,
        db: Session = Depends(get_db)
):
    return crud.create_juleha(db=db, juleha=juleha)


@routes.get("/julehas/", response_class=HTMLResponse)
def read_julehas(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    julehas = crud.get_julehas(db, skip=skip, limit=limit)
    return str(pages.julehas_table(julehas))


@routes.get("/julehas/{juleha_id}", response_model=schemas.Juleha)
def read_juleha( juleha_id: int, db: Session = Depends(get_db)):
    db_juleha = crud.get_juleha(db, juleha_id=juleha_id)
    if db_juleha is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_juleha
