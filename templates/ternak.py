from templates.components import (
    table_builder,
    show_img,
    edit_btn,
    inlabel,
    file_input,
    combo_gen,
    update_btn,
    submit_btn,
)

from htpy import (
    select,
    option,
    form,
    div,
    img,
    h1,
    button,
    input,
    Element,
    tr,
    td,
    link,
    script,
    a,
    label,
    small,
)


def ternaks_page(ternaks) -> Element:
    return base_page(
        page_title="ternak",
        extra_head=[
            link(rel="stylesheet", href="/static/datatable.style.css"),
            script(src="/static/simple-datatables.904.js"),
        ],
        content=[
            drawer_menu(),
            div(style="margin-top: 4em;")[
                h1["ternak"],
                a(role="button", href="/ternak/new")["+ ternak"],
                ternaks_table(ternaks),
                script(src="/static/script.js"),
            ]
        ]
    )


def ternak_detail(ternak=None, julehas=None, peternaks=None,
                  lock: bool = False) -> Element:
    return base_page(
        page_title="ternak",
        content=[
            drawer_menu(),
            div(style="margin: 4em 0;")[
                h1["Tambah ternak"],
                ternak_form(ternak, julehas, peternaks, lock),
            ]
        ]
    )


def ternak_form(
    ternak=None, julehas=None, peternaks=None, lock: bool = False
) -> Element:
    if lock:
        form_btn = edit_btn("/ternak", ternak.id)
        juleha_combo = inlabel(
            "Juleha", "text", "juleha_id",
            ternak.juleha.name, lock
        )
        peternak_combo = inlabel(
            "Peternak", "text", "peternak_id",
            ternak.peternak.name, lock
        )
    else:
        juleha_combo = combo_gen(
            "Juleha", "juleha_id", julehas,
            (ternak.juleha_id if ternak else None),
            (None if ternak else "Pilih Juleha")
        )
        peternak_combo = combo_gen(
            "Peternak", "peternak_id", peternaks,
            (ternak.peternak_id if ternak else None),
            (None if ternak else "Pilih Peternak")
        )
        if ternak is not None:
            form_btn = update_btn("/ternak/", ternak.id)
        else:
            form_btn = submit_btn

    return form(
        "#form",
        action="/ternak",
        method="post",
        enctype="multipart/form-data",
        autocomplete="off"
    )[
        img(".htmx-indicator", src="/static/indicator.gif"),
        inlabel("Tag", "text", "name",
                (ternak.name if ternak else ""), lock),
        label[
            small["Bobot"],
            input(
                type_="text",
                name="bobot",
                disabled=lock,
                value=(ternak.bobot if ternak else "")
            ),
        ],
        label[
            small["Jenis"],
            input(
                type_="text",
                name="jenis",
                disabled=lock,
                value=(ternak.jenis if ternak else "")
            ),
        ],
        label[
            small["Kesehatan"],
            input(
                type_="text",
                name="kesehatan",
                disabled=lock,
                value=(ternak.kesehatan if ternak else "")
            ),
        ],
        juleha_combo,
        peternak_combo,
        inlabel("Waktu Disembelih", "datetime-local", "waktu_sembelih",
                (ternak.waktu_sembelih if ternak else ""),
                lock),
        form_btn
    ]


def ternaks_table(ternaks) -> Element:
    col_headers = [
        "Bobot", "Jenis", "Kesehatan",
        "Peternak", "Juleha", "Actions"
    ]
    rows = (tr[
        td[str(ternak.bobot) + "kg"],
        td[ternak.jenis],
        td[ternak.kesehatan],
        td[ternak.peternak.name],
        td[ternak.juleha.name],
        td[
            div(".table-actions", role="group")[
                a(href="/ternak/" + str(ternak.id))["Detail"],
                a(href="/ternak/edit/" + str(ternak.id))["Edit"],
                a(
                    hx_delete="/ternak/" + str(ternak.id),
                    hx_confirm=f"""
Apakah anda yakin mau menghapus data {ternak.id}?
                    """,
                    hx_target="#table-wrapper"
                )["Hapus"],
            ]
        ],
    ] for ternak in ternaks)

    return table_builder(col_headers, rows)
