from templates.components import (
    table_builder,
    show_img,
    edit_btn,
    file_input,
    update_btn,
    submit_btn,
    inlabel,
    action_buttons,
)
from htpy import (
    form,
    div,
    img,
    Element,
    tr,
    td,
    label,
    small,
)


def rph_form(rph=None, lock: bool = False) -> Element:
    if lock:
        form_btn = edit_btn("/rph/", rph.id)
        sertifikat = show_img("sert_rph/" + rph.file_sertifikasi)
    else:
        sertifikat = file_input(
            (rph.file_sertifikasi if rph else ""), "file_sertifikasi", lock
        )

        if rph is not None:
            form_btn = update_btn("/rph/", rph.id)
        else:
            form_btn = submit_btn

    return form("#form", action="/rph", method="post", enctype="multipart/form-data")[
        inlabel("Nama", "text", "name", (rph.name if rph else ""), lock),
        inlabel("Alamat", "text", "alamat", (rph.alamat if rph else ""), lock),
        inlabel("Telepon", "text", "telepon", (rph.telepon if rph else ""), lock),
        inlabel(
            "Status Sertifikasi",
            "text",
            "status_sertifikasi",
            (rph.status_sertifikasi if rph else ""),
            lock,
        ),
        label[small["Sertifikat"], sertifikat],
        form_btn,
    ]


def rphs_table(rphs) -> Element:
    tbl_headers = ["Nama", "Alamat", "Telepon", "Status Sertifikasi", "Actions"]
    rows = (
        [
            tr[
                td[rph.name],
                td[rph.alamat],
                td[rph.telepon],
                td[rph.status_sertifikasi],
                td[action_buttons("rph", rph.id, rph.name)],
            ]
        ]
        for rph in rphs
    )

    return table_builder(tbl_headers, rows)
