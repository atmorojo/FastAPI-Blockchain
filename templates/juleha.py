from templates.components import (
    table_builder,
    edit_btn,
    inlabel,
    update_btn,
    submit_btn,
    show_img,
    file_input,
    action_buttons,
)

from htpy import (
    form,
    div,
    Element,
    tr,
    td,
    label,
    small,
)


def juleha_form(juleha=None, lock: bool = False) -> Element:
    if lock:
        form_btn = edit_btn("/juleha/", juleha.id)
        sertifikat = show_img("sertifikat/" + juleha.upload_sertifikat)
    else:
        sertifikat = file_input(
            (juleha.upload_sertifikat if juleha else ""), "file_sertifikat", lock
        )
        if juleha is not None:
            form_btn = update_btn("/juleha/", juleha.id)
        else:
            form_btn = submit_btn

    return form(
        "#form", action="/juleha/", method="post", enctype="multipart/form-data"
    )[
        inlabel("Nama", "text", "name", (juleha.name if juleha else ""), lock),
        inlabel(
            "Nomor Sertifikat",
            "text",
            "nomor_sertifikat",
            (juleha.nomor_sertifikat if juleha else ""),
            lock,
        ),
        inlabel(
            "Masa Sertifikat",
            "date",
            "masa_sertifikat",
            (juleha.masa_sertifikat if juleha else ""),
            lock,
        ),
        label[small["Sertifikat"], sertifikat],
        form_btn,
    ]


def julehas_table(julehas) -> Element:
    col_headers = ["Nama", "Nomor Sertifikat", "Masa Berlaku", "Actions"]
    rows = (
        [
            tr[
                td[juleha.name],
                td[juleha.nomor_sertifikat],
                td[juleha.masa_sertifikat],
                td[action_buttons("juleha", juleha.id, juleha.name)],
            ]
        ]
        for juleha in julehas
    )

    return table_builder(col_headers, rows)
