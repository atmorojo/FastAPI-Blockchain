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

