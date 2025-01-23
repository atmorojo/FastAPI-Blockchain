from fastapi import APIRouter, Depends, Form
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
    return str(
        pages.table_page(
            "Laporan Sembelihan per Juleha",
            report_view.date_range("/report/sembelih"),
            button=False
        )
    )


#@routes.put("/sembelih", response_class=HTMLResponse)
@routes.get("/coba", response_class=HTMLResponse)
def juleha_sembelih_by_date(
    db=Depends(get_db),
    # sejak=Form(...),
    # sampai=Form(...),
):
    """
    TODO:
    * Ambil nama RPH!
    """
    sejak="1991-02-01"
    sampai = datetime.now().strftime("%Y-%m-%d")
    report = Report(db, models.Ternak, models.Transaksi)
    report_data = report.ternak_range_report(
        sejak, sampai).group_by_juleha().group_by_date().get_all()
    report = report_view.report_juleha_table("RPH", f"{sejak} - {sampai}", report_data)
    return str(report_view.tpl_print(report))


@routes.get("/pengiriman", response_class=HTMLResponse)
def kiriman_lapak_report(db=Depends(get_db)):
    today = datetime.now().strftime("%Y-%m-%d")
    report = Report(db, models.Ternak, models.Transaksi)
    report_data = report.kiriman_range_report(
        today, today).group_by_lapak().group_by_waktu_kirim().get_all()
    return str(
        pages.table_page(
            "Laporan Pengiriman per Lapak",
            report_view.report_kiriman_table(report_data),
            date_filter=date_range("/report/pengiriman"),
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
    report_data = report.kiriman_range_report(
        sejak, sampai).group_by_lapak().group_by_waktu_kirim().get_all()
    return str(report_view.report_kiriman_table(report_data))


