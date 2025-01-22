from datetime import datetime
from templates.components import (
    table_builder,
)
from htpy import style, table, header, thead, th, tr, td, h1, tbody

def date_formatter(input_date):
    months_indonesian = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]

    date_obj = datetime.strptime(input_date, "%Y-%m-%d")

    month_name = months_indonesian[date_obj.month - 1]  # Adjust for 0-based index

    formatted_date = f"{month_name[:3]}/{date_obj.day:02d}/{date_obj.year}" # Format date as Des/12/2012

    return formatted_date  # Output: Des/12/2012


report_css = """
/* General Reset */
body {
  margin: 0;
  font-family: sans-serif;
  background-color: white;
  color: black;
}

/* Header */
header {
  margin: 1rem 0;
}

header h1 {
  font-size: 2rem;
  font-weight: bold;
  margin: 0.3em 0;
}

/* Date Range */
.date-range {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.date-range span {
  font-weight: bold;
}

.content {
padding: 1.5cm;
}

/* Table */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem auto;
  font-size: 1rem;
}

table th,
table td {
  padding: 0.5rem;
}

table thead th {
  background-color: #e0e0e0;
  font-weight: bold;
}

table tbody tr:nth-child(odd) {
  background-color: #f9f9f9;
}

table tbody tr:nth-child(even) {
  background-color: white;
}

table tfoot {
  background-color: #e0e0e0;
  font-weight: bold;
}

.kanan { text-align: right; }
.kiri { text-align: left; }
.tengah { text-align: center; }
.date {
    padding-top: 1em;
}

/* Print Styles */
@media print {
  @page { margin: 0; }
  body {
    margin: 0;
    font-size: 12pt;
  }

  header h1 {
    font-size: 16pt;
  }

  .date-range {
    font-size: 12pt;
  }

  table {
    font-size: 10pt;
    width: 100%;
  }

  table th,
  table td {
    padding: 4px;
  }

  table tfoot {
    font-size: 11pt;
  }

  table thead th {
    background-color: #f0f0f0 !important;
    color: black;
  }

  table tbody tr {
    background-color: white !important;
  }
}

"""
from htpy import (
    Element,
    small,
    form,
    div,
    b,
    tr,
    td,
    input,
)


def report_juleha_table(rph, periode, report_data) -> Element:
    col_headers = ["No", "Tanggal", "Nama Juleha", "Jumlah"]
    headers = thead[tr[
        th(".tengah", style="width: 2em;")[col_headers[0]],
        th(".tengah", style="width: 12em;")[col_headers[1]],
        th(".kiri")[col_headers[2]],
        th(".kanan")[col_headers[3]]
    ]]
    date = ""
    rows = []
    no = 0
    total = 0

    for row in report_data:
        no = no + 1
        rows.append(tr[
            td(".tengah")[str(no)],
            td(".tengah")[date_formatter(row[0].waktu_sembelih)],
            td[row[0].juleha.name],
            td(".kanan")[str(row[1])],
        ])


    return div(".content")[
        header(".center")[
            h1["Laporan Penyembelihan"],
            h1[f"RPH {rph}"],
            h1(".date-range")[f"Tanggal {periode}"]
        ],
        table[headers, tbody[rows]]
    ]


def report_kiriman_table(report_data) -> Element:
    col_headers = ["Nama Lapak", "Jumlah"]
    date = ""
    rows = []

    for row in report_data:
        if row[0].waktu_kirim != date:
            date = row[0].waktu_kirim
            rows.append(tr[td(col_span="2")[
                b[date]
            ]])

        rows.append(tr[
            td[row[0].lapak.name],
            td[str(row[1])],
        ])

    return table_builder(col_headers, rows)


def date_range(endpoint):
    current_date = datetime.now().strftime("%Y-%m-%d")

    return div(style="padding-top: 12%;")[
        small["Pilih rentang waktu:"],
        form(
            role="search",
            hx_put=f"{endpoint}",
            hx_target="html",
            autocomplete="off",
        )[
            input(
                type="date", name="sejak", aria_label="Date", value=f"{current_date}"
            ),
            input(
                type="date", name="sampai", aria_label="Date", value=f"{current_date}"
            ),
            input(type="submit", value="Buka Laporan")
        ],
    ]


def tpl_print(report):
    return div(onload="window.print();")[
        style[report_css],
        report,
    ]
