from htpy import (
    render_node,
    ul,
    aside,
    li,
    a,
    header,
    nav,
    span,
    Element,
    table,
    label,
    thead,
    tbody,
    th,
    tr,
    input
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


def drawer_menu() -> Element:
    return render_node([
        input(
            "#burger-btn.burger-btn",
            type_="checkbox",
        ),
        label(".burger-icon", for_="burger-btn")[
            span,
            span,
            span
        ],
        aside(".nav-drawer")[nav[ul[
            li[a(href="/dashboard")["Dashboard"]],
            li[a(href="/julehas")["Juleha"]],
            li[a(href="#")["Peternak"]],
            li[a(href="#")["Ternak"]],
        ]]]
    ])
