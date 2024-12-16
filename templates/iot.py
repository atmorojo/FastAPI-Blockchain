from templates.components import (
    table_builder,
    edit_btn,
    inlabel,
    update_btn,
    submit_btn,
    action_buttons,
)

from htpy import (
    form,
    img,
    Element,
    tr,
    td,
)


def iot_form(iot=None, lock: bool = False) -> Element:
    if lock:
        form_btn = edit_btn("/iot/", iot.id)
    else:
        form_btn = update_btn("/iot/", iot.id) if iot else submit_btn

    return form("#form", action="/iot", method="post", enctype="multipart/form-data")[
        img(".htmx-indicator", src="/static/indicator.gif"),
        inlabel("Node", "text", "node", (iot.node if iot else ""), lock),
        form_btn,
    ]


def iots_table(iots) -> Element:
    col_headers = ["Node", "Actions"]
    rows = (
        tr[
            td[iot.node],
            td[action_buttons("iot", iot.id, iot.node)],
        ]
        for iot in iots
    )

    return table_builder(col_headers, rows)
