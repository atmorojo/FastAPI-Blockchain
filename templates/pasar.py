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
    form,
    div,
    img,
    Element,
    tr,
    td,
    a,
    label,
    small,
)


def pasar_form(pasar, lock: bool = False) -> Element:
    if lock:
        form_btn = edit_btn("/pasar/", pasar.id)
    else:
        if pasar is not None:
            form_btn = update_btn("/pasar/", pasar.id)
        else:
            form_btn = submit_btn

    return form(
        "#form",
        action="/pasar",
        method="post",
        enctype="multipart/form-data"
    )[
        img(".htmx-indicator", src="/static/indicator.gif"),
        inlabel("Nama", "text", "name",
                (pasar.name if pasar else ""),
                lock),
        inlabel("Alamat", "text", "alamat",
                (pasar.alamat if pasar else ""),
                lock),
        form_btn
    ]


def pasars_table(pasars) -> Element:
    col_headers = ["Nama", "Alamat", "Actions"]
    rows = (tr[
                td[pasar.name],
                td[pasar.alamat],
                td[
                    div(".table-actions", role="group")[
                        a(href="/pasar/" + str(pasar.id))["Detail"],
                        a(href="/pasar/edit/" + str(pasar.id))["Edit"],
                        a(
                            hx_delete="/pasar/" + str(pasar.id),
                            hx_confirm=f"""
Apakah anda yakin mau menghapus data {pasar.name}?
                            """,
                            hx_target="#table-wrapper"
                        )["Hapus"],
                    ]
                ],
            ] for pasar in pasars)

    return table_builder(
        col_headers,
        rows
        )
