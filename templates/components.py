from htpy import (
    img,
    small,
    select,
    option,
    button,
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
    div,
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
    return div("#table-wrapper")[
        table("#table")[
            table_header(headers),
            tbody[
                rows
            ]
        ]
    ]


def drawer_menu() -> Element:
    return div(
        ".drawer-wrapper",
        _="""
on click from elsewhere
set #burger-btn.checked to false
        """
    )[
        input(
            "#burger-btn.burger-btn",
            type_="checkbox",
        ),
        label(".burger-icon", for_="burger-btn")[
            span,
            span,
            span
        ],
        aside(
            ".nav-drawer",
        )[nav[ul[
            li[a(href="/dashboard")["Dashboard"]],
            li[a(href="/julehas")["Juleha"]],
            li[a(href="/peternaks")["Peternak"]],
            li[a(href="/ternak")["Ternak"]],
            li[a(href="/rph")["RPH"]],
            li[a(href="/penyelia")["Penyelia"]],
        ]]]
    ]


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


def combo_gen(label_text, name, items, selected=None, placeholder=None):
    return label[
        small[label_text],
        select(name=name)[
            (option(
                value="", disabled=True, selected=True, hidden=True
            )[placeholder] if placeholder else None),
            (option(
                value=item.id,
                selected=(item.id == selected)
            )[item.name] for item in items)
        ]
    ]
