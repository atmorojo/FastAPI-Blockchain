from templates.base_template import base_page
from templates.components import table_builder, drawer_menu
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


def penyelias_page(penyelias) -> Element:
    return base_page(
        page_title="Penyelia",
        extra_head=[
            link(rel="stylesheet", href="/static/datatable.style.css"),
            script(src="/static/simple-datatables.904.js"),
        ],
        content=[
            drawer_menu(),
            div(style="margin-top: 4em;")[
                h1["Penyelia"],
                a(role="button", href="/penyelia/new")["+ penyelia"],
                penyelias_table(penyelias),
                script(src="/static/script.js"),
            ]
        ]
    )


def penyelia_detail(penyelia=None, rph=None, lock: bool = False) -> Element:
    return base_page(
        page_title="Penyelia",
        content=[
            drawer_menu(),
            div(style="margin: 4em 0;")[
                h1["Tambah penyelia"],
                penyelia_form(penyelia, rph, lock),
            ]
        ]
    )


def update_btn(parent_route, id):
    return button(
        ".full",
        hx_put=parent_route + str(id),
        hx_target="#form",
        hx_indicator="#form",
        hx_encoding="multipart/form-data",
        hx_push_url="true"
    )["Simpan Perubahan"]


def file_input(_value, _name, lock):
    return input(
        type_="file",
        name=_name,
        value=_value,
        disabled=lock,
    )


def edit_btn(parent_route, id):
    return button(
        ".full",
        hx_get=parent_route + "edit/" + str(id),
        hx_target="#form",
        hx_push_url="true"
    )["Edit"]


submit_btn = input(type_="submit", value="Simpan")


def show_img(url):
    return img(".full", src="/files/" + url)


def inlabel(_label, _type, _name, _value, lock):
    return label[
        small[_label],
        input(type_=_type, name=_name, disabled=lock, value=_value),
    ],


def combo_gen(label_text, name, items, selected=None, placeholder=None):
    return label[
        small[label_text],
        select(name=name)[
            (option(
                value="", disabled=True, selected=True, hidden=True
            )[placeholder] if placeholder else None),
            (option(
                value=item.id,
                selected=(item.id == selected)
            )[item.name] for item in items)
        ]
    ]


def penyelia_form(penyelia, rph, lock: bool = False) -> Element:
    if lock:
        file_sk = show_img("sk_penyelia/" + penyelia.file_sk)
        form_btn = edit_btn("/penyelia/", penyelia.id)
        rph_combo = inlabel("RPH", "text", "rph_id", penyelia.rph.name, True)
    else:
        file_sk = file_input(
            (penyelia.file_sk if penyelia else ""),
            "file_sk", lock)
        rph_combo = combo_gen(
            "RPH",
            "rph_id",
            rph,
            (penyelia.rph_id if penyelia else None),
            (None if penyelia else "Pilih RPH")
        )
        if penyelia is not None:
            form_btn = update_btn("/penyelia/", penyelia.id)
        else:
            form_btn = submit_btn

    return form(
        "#form",
        action="/penyelia",
        method="post",
        enctype="multipart/form-data"
    )[
        img(".htmx-indicator", src="/static/indicator.gif"),
        inlabel("NIP", "text", "nip",
                (penyelia.nip if penyelia else ""),
                lock),
        inlabel("Nama", "text", "name",
                (penyelia.name if penyelia else ""),
                lock),
        inlabel("Status", "text", "status",
                (penyelia.status if penyelia else ""),
                lock),
        inlabel("Tanggal Berlaku", "date", "tgl_berlaku",
                (penyelia.tgl_berlaku if penyelia else ""),
                lock),
        rph_combo,
        label[
            small["File SK"],
            file_sk
        ],
        form_btn
    ]


def penyelias_table(penyelias) -> Element:
    return div("#table-wrapper")[
        table_builder(
            ["NIP", "Nama", "Status", "RPH", "Actions"],
            (a[tr[
                td[penyelia.nip],
                td[penyelia.name],
                td[penyelia.status],
                td[penyelia.rph.name],
                td[
                    div(".table-actions", role="group")[
                        a(href="/penyelia/" + str(penyelia.id))["Detail"],
                        a(href="/penyelia/edit/" + str(penyelia.id))["Edit"],
                        a(
                            hx_delete="/penyelia/" + str(penyelia.id),
                            hx_confirm=f"""
Apakah anda yakin mau menghapus data {penyelia.name}?
                            """,
                            hx_target="#table-wrapper"
                        )["Hapus"],
                    ]
                ],
            ]] for penyelia in penyelias)
        )
    ]
