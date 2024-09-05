from templates.base_template import base_page
from templates.components import drawer_menu
from htpy import (
    form,
    div,
    h1,
    button,
    p,
    input,
    Element,
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


def table_page(title, datatable) -> Element:
    return base_page(
        page_title=title,
        extra_head=[
            link(rel="stylesheet", href="/static/datatable.style.css"),
            script(src="/static/simple-datatables.904.js"),
        ],
        content=[
            drawer_menu(),
            div(style="margin-top: 4em;")[
                h1[title],
                a(
                    role="button",
                    href="/" + title.lower() + "/new"
                )["+ " + title.lower()],
                datatable,
                script(src="/static/script.js"),
            ]
        ]
    )


def detail_page(
    title,
    detail_form,
) -> Element:
    return base_page(
        page_title=title,
        content=[
            drawer_menu(),
            div(style="margin: 4em 0;")[
                h1["Tambah " + title],
                detail_form,
            ]
        ]
    )
