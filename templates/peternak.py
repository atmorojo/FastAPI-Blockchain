from templates.components import (
    table_builder,
    edit_btn,
    inlabel,
    update_btn,
    submit_btn,
    action_buttons,
    dropdown_gen,
)
from htpy import (
    Element,
    form,
    td,
    tr,
)


def peternak_form(peternak=None, lock: bool = False) -> Element:
    if lock:
        form_btn = edit_btn("/peternak/", peternak.id)
        status_usaha = inlabel("Status Usaha", "text", "status_usaha",
                               (peternak.status_usaha if peternak else ""),
                               lock),
    else:
        status_usaha = dropdown_gen(
            "Status Usaha", "status_usaha",
            ["Mandiri", "Badan Usaha"],
            (peternak.status_usaha if peternak else None)
        )
        if peternak is not None:
            form_btn = update_btn("/peternak/", peternak.id)
        else:
            form_btn = submit_btn

    return form(
        "#form",
        method="post",
        action="/peternak",
        autocomplete="off",
        enctype="multipart/form-data"
    )[
        inlabel("Nama", "text", "name",
                (peternak.name if peternak else ""), lock),
        inlabel("Alamat", "text", "alamat",
                (peternak.alamat if peternak else ""), lock),
        status_usaha,
        form_btn
    ]


def peternak_table(peternaks) -> Element:
    tbl_headers = ["Nama", "Alamat", "Status Usaha", "Actions"]
    rows = ([tr[
        td[peternak.name],
        td[peternak.alamat],
        td[peternak.status_usaha],
        td[action_buttons("peternak", peternak.id, peternak.name)],
    ]] for peternak in peternaks)

    return table_builder(tbl_headers, rows)
