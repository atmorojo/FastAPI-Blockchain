from templates.base_template import base_page
from templates.components import table_builder, drawer_menu, inlabel
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
    if lock is False:
        if ternak is not None:
            form_btn = button(
                ".full",
                hx_put="/ternak/" + str(ternak.id),
                hx_target="#form",
                hx_indicator="#form",
                hx_encoding="multipart/form-data",
                hx_push_url="true"
            )["Simpan Perubahan"]

            juleha_combo = select(name="juleha_id")[
                (option(
                    value=juleha.id,
                    selected=(juleha.id == ternak.juleha_id)
                )[juleha.name] for juleha in julehas)
            ]
            peternak_combo = select(name="peternak_id")[
                (option(
                    value=peternak.id,
                    selected=(peternak.id == ternak.peternak_id)
                )[peternak.name] for peternak in peternaks)
            ]
        else:
            form_btn = input(type_="submit", value="Simpan")
            juleha_combo = select(name="juleha_id")[
                option(value="", disabled=True, selected=True, hidden=True)[
                    "Pilih Juleha"],
                (option(value=juleha.id)[juleha.name] for juleha in julehas)
            ]
            peternak_combo = select(name="peternak_id")[
                option(value="", disabled=True, selected=True, hidden=True)[
                    "Pilih Peternak"],
                (option(value=peternak.id)[peternak.name] for peternak in
                 peternaks)
            ]

    else:
        form_btn = button(
            ".full",
            hx_get="/ternak/edit/" + str(ternak.id),
            hx_target="#form",
            hx_push_url="true"
        )["Edit"]

        juleha_combo = input(
            type_="text", value=ternak.juleha.name, disabled=True)
        peternak_combo = input(
            type_="text", value=ternak.peternak.name, disabled=True)

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
        label[
            small["Juleha"],
            juleha_combo
        ],
        label[
            small["Peternak"],
            peternak_combo
        ],
        form_btn
    ]


def ternaks_table(ternaks) -> Element:
    return div("#table-wrapper")[
        table_builder(
            ["Bobot", "Jenis", "Kesehatan", "Peternak", "Juleha", "Actions"],
            (a[tr[
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
            ]] for ternak in ternaks)
        )
    ]
