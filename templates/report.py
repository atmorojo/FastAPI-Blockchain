from templates.components import (
    table_builder,
)

from htpy import (
    Element,
    b,
    tr,
    td,
)


def report_juleha_table(report_data) -> Element:
    col_headers = ["Nama Juleha", "Jumlah"]
    date = ""
    rows = []

    for row in report_data:
        if row[0].waktu_sembelih != date:
            date = row[0].waktu_sembelih
            rows.append(tr[td[b[date]], td[""]])

        rows.append(tr[
            td[row[0].juleha.name],
            td[str(row[1])],
        ])

    return table_builder(col_headers, rows)


def report_kiriman_table(report_data) -> Element:
    col_headers = ["Nama Lapak", "Jumlah"]
    date = ""
    rows = []

    for row in report_data:
        if row[0].waktu_kirim != date:
            date = row[0].waktu_kirim
            rows.append(tr[td[b[date]], td[""]])

        rows.append(tr[
            td[row[0].lapak.name],
            td[str(row[1])],
        ])

    return table_builder(col_headers, rows)
