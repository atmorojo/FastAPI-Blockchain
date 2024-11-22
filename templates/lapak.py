from templates.components import (
    table_builder,
    edit_btn,
    inlabel,
    combo_gen,
    update_btn,
    submit_btn,
    action_buttons,
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


def lapak_form(lapak=None, lock: bool = False, pasar=None) -> Element:
    if lock:
        form_btn = edit_btn("/lapak/", lapak.id)
        pasar_input = inlabel("Pasar", "text", "pasar_id", lapak.pasar.name, lock)
    else:
        pasar_input = combo_gen(
            "Pasar",
            "pasar_id",
            pasar,
            (lapak.pasar_id if lapak else None),
            "Pilih pasar",
        )
        form_btn = update_btn("/lapak/", lapak.id) if lapak else submit_btn

    return form("#form", action="/lapak", method="post", enctype="multipart/form-data")[
        img(".htmx-indicator", src="/static/indicator.gif"),
        inlabel("Nama", "text", "name", (lapak.name if lapak else ""), lock),
        inlabel(
            "No Lapak", "text", "no_lapak", (lapak.no_lapak if lapak else ""), lock
        ),
        pasar_input,
        form_btn,
    ]


def lapaks_table(lapaks) -> Element:
    col_headers = ["Nama", "No Lapak", "Pasar", "Actions"]
    rows = (
        tr[
            td[lapak.name],
            td[lapak.no_lapak],
            td[lapak.pasar.name],
            td[action_buttons("lapak", lapak.id, lapak.name)],
        ]
        for lapak in lapaks
    )

    return table_builder(col_headers, rows)
