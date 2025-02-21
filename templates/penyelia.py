from templates.components import (
    table_builder,
    show_img,
    edit_btn,
    inlabel,
    file_input,
    combo_gen,
    update_btn,
    submit_btn,
    action_buttons,
)

from htpy import (
    form,
    Element,
    tr,
    td,
    label,
    small,
)


def penyelia_form(penyelia, rph, admin, lock: bool = False) -> Element:
    if lock:
        file_sk = show_img("sk_penyelia/" + penyelia.file_sk)
        form_btn = edit_btn("/penyelia/", penyelia.id)
        rph_combo = inlabel("RPH", "text", "rph_id", penyelia.rph.name, True)
    else:
        file_sk = file_input((penyelia.file_sk if penyelia else ""), "file_sk", lock)
        rph_combo = combo_gen(
            "RPH",
            "rph_id",
            rph,
            admin,
            # (penyelia.rph_id if penyelia else None),
            (None if penyelia else "Pilih RPH"),
        )
        if penyelia is not None:
            form_btn = update_btn("/penyelia/", penyelia.id)
        else:
            form_btn = submit_btn

    return form(
        "#form", action="/penyelia/", method="post", enctype="multipart/form-data"
    )[
        inlabel("NIP", "text", "nip", (penyelia.nip if penyelia else ""), lock),
        inlabel("Nama", "text", "name", (penyelia.name if penyelia else ""), lock),
        inlabel(
            "Status", "text", "status", (penyelia.status if penyelia else ""), lock
        ),
        inlabel(
            "Tanggal Berlaku",
            "date",
            "tgl_berlaku",
            (penyelia.tgl_berlaku if penyelia else ""),
            lock,
        ),
        rph_combo,
        label[small["File SK"], file_sk],
        form_btn,
    ]


def penyelias_table(penyelias) -> Element:
    col_headers = ["NIP", "Nama", "Status", "RPH", "Actions"]
    rows = (
        tr[
            td[penyelia.nip],
            td[penyelia.name],
            td[penyelia.status],
            td[penyelia.rph.name],
            td[action_buttons("penyelia", penyelia.id, penyelia.name)],
        ]
        for penyelia in penyelias
    )

    return table_builder(col_headers, rows)
