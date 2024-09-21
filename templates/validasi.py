from templates.components import (
    table_builder,
)

from htpy import (
    div,
    Element,
    tr,
    td,
    a,
)


def action_buttons(id, name):
    return div(".table-actions", role="group")[
      a(".outline.secondary", role="button",
        href="/validasi/" + str(id)
        )["Detail"],
      a(".outline.secondary", role="button",
        href="/validasi/edit/" + str(id)
        )["Edit"],
      a(".outline.warning", role="button",
        hx_delete="/validasi/" + str(id),
        hx_confirm=f"""
Apakah anda yakin mau menghapus data {name}?
        """,
        hx_target="#table-wrapper"
        )["Hapus"],
    ]


validated = a(role="button", disabled=True)["Telah divalidasi"]


def action_button(validasi):
    return a(role="button",
             hx_put="/validasi/" + str(validasi.id),
             hx_target="this",
             hx_swap="outerHTML",
             hx_confirm=f"""
Apakah anda yakin untuk memvalidasi {validasi.ternak.name}?
             """
             )["Validasi"]


def validasi_table(validasis, validator) -> Element:
    col_headers = ["Tag Kambing", "Actions"]
    rows = (tr[
      td[validasi.ternak.name],
      td[
        div(".table-actions", role="group")[
          (validated if getattr(validasi, validator) else action_button(validasi))
        ]
      ],
    ] for validasi in validasis)

    return table_builder(
        col_headers,
        rows
        )
