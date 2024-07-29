from htpy import (
    ul,
    li,
    a,
    header,
    nav,
    Element,
    table,
    thead,
    tbody,
    th,
    tr,
)


def nav_link(path: str, menu: str) -> Element:
    return li(role="button")[
        a(href=path)[menu]
    ]


def navbar() -> Element:
    return header("#navbar")[
        nav[
            ul(role="group")[
                nav_link("/dashboard", "Dashboard"),
                nav_link("/profile", "Profile"),
                nav_link("/settings", "Settings"),
            ]
        ]
    ]


def table_header(headers) -> Element:
    return thead[tr[
            (th[i] for i in headers)
    ]]


def table_builder(headers, rows) -> Element:
    return table("#table")[
        table_header(headers),
        tbody[
            rows
        ]
    ]
