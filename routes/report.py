from fastapi import APIRouter, HTTPException, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from src import models, security
from controllers.crud import Crud
from src.database import SessionLocal, engine, get_db
import templates.pages as pages
import templates.iot as iot_view

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/report",
    dependencies=[Depends(security.auth_rph)]
)


@routes.get("/new", response_class=HTMLResponse)
def new_iot():
    return str(pages.detail_page("iot", iot_view.iot_form()))


@routes.get("/", response_class=HTMLResponse)
def read_iots(skip: int = 0, limit: int = 100):
    iots = iot_db.get(skip=skip, limit=limit)
    return str(pages.table_page("IoT", iot_view.iots_table(iots)))


@routes.get("/{iot_id}", response_class=HTMLResponse)
def read_iot(iot_id: int):
    lock = True
    iot = iot_db.get_by_id(iot_id)
    if iot is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(pages.detail_page("iot", iot_view.iot_form(iot=iot, lock=lock)))
