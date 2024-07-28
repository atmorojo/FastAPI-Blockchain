from htpy import (
    ul,
    li,
    a,
    header,
    nav,
    Element
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
