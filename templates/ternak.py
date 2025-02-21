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
    a,
    form,
    Element,
    tr,
    td,
    script,
    label,
    small,
)


def ternak_form(ternak=None, peternaks=None, lock: bool = False) -> Element:
    if lock:
        form_btn = edit_btn("/ternak/", ternak.id)
        picture = show_img("img_ternak/" + (ternak.img or ""))
        peternak_combo = inlabel(
            "Pemilik Ternak", "text", "peternak_id", ternak.peternak.name, lock
        )
        jenis = inlabel(
            "Jenis", "text", "jenis", (ternak.jenis if ternak else ""), lock
        )
    else:
        picture = file_input((ternak.img if ternak else ""), "img", lock)
        peternak_combo = combo_gen(
            "Pemilik Ternak",
            "peternak_id",
            peternaks,
            (ternak.peternak_id if ternak else None),
            (None if ternak else "Pilih Peternak"),
        )
        jenis = dropdown_gen(
            "Jenis Ternak",
            "jenis",
            ["Kambing", "Sapi", "Domba", "Kerbau"],
            (ternak.jenis if ternak else None),
        )
        if ternak is not None:
            form_btn = update_btn("/ternak/", ternak.id)
        else:
            form_btn = submit_btn

    return form(
        "#form",
        action="/ternak/",
        method="post",
        enctype="multipart/form-data",
        autocomplete="off",
    )[
        label[small["Gambar"], picture],
        inlabel(
            "Bobot",
            "number",
            "bobot",
            (ternak.bobot if ternak else ""),
            lock,
            True,
            placeholder="Kg",
        ),
        jenis,
        peternak_combo,
        form_btn,
        script(src="/static/compress_logic.js", type_="module"),
    ]


def sembelih_form(
    ternak=None, julehas=None, penyelias=None, lock: bool = False
) -> Element:
    """
    TODO: Tambah field waktu_sembelih jika waktu_sembelih sudah ter-set
    """

    if ternak.waktu_sembelih is not None:
        waktu_sembelih = (
            inlabel(
                "Disembelih pada",
                "date",
                "waktu_sembelih",
                ternak.waktu_sembelih,
                lock,
                True,
            ),
        )
    else:
        waktu_sembelih = ""
    picture = show_img("img_ternak/" + (ternak.img or ""))
    if lock:
        form_btn = edit_btn("/ternak/proses/", ternak.id)
        juleha_combo = inlabel("Juleha", "text", "juleha_id", ternak.juleha.name, lock)
        penyelia_combo = inlabel(
            "penyelia", "text", "penyelia_id", ternak.penyelia.name, lock
        )
        kesehatan = inlabel("Kesehatan", "text", "kesehatan", ternak.kesehatan, lock)
    else:
        juleha_combo = combo_gen(
            "Juleha",
            "juleha_id",
            julehas,
            (ternak.juleha_id if ternak.juleha_id else None),
            (None if ternak.juleha_id else "Pilih Juleha"),
        )
        penyelia_combo = combo_gen(
            "Penyelia",
            "penyelia_id",
            penyelias,
            (ternak.penyelia_id if ternak.penyelia_id else None),
            (None if ternak.penyelia_id else "Pilih penyelia"),
        )
        kesehatan = dropdown_gen(
            "Kesehatan",
            "kesehatan",
            ["Sehat", "Layak"],
            (ternak.kesehatan if ternak.kesehatan else None),
            placeholder=(None if ternak.kesehatan else "Status kesehatan"),
        )
        if ternak is not None:
            form_btn = update_btn("/ternak/proses/", ternak.id)
        else:
            form_btn = submit_btn

    return form(
        "#form",
        action=f"/ternak/proses/{(ternak.id or '')}",
        method="post",
        enctype="multipart/form-data",
        autocomplete="off",
    )[
        label[small["Gambar"], picture],
        inlabel(
            "Karkas",
            "number",
            "karkas",
            (ternak.karkas if ternak else ""),
            lock,
            True,
            placeholder="Kg",
        ),
        kesehatan,
        juleha_combo,
        penyelia_combo,
        waktu_sembelih,
        form_btn,
    ]


def ternaks_table(ternaks) -> Element:
    col_headers = ["Foto", "Bobot", "Karkas", "Jenis", "Antrian", "Actions"]
    rows = (
        tr[
            td(style="width: 50px;")[
                show_img("img_ternak/" + (ternak.img if ternak.img else ""))
            ],
            td[str(ternak.bobot) + " Kg"],
            td[str(ternak.karkas or "-") + " Kg"],
            td[ternak.jenis],
            td[f"{ternak.waktu_daftar[5:]} {(int(ternak.no_antri or 0)):03}"],
            td[
                action_buttons(
                    "ternak",
                    ternak.id,
                    "ini",
                    extra_1=a(
                        disabled=(True if ternak.waktu_sembelih else False),
                        role="button",
                        href=f"/ternak/proses/edit/{ternak.id}",
                    )[("Sudah disembelih" if ternak.waktu_sembelih else "Sembelih")],
                )
            ],
        ]
        for ternak in ternaks
    )

    return table_builder(col_headers, rows)
