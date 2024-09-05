from templates.components import (
    table_builder,
    edit_btn,
    inlabel,
    combo_gen,
    update_btn,
    submit_btn,
)

from htpy import (
    form,
    div,
    img,
    Element,
    tr,
    td,
    a,
)


def transaksi_form(
    transaksi=None,
    lock: bool = False,
    lapak=None,
    transportasi=None,
    penyelia=None,
    juleha=None,
    ternak=None
) -> Element:
    if lock:
        form_btn = edit_btn("/transaksi/", transaksi.id)
        transportasi_input = inlabel(
            "Transportasi", "text", "transportasi_id",
            transaksi.transportasi.name, lock)
        lapak_input = inlabel(
            "Lapak", "text", "lapak_id",
            transaksi.lapak.name, lock)
        penyelia_input = inlabel(
            "Penyelia", "text", "penyelia_id",
            transaksi.penyelia.name, lock)
        juleha_input = inlabel(
            "Juleha", "text", "juleha_id",
            transaksi.juleha.name, lock)
        ternak_input = inlabel(
            "Ternak", "text", "ternak_id",
            transaksi.ternak.name, lock)
    else:
        transportasi_input = combo_gen(
            "Transportasi", "transportasi_id",
            transportasi, (transaksi.transportasi_id if transaksi else None),
            "Pilih Transportasi"
        )
        lapak_input = combo_gen(
            "Lapak", "lapak_id",
            lapak, (transaksi.lapak_id if transaksi else None),
            "Pilih Lapak"
        )
        penyelia_input = combo_gen(
            "Penyelia", "penyelia_id",
            penyelia, (transaksi.penyelia_id if transaksi else None),
            "Pilih Penyelia"
        )
        juleha_input = combo_gen(
            "Juleha", "juleha_id",
            juleha, (transaksi.juleha_id if transaksi else None),
            "Pilih Juleha"
        )
        ternak_input = combo_gen(
            "Ternak", "ternak_id",
            ternak, (transaksi.ternak_id if transaksi else None),
            "Pilih Ternak"
        )
        form_btn = (update_btn(
            "/transaksi/", transaksi.id
        ) if transaksi else submit_btn)

    return form(
        "#form",
        action="/transaksi",
        method="post",
        enctype="multipart/form-data"
    )[
        img(".htmx-indicator", src="/static/indicator.gif"),
        inlabel("Jumlah", "text", "jumlah",
                (transaksi.jumlah if transaksi else ""),
                lock),
        transportasi_input,
        lapak_input,
        penyelia_input,
        juleha_input,
        ternak_input,
        form_btn
    ]


def transaksis_table(transaksis) -> Element:
    col_headers = ["Juleha", "Lapak", "Status", "Actions"]
    rows = (tr[
                td[transaksi.juleha.name],
                td[transaksi.lapak.name],
                td[transaksi.status],
                td[
                    div(".table-actions", role="group")[
                        a(href="/transaksi/" + str(transaksi.id))["Detail"],
                        a(href="/transaksi/edit/" + str(transaksi.id))["Edit"],
                        a(
                            hx_delete="/transaksi/" + str(transaksi.id),
                            hx_confirm=f"""
Apakah anda yakin mau menghapus data {transaksi.id}?
                            """,
                            hx_target="#table-wrapper"
                        )["Hapus"],
                    ]
                ],
            ] for transaksi in transaksis)

    return table_builder(
        col_headers,
        rows
        )
