from datetime import datetime as dt
from templates.components import (
    table_builder,
    navbar,
)

from htpy import div, Element, tr, td, a, p, b, h1


def bc_detail(data, logged_in) -> Element:
    return div[
        navbar(role=None, logged_in=logged_in),
        h1(style="margin-top: 4em; margin-bottom: 1em;")["Keterangan daging"],
        p[b["Nama RPH: "], data["rph_name"]],
        p[b["Nama Lapak: "], data["lapak_name"]],
        p[b["Pemilik Ternak: "], data["peternak_name"]],
        p[b["Juleha: "], data["juleha_name"]],
        p[b["Bobot: "], f"{data['jumlah']} Kg"],
        p[b["Disembelih pada: "], data["waktu_sembelih"]],
        (
            a(
                role="button",
                href=f"/sensor/end/{data['id_transaksi']}",
            )["Sudah Sampai"]
            if logged_in
            else ""
        ),
    ]


def kiriman_table(data) -> Element:
    col_headers = ["Kiriman dari", "Jumlah", "Dikirim pada", "Actions"]
    rows = (
        tr[
            td[d.ternak.penyelia.rph.name],
            td[f"{d.jumlah} Kg"],
            td[str_time(d.waktu_kirim)],
            td[
                a(
                    role="button",
                    disabled=(False if d.waktu_selesai_kirim else True),
                    href=f"/print/qr/{d.id}",
                )["Print QR"]
            ],
        ]
        for d in data
    )

    return table_builder(col_headers, rows)


def str_time(time):
    return dt.strptime(time, "%Y-%m-%dT%H:%M").strftime("%d %B %Y")
