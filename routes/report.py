from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse

from repositories.report import Report
from src import models, security
from src.database import engine, get_db
from datetime import datetime
from templates.components import date_range
import templates.pages as pages
import templates.report as report_view

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(prefix="/report", dependencies=[Depends(security.auth_rph)])


@routes.get("/sembelih", response_class=HTMLResponse)
def juleha_sembelih_report(db=Depends(get_db)):
    today = datetime.now().strftime("%Y-%m-%d")
    report = Report(db, models.Ternak, models.Transaksi)
    report_data = report.ternak_range_report(
        today, today).group_by_juleha().get_all()
    return str(
        pages.table_page(
            "Laporan Sembelihan per Juleha",
            report_view.report_juleha_table(report_data),
            date_filter=date_range("/report/sembelih"),
            button=False
        )
    )


@routes.put("/sembelih", response_class=HTMLResponse)
def juleha_sembelih_by_date(
    db=Depends(get_db),
    sejak=Form(...),
    sampai=Form(...),
):
    report = Report(db, models.Ternak, models.Transaksi)
    report_data = report.ternak_range_report(
        sejak, sampai).group_by_juleha().get_all()
    return str(report_view.report_juleha_table(report_data))


@routes.get("/pengiriman", response_class=HTMLResponse)
def kiriman_lapak_report(db=Depends(get_db)):
    today = datetime.now().strftime("%Y-%m-%d")
    report = Report(db, models.Ternak, models.Transaksi)
    report_data = report.ternak_range_report(
        today, today).group_by_juleha().get_all()
    return str(
        pages.table_page(
            "Laporan Pengiriman per Juleha",
            report_view.report_juleha_table(report_data),
            date_filter=date_range("/report/kiriman"),
            button=False
        )
    )


@routes.put("/pengiriman", response_class=HTMLResponse)
def kiriman_lapak_by_date(
    db=Depends(get_db),
    sejak=Form(...),
    sampai=Form(...),
):
    report = Report(db, models.Ternak, models.Transaksi)
    report_data = report.ternak_range_report(
        sejak, sampai).group_by_juleha().get_all()
    return str(report_view.report_juleha_table(report_data))


