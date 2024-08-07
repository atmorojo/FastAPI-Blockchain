from templates.base_template import base_page
from templates.components import table_builder, drawer_menu
from htpy import (
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


def peternaks_page(peternaks) -> Element:
    return base_page(
        page_title="peternak",
        extra_head=[
            link(rel="stylesheet", href="/static/datatable.style.css"),
            script(src="/static/simple-datatables.904.js"),
        ],
        content=[
            drawer_menu(),
            div(style="margin-top: 4em;")[
                h1["peternak"],
                a(role="button", href="/peternaks/new")["+ peternak"],
                peternaks_table(peternaks),
                script(src="/static/script.js"),
            ]
        ]
    )


def peternak_detail(peternak=None, lock: bool = False) -> Element:
    return base_page(
        page_title="peternak",
        content=[
            drawer_menu(),
            div(style="margin: 4em 0;")[
                h1["Tambah peternak"],
                peternak_form(peternak, lock),
            ]
        ]
    )


def peternak_form(peternak=None, lock: bool = False) -> Element:
    if lock is False:
        if peternak is not None:
            form_btn = button(
                ".full",
                hx_put="/peternaks/" + str(peternak.id),
                hx_target="#form",
                hx_indicator="#form",
                hx_encoding="multipart/form-data",
                hx_push_url="true"
            )["Simpan Perubahan"]
        else:
            form_btn = input(type_="submit", value="Simpan")
    else:
        form_btn = button(
            ".full",
            hx_get="/peternaks/edit/" + str(peternak.id),
            hx_target="#form",
            hx_push_url="true"
        )["Edit"]

    return form(
        "#form",
        action="/peternaks",
        method="post",
        enctype="multipart/form-data"
    )[
        img(".htmx-indicator", src="/static/indicator.gif"),
        label[
            small["Nama"],
            input(
                type_="text",
                name="name",
                disabled=lock,
                value=(peternak.name if peternak else "")
            ),
        ],
        label[
            small["Alamat"],
            input(
                type_="text",
                name="alamat",
                disabled=lock,
                value=(peternak.alamat if peternak else "")
            ),
        ],
        label[
            small["Status Usaha"],
            input(
                type_="text",
                name="status_usaha",
                disabled=lock,
                value=(peternak.status_usaha if peternak else "")
            ),
        ],
        form_btn
    ]


def peternaks_table(peternaks) -> Element:
    return div("#table-wrapper")[
        table_builder(
            ["Nama", "Alamat", "Status Usaha", "Actions"],
            (a[tr[
                td[peternak.name],
                td[peternak.alamat],
                td[peternak.status_usaha],
                td[
                    div(".table-actions", role="group")[
                        a(href="/peternaks/" + str(peternak.id))["Detail"],
                        a(href="/peternaks/edit/" + str(peternak.id))["Edit"],
                        a(
                            hx_delete="/peternaks/" + str(peternak.id),
                            hx_confirm=f"""
Apakah anda yakin mau menghapus data {peternak.name}?
                            """,
                            hx_target="#table-wrapper"
                        )["Hapus"],
                    ]
                ],
            ]] for peternak in peternaks)
        )
    ]
