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
    dropdown_gen,
)

from htpy import (
    select,
    option,
    form,
    div,
    img,
    h1,
    button,
    input,
    Element,
    tr,
    td,
    link,
    script,
    a,
    label,
    small,
)


def ternak_form(
    ternak=None,
    julehas=None,
    peternaks=None,
    penyelias=None,
    lock: bool = False
) -> Element:
    if lock:
        form_btn = edit_btn("/ternak/", ternak.id)
        picture = show_img("img_ternak/" + ternak.img)
        juleha_combo = inlabel(
            "Juleha", "text", "juleha_id",
            ternak.juleha.name, lock
        )
        peternak_combo = inlabel(
            "Peternak", "text", "peternak_id",
            ternak.peternak.name, lock
        )
        penyelia_combo = inlabel(
            "penyelia", "text", "penyelia_id",
            ternak.penyelia.name, lock
        )

        jenis = inlabel("Jenis", "text", "jenis",
                        (ternak.jenis if ternak else ""), lock)
        kesehatan = inlabel("kesehatan", "text", "kesehatan",
                            (ternak.kesehatan if ternak else ""), lock)
    else:
        picture = file_input(
            (ternak.img if ternak else ""),
            "img", lock
        )
        juleha_combo = combo_gen(
            "Juleha", "juleha_id", julehas,
            (ternak.juleha_id if ternak else None),
            (None if ternak else "Pilih Juleha")
        )
        peternak_combo = combo_gen(
            "Peternak", "peternak_id", peternaks,
            (ternak.peternak_id if ternak else None),
            (None if ternak else "Pilih Peternak")
        )
        penyelia_combo = combo_gen(
            "Penyelia", "penyelia_id", penyelias,
            (ternak.penyelia_id if ternak else None),
            (None if ternak else "Pilih penyelia")
        )
        jenis = dropdown_gen(
            "Jenis Ternak", "jenis",
            ["Kambing", "Sapi", "Domba", "Kerbau"],
            (ternak.jenis if ternak else None))
        kesehatan = dropdown_gen(
            "Kesehatan", "kesehatan",
            ["Sehat", "Layak"],
            (ternak.kesehatan if ternak else None))
        if ternak is not None:
            form_btn = update_btn("/ternak/", ternak.id)
        else:
            form_btn = submit_btn

    return form(
        "#form",
        action="/ternak/",
        method="post",
        enctype="multipart/form-data",
        autocomplete="off"
    )[
        label[
            small["Gambar"],
            picture
        ],
        inlabel("Karkas", "number", "karkas",
                (ternak.karkas if ternak else ""), lock, True),
        jenis,
        kesehatan,
        juleha_combo,
        penyelia_combo,
        peternak_combo,
        inlabel("Waktu Disembelih", "datetime-local", "waktu_sembelih",
                (ternak.waktu_sembelih if ternak else ""),
                lock),
        form_btn,
        script(src="/static/compress_logic.js", type_="module", defer=True),
    ]


def ternaks_table(ternaks) -> Element:
    col_headers = [
        "Foto", "Karkas", "Jenis",
        "Kesehatan", "Juleha", "Actions"
    ]
    rows = (tr[
        td(style="width: 50px;")[
            show_img("img_ternak/" + (ternak.img if ternak.img else ""))],
        td[str(ternak.karkas) + "kg"],
        td[ternak.jenis],
        td[ternak.kesehatan],
        td[ternak.juleha.name],
        td[action_buttons("ternak", ternak.id, "ini")],
    ] for ternak in ternaks)

    return table_builder(col_headers, rows)
