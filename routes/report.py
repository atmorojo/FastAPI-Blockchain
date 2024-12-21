from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse

from src import models, security, utils
from src.database import engine, get_db
import templates.pages as pages
import templates.iot as iot_view

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(prefix="/report", dependencies=[Depends(security.auth_rph)])


@routes.get("/pengiriman", response_class=HTMLResponse)
def pengiriman_report(db=Depends(get_db)):
    today = datetime.now().strftime("%Y-%m-%d")

