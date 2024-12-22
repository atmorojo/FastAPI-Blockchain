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


def report_juleha_table(report_data) -> Element:
    col_headers = ["Name", "Jumlah"]
    rows = (
        tr[
            td[row[0].juleha.name],
            td[str(row[1])],
            # td[action_buttons("iot", iot.id, iot.node)],
        ]
        for row in report_data
    )

    return table_builder(col_headers, rows)


def report_kiriman_table(report_data) -> Element:
    col_headers = ["Name", "Jumlah"]
    rows = (
        tr[
            td[row[0].juleha.name],
            td[str(row[1])],
            # td[action_buttons("iot", iot.id, iot.node)],
        ]
        for row in report_data
    )

    return table_builder(col_headers, rows)
