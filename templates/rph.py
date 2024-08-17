from templates.base_template import base_page
from templates.components import table_builder, drawer_menu
from htpy import (
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


def rphs_page(rphs) -> Element:
    return base_page(
        page_title="RPH",
        extra_head=[
            link(rel="stylesheet", href="/static/datatable.style.css"),
            script(src="/static/simple-datatables.904.js"),
        ],
        content=[
            drawer_menu(),
            div(style="margin-top: 4em;")[
                h1["RPH"],
                a(role="button", href="/rph/new")["+ rph"],
                rphs_table(rphs),
                script(src="/static/script.js"),
            ]
        ]
    )


def rph_detail(rph=None, lock: bool = False) -> Element:
    return base_page(
        page_title="RPH",
        content=[
            drawer_menu(),
            div(style="margin: 4em 0;")[
                h1["Tambah rph"],
                rph_form(rph, lock),
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


def rph_form(rph, lock: bool = False) -> Element:
    if lock:
        sertifikat = show_img("sert_rph/" + rph.file_sertifikasi)

        form_btn = edit_btn("/rph/", rph.id)
    else:
        sertifikat = file_input((rph.file_sertifikasi if rph else ""),
                                "file_sertifikasi", lock)
        if rph is not None:
            form_btn = update_btn("/rph/", rph.id)
        else:
            form_btn = submit_btn

    return form(
        "#form",
        action="/rph",
        method="post",
        enctype="multipart/form-data"
    )[
        img(".htmx-indicator", src="/static/indicator.gif"),
        inlabel("Nama", "text", "name",
                (rph.name if rph else ""),
                lock),
        inlabel("Alamat", "text", "alamat",
                (rph.alamat if rph else ""),
                lock),
        inlabel("Telepon", "text", "telepon",
                (rph.telepon if rph else ""),
                lock),
        inlabel("Status Sertifikasi", "text", "status_sertifikasi",
                (rph.status_sertifikasi if rph else ""),
                lock),
        label[
            small["Sertifikat"],
            sertifikat
        ],
        form_btn
    ]


def rphs_table(rphs) -> Element:
    return div("#table-wrapper")[
        table_builder(
            ["Nama", "Alamat", "Telepon", "Status Sertifikasi", "Actions"],
            (a[tr[
                td[rph.name],
                td[rph.alamat],
                td[rph.telepon],
                td[rph.status_sertifikasi],
                td[
                    div(".table-actions", role="group")[
                        a(href="/rph/" + str(rph.id))["Detail"],
                        a(href="/rph/edit/" + str(rph.id))["Edit"],
                        a(
                            hx_delete="/rph/" + str(rph.id),
                            hx_confirm=f"""
Apakah anda yakin mau menghapus data {rph.name}?
                            """,
                            hx_target="#table-wrapper"
                        )["Hapus"],
                    ]
                ],
            ]] for rph in rphs)
        )
    ]
