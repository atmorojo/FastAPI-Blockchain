from templates.components import table_builder, show_img

from htpy import (
    div,
    Element,
    tr,
    td,
    a,
)


validated = a(role="button", disabled=True)["Telah divalidasi"]


def action_button(validasi):
    return a(
        role="button",
        hx_put="/validasi/" + str(validasi.id),
        hx_target="this",
        hx_swap="outerHTML",
        hx_confirm="Apakah anda yakin untuk memvalidasi ternak ini?",
    )["Validasi"]


def validasi_table(validasis, validator) -> Element:
    col_headers = ["Kambing", "Actions"]
    rows = (
        tr[
            td(style="width: 50px;")[
                show_img("img_ternak/" + (validasi.img if validasi.img else ""))
            ],
            td[
                div(".table-actions", role="group")[
                    (
                        validated
                        if getattr(validasi, validator)
                        else action_button(validasi)
                    )
                ]
            ],
        ]
        for validasi in validasis
    )

    return table_builder(col_headers, rows)


def lapak_table(validasis, validator) -> Element:
    col_headers = ["Tag Kambing", "Actions"]
    rows = (
        tr[
            td[validasi.ternak.name],
            td[
                div(".table-actions", role="group")[
                    (
                        validated
                        if getattr(validasi, validator)
                        else action_button(validasi)
                    )
                ]
            ],
        ]
        for validasi in validasis
    )

    return table_builder(col_headers, rows)
