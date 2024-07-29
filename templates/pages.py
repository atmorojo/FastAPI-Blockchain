from templates.base_template import base_page
from templates.components import navbar, table_builder
from htpy import (
    form,
    div,
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
                    button(".login")["Sign in"]
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
            div(style="margin-top: 4em;")[
                h1["Dashboard"],
                p["Selamat datang, user"],
            ],
            navbar()
        ]
    )



def julehas_table(julehas) -> Element:
    return base_page(
        page_title="Juleha",
        extra_head=[
            link(rel="stylesheet", href="/static/datatable.style.css"),
            script(src="/static/simple-datatables.904.js"),
        ],
        content=[
            div(style="margin-top: 4em;")[
                h1["Juleha"],
                table_builder(
                    ["No", "Nama"],
                    (a[tr[
                        td[str(juleha.id)],
                        td[juleha.name]
                    ]] for juleha in julehas)
                )
            ],
            navbar(),
            script(src="/static/script.js"),
        ]
    )
