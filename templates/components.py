from htpy import (
    Element,
    a,
    aside,
    button,
    details,
    div,
    h1,
    header,
    hr,
    img,
    input,
    label,
    li,
    nav,
    option,
    p,
    select,
    small,
    span,
    summary,
    table,
    tbody,
    th,
    thead,
    tr,
    ul,
)


def action_buttons(route, id, name):
    return div(".table-actions.full", role="group")[
      a(".outline.secondary", role="button",
        href="/" + route + "/" + str(id)
        )["Detail"],
      a(".outline.secondary", role="button",
        href="/" + route + "/edit/" + str(id)
        )["Edit"],
      a(".outline.warning", role="button",
        hx_delete="/" + route + "/" + str(id),
        hx_confirm=f"""
Apakah anda yakin mau menghapus data {name}?
        """,
        hx_target="#table-wrapper"
        )["Hapus"],
    ]


def nav_link(path: str, menu: str) -> Element:
    return li(role="button")[
        a(href=path)[menu]
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


def navbar() -> Element:
    return div(".navbar.full")[
        drawer_menu,
        a("#logout_button", href="/logout")["Log out"]
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
            div(style="width: 30px; margin-right: .5em;")[span, span, span],
            h1(
                style="""
                    color: var(--pico-form-element-color);
                    margin: 0;
                    line-height: 30px;
                    font-size: 1em;
                """
            )["APDH"],
        ],
        aside(
            ".nav-drawer",
        )[nav[ul[
            li[a(href="/dashboard")["Dashboard"]],
            li[a(href="/rph")["RPH"]],
            li[a(href="/juleha")["Juleha"]],
            li[a(href="/penyelia")["Penyelia"]],
            li[a(href="/peternak")["Peternak"]],
            li[a(href="/iot")["IoT"]],
            li[hr],
            li[a(href="/ternak")["Ternak"]],
            li[a(href="/pasar")["Pasar"]],
            li[a(href="/lapak")["Lapak"]],
            li[a(href="/transaksi")["Transaksi"]],
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
    return div[
        input(
            "#upload",
            type_="file",
            accept="image/*",
            capture="environment",
            name=_name,
            disabled=lock,
        ),
        img("#preview"),
    ]


def edit_btn(parent_route, id):
    return button(
        ".full",
        style="margin-top: 2em;",
        hx_get=parent_route + "edit/" + str(id),
        hx_target="#form",
        hx_push_url="true"
    )["Edit"]


submit_btn = input(
    style="margin-top: 2em;",
    type_="submit", value="Simpan"
)


def show_img(url):
    return img(".full", src="/files/" + url)


def spoiler(url):
    return div[
        button(
            type_="button",
            style="""
            font-size: 12px; font-weight: bold;
            height: fit-content; width: fit-content;
            padding: 5px 10px;
            """,
            _="""on click
                    toggle .show on next .spoiler
            """,
        )["Toggle Image"],
        img(".spoiler.full", src="/files/" + url)
    ]


def inlabel(_label, _type, _name, _value, lock, focus=False):
    return label[
        small[_label],
        input(autofocus=focus,
              type_=_type,
              name=_name,
              disabled=lock,
              value=_value),
    ],


def combo_gen(
        label_text, name, items,
        selected=None, placeholder=None, custom_name=None
):
    return label[
        small[label_text],
        select(name=name)[
            (option(
                value="", disabled=True, selected=True, hidden=True
            )[placeholder] if placeholder else None),
            (option(
                value=item.id,
                selected=(item.id == selected)
            )[
                (getattr(
                    item, custom_name
                )) if custom_name else item.name
            ] for item in items)
        ]
    ]


def dropdown_gen(
    label_text, name, option_items,
    selected=None, placeholder=None,
):
    return label[
        small[label_text],
        select(name=name)[
            option(
                value="", disabled=True, selected=True, hidden=True
            )[(placeholder if placeholder else f"Pilih {label_text}")],
            (option(
                value=item, selected=(item == selected)
            )[item] for item in option_items)
        ]
    ]


def img_dropdown(
    label_text, field_name,
    img_dir, items,
    selected=None,
    extra_li=None,
    extra_text=None
):
    return div[
        small[label_text],
        details(".dropdown")[
            summary[label_text],
            ul[
                (li[label[
                    input(type_="radio",
                          name=field_name,
                          value=item.id,
                          data_helper=(
                              extra_text if extra_text else ""
                          ) + item.peternak.name,
                          _="""
                            set :grandpa to the closest <details/>
                            init
                                log my @checked
                                if my @checked == "" trigger poke
                            end
                            on click
                                toggle @open on :grandpa
                                trigger poke
                            end
                            on poke
                                put my @data-helper into
                                    the first <summary/> in :grandpa
                          """,
                          checked=(item.id == selected)
                          ),
                    img(style="height: 4em; margin-right: 2em;",
                        src=img_dir + item.img),
                    (extra_text if extra_text else "") + item.peternak.name
                ]] for item in items),
                extra_li
            ]]]
