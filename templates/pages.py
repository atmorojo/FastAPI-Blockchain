from templates.base_template import base_page
from templates.components import table_builder, drawer_menu
from htpy import (
    form,
    div,
    img,
    h1,
    button,
    p,
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


def login_page() -> Element:
    return base_page(
        page_title="Login",
        content=[
            div(style="margin-top: 4em;")[
                form(action="/login", method="post")[
                    h1["Sign In"],
                    input(type_="text", name="username"),
                    input(type_="password", name="password"),
                    button(".full")["Sign in"]
                ]
            ],
            div("#footer")[
                "© Copyright 2024 by ",
                a(href="#")["me"]
            ]
        ]
    )


def dashboard_page() -> Element:
    return base_page(
        page_title="Dashboard",
        content=[
            drawer_menu(),
            div(style="margin-top: 4em;")[
                h1["Dashboard"],
                p["Selamat datang, user"],
            ],
        ]
    )


def julehas_table(julehas) -> Element:
    return div("#table-wrapper")[
        table_builder(
            ["No", "Nama", "Actions"],
            (a[tr[
                td[str(juleha.id)],
                td[juleha.name],
                td[
                    div(".table-actions", role="group")[
                        a(href="/julehas/" + str(juleha.id))["Detail"],
                        a()["Edit"],
                        a(
                            hx_delete="/julehas/" + str(juleha.id),
                            hx_confirm=f"""
Apakah anda yakin mau menghapus data {juleha.name}?
                            """,
                            hx_target="#table-wrapper"
                        )["Hapus"],
                    ]
                ],
            ]] for juleha in julehas)
        )
    ]


def julehas_page(julehas) -> Element:
    return base_page(
        page_title="Juleha",
        extra_head=[
            link(rel="stylesheet", href="/static/datatable.style.css"),
            script(src="/static/simple-datatables.904.js"),
        ],
        content=[
            drawer_menu(),
            div(style="margin-top: 4em;")[
                h1["Juleha"],
                a(role="button", href="/julehas/new")["+ Juleha"],
                julehas_table(julehas),
                script(src="/static/script.js"),
            ]
        ]
    )


def juleha_detail(juleha, lock: bool = False) -> Element:
    return base_page(
        page_title="Juleha",
        content=[
            div(style="margin: 4em 0;")[
                h1["Tambah Juleha"],
                juleha_form(juleha, lock),
            ]
        ]
    )


def juleha_form(juleha, lock: bool = False) -> Element:
    if lock is False:
        if juleha.id:
            form_btn = button(
                ".full",
                hx_put="/julehas/" + str(juleha.id),
                hx_target="#form",
                hx_indicator="#form",
                hx_encoding="multipart/form-data",
                hx_push_url="true"
            )["Simpan Perubahan"]
        else:
            form_btn = input(type_="submit", value="Simpan")

        sertifikat = input(
            type_="file",
            name="file_sertifikat",
            disabled=lock,
            value=(juleha.upload_sertifikat if juleha else "")
        )
    else:
        form_btn = button(
            ".full",
            hx_get="/julehas/edit/" + str(juleha.id),
            hx_target="#form",
            hx_push_url="true"
        )["Edit"]

        sertifikat = img(
            ".full",
            src="/files/sertifikat/" + juleha.upload_sertifikat
        )

    return form(
        "#form",
        action="/julehas",
        method="post",
        enctype="multipart/form-data"
    )[
        img(".htmx-indicator", src="/static/indicator.gif"),
        label[
            small["Nama"],
            input(
                type_="text",
                name="name",
                disabled=lock,
                value=(juleha.name if juleha else "")
            ),
        ],
        label[
            small["Masa Sertifikat"],
            input(
                type_="text",
                name="ms_sertifikat",
                disabled=lock,
                value=(juleha.ms_sertifikat if juleha else "")
            ),
        ],
        label[
            small["Sertifikat"],
            sertifikat
        ],
        form_btn
    ]
