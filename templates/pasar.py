from templates.components import (
    table_builder,
    action_buttons,
    edit_btn,
    inlabel,
    update_btn,
    submit_btn,
)

from htpy import (
    form,
    Element,
    tr,
    td,
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
                td[action_buttons("pasar", pasar.id, pasar.name)],
            ] for pasar in pasars)

    return table_builder(
        col_headers,
        rows
        )
