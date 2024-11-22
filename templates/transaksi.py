from datetime import datetime
from zoneinfo import ZoneInfo

from templates.components import (
    table_builder,
    edit_btn,
    inlabel,
    combo_gen,
    show_img,
    update_btn,
    submit_btn,
    secure_action_buttons,
    img_dropdown,
)

from htpy import div, blockquote, img, small, label, form, Element, tr, td, a, li


def transaksi_form(
    transaksi=None,
    lock: bool = False,
    lapak=None,
    ternak=None,
    iot=None,
) -> Element:
    if not transaksi:
        tanggal = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat()[:16]

    waktu_kirim_input = inlabel(
        "Waktu Kirim",
        "datetime-local",
        "waktu_kirim",
        (transaksi.waktu_kirim if transaksi else tanggal),
        lock,
    )
    if lock:
        form_btn = edit_btn("/transaksi/", transaksi.id)
        lapak_input = inlabel("Lapak", "text", "lapak_id", transaksi.lapak.name, lock)
        ternak_input = label[
            small["Ternak"], show_img("img_ternak/" + transaksi.ternak.img)
        ]
        iot_input = inlabel("IoT", "text", "iot_id", transaksi.iot.node, lock)
    else:
        lapak_input = combo_gen(
            "Lapak",
            "lapak_id",
            lapak,
            (transaksi.lapak_id if transaksi else None),
            "Pilih Lapak",
        )
        ternak_input = img_dropdown(
            "Pilih Ternak",
            "ternak_id",
            "/files/img_ternak/",
            (ternak if ternak else None),
            (transaksi.ternak_id if transaksi else None),
            extra_li=li[a(href="/ternak/new")["+ Tambah Ternak Baru"]],
            extra_text="Ternak dari ",
        )
        iot_input = combo_gen(
            "IoT",
            "iot_id",
            iot,
            (transaksi.iot_id if transaksi else None),
            "Pilih IoT",
            "node",
        )
        form_btn = update_btn("/transaksi/", transaksi.id) if transaksi else submit_btn

    return form(
        "#form", action="/transaksi/", method="post", enctype="multipart/form-data"
    )[
        ternak_input,
        inlabel(
            "Jumlah", "number", "jumlah", (transaksi.jumlah if transaksi else ""), lock
        ),
        lapak_input,
        iot_input,
        waktu_kirim_input,
        form_btn,
    ]


def transaksis_table(transaksis) -> Element:
    col_headers = ["No. Transaksi", "Lapak", "Status", "Actions"]
    rows = (
        tr[
            td(style="width: 50px;")[img(".full", src=f"/qr/{transaksi.id}")],
            td[transaksi.lapak.name],
            td[transaksi.status_kirim],
            td[
                secure_action_buttons(
                    "transaksi",
                    transaksi.id,
                    "ini",
                    extra_1=a(
                        ".outline.secondary",
                        role="button",
                        href=f"/print/qr/{transaksi.id}",
                    )["Print QR"],
                )
            ],
        ]
        for transaksi in transaksis
    )

    return table_builder(col_headers, rows)


def unauthorized(prev_link):
    return div[a(href=prev_link)["← Kembali ke tabel user"], blockquote["Unauthorized"]]
