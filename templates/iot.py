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


def iot_form(iot=None, lock: bool = False, rph=None) -> Element:
    if lock:
        form_btn = edit_btn("/iot/", iot.id)
        rph_input = inlabel("rph", "text", "rph_id", iot.rph.name, lock)
    else:
        rph_input = combo_gen(
            "rph", "rph_id", rph,
            (iot.rph_id if iot else None),
            "Pilih RPH"
        )
        form_btn = (update_btn(
            "/iot/", iot.id
        ) if iot else submit_btn)

    return form(
        "#form",
        action="/iot",
        method="post",
        enctype="multipart/form-data"
    )[
        img(".htmx-indicator", src="/static/indicator.gif"),
        inlabel("Node", "text", "node",
                (iot.node if iot else ""),
                lock),
        rph_input,
        form_btn
    ]


def iots_table(iots) -> Element:
    col_headers = ["Node", "RPH", "Actions"]
    rows = (tr[
                td[iot.node],
                td[iot.rph.name],
                td[
                    div(".table-actions", role="group")[
                        a(href="/iot/" + str(iot.id))["Detail"],
                        a(href="/iot/edit/" + str(iot.id))["Edit"],
                        a(
                            hx_delete="/iot/" + str(iot.id),
                            hx_confirm=f"""
Apakah anda yakin mau menghapus data {iot.node}?
                            """,
                            hx_target="#table-wrapper"
                        )["Hapus"],
                    ]
                ],
            ] for iot in iots)

    return table_builder(
        col_headers,
        rows
        )
