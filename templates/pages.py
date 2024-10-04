from templates.base_template import base_page
from templates.components import navbar
from htpy import (
    span,
    svg,
    rect,
    img,
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


def dashboard_page(user) -> Element:
    return base_page(
        page_title="Dashboard",
        content=[
            navbar,
            div(style="margin-top: 4em;")[
                h1["Dashboard"],
                p[f"Selamat datang, {user.username.title()}"],
            ],
        ]
    )


def table_page(title, datatable, button=True) -> Element:
    if button:
        add_button = a(
            "#tambah-button",
            role="button",
            href="/" + title.lower() + "/new"
        )[svg(".plus", viewBox="0 0 100 100")[
            rect(".plus-sign",
                 x="40", y="10",
                 width="20", height="80"),
            rect(".plus-sign",
                 x="10", y="40",
                 width="80", height="20")
            ], span[f"tambah {title} baru".title()]
          ]
    else:
        add_button = ""

    return base_page(
        page_title="APDH" + (" | " + title.title() if title else ""),
        extra_head=[
            link(rel="stylesheet", href="/static/datatable.style.css"),
            script(src="/static/simple-datatables.904.js"),
        ],
        content=[
            navbar,
            div(style="margin-top: 4em;")[
                div(style="""
                    display: flex;
                    justify-content: space-between;
                    margin: 2em 0;
                    """)[
                    h1["Master " + title.title()],
                    add_button,
                ],
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
            navbar,
            div(style="margin: 4em 0;")[
                a(style="""
                text-decoration:none;
                margin: 1em 0;
                display: inline-block;
                """,
                  href=f"/{title.lower()}")[f"← Kembali ke daftar {title}"],
                h1[title.title()],
                img(".my-indicator", src="/static/indicator.gif"),
                detail_form,
            ]
        ]
    )
