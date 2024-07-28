from templates.base_template import base_page
from templates.components import navbar
from htpy import (
    form,
    div,
    h1,
    button,
    p,
    input,
    Element
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
