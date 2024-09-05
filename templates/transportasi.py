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


def transportasi_form(transportasi, lock: bool = False, rph=None) -> Element:
    if lock:
        form_btn = edit_btn("/transportasi/", transportasi.id)
        rph_input = inlabel("RPH", "text", "rph_id", transportasi.rph.name, lock)
    else:
        rph_input = combo_gen(
            "RPH",
            "rph_id",
            rph,
            (transportasi.rph_id if transportasi else None),
            "Pilh RPH"
        )
        form_btn = (update_btn(
            "/transportasi/", transportasi.id
        ) if transportasi else submit_btn)

    return form(
        "#form",
        action="/transportasi",
        method="post",
        enctype="multipart/form-data"
    )[
        img(".htmx-indicator", src="/static/indicator.gif"),
        inlabel("name", "text", "name",
                (transportasi.name if transportasi else ""),
                lock),
        rph_input,
        form_btn
    ]


def transportasis_table(transportasis) -> Element:
    col_headers = ["Nama", "Milik", "Actions"]
    rows = (tr[
                td[transportasi.name],
                td[transportasi.rph.name],
                td[
                    div(".table-actions", role="group")[
                        a(href="/transportasi/" + str(transportasi.id))["Detail"],
                        a(href="/transportasi/edit/" + str(transportasi.id))["Edit"],
                        a(
                            hx_delete="/transportasi/" + str(transportasi.id),
                            hx_confirm=f"""
Apakah anda yakin mau menghapus data {transportasi.name}?
                            """,
                            hx_target="#table-wrapper"
                        )["Hapus"],
                    ]
                ],
            ] for transportasi in transportasis)

    return table_builder(
        col_headers,
        rows
        )
