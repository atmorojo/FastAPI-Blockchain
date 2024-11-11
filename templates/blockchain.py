from templates.components import (
    table_builder,
    edit_btn,
    inlabel,
    combo_gen,
    update_btn,
    submit_btn,
    action_buttons,
    navbar
)

from htpy import (
    form,
    div,
    img,
    Element,
    tr,
    td,
    a,
    p,
    b,
    h1
)


def bc_detail(data, logged_in) -> Element:
    return div[
        navbar(is_admin=False, logged_in=logged_in),
        h1(style="margin-top: 4em; margin-bottom: 1em;")["Keterangan daging"],
        p[b["Nama RPH: "], data["rph_name"]],
        p[b["Nama Lapak: "], data["lapak_name"]],
        p[b["Pemilik Ternak: "], data["peternak_name"]],
        p[b["Juleha: "], data["juleha_name"]],
        p[b["Bobot: "], f"{data["jumlah"]} Kg"],
        p[b["Disembelih pada: "], data["waktu_sembelih"]],
        a(href=f"/sensor/end/{data["id_transaksi"]}", role="button")["Sudah Sampai"]
    ]


def lapaks_table(lapaks) -> Element:
    col_headers = ["Nama", "No Lapak", "Pasar", "Actions"]
    rows = (tr[
                td[lapak.name],
                td[lapak.no_lapak],
                td[lapak.pasar.name],
                td[action_buttons("lapak", lapak.id, lapak.name)],
            ] for lapak in lapaks)

    return table_builder(
        col_headers,
        rows
        )
