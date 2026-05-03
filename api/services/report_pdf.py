"""PDF rendering for monthly volunteer reports using WeasyPrint."""
from __future__ import annotations

import html
from datetime import date, datetime
from decimal import Decimal

from weasyprint import HTML

_SL_MONTHS = [
    '', 'Januar', 'Februar', 'Marec', 'April', 'Maj', 'Junij',
    'Julij', 'Avgust', 'September', 'Oktober', 'November', 'December',
]

_BASE_CSS = """
@page { margin: 2cm; size: A4; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10pt; color: #1a1a2e; margin: 0; }
h1 { font-size: 16pt; margin-bottom: 0.2em; color: #1e3a8a; }
.meta { color: #444; margin-bottom: 1.5em; font-size: 10pt; line-height: 1.6; }
table { width: 100%; border-collapse: collapse; margin-top: 0.8em; }
thead th { background: #1e40af; color: white; padding: 7px 8px; text-align: left; font-size: 9pt; }
tbody td { padding: 5px 8px; border-bottom: 1px solid #e5e7eb; font-size: 9pt; vertical-align: top; }
tbody tr:nth-child(even) td { background: #f8fafc; }
.num { text-align: right; white-space: nowrap; }
tfoot td { font-weight: bold; border-top: 2px solid #1e40af; padding: 7px 8px; font-size: 9pt; }
.footer { margin-top: 2em; font-size: 8pt; color: #9ca3af; text-align: right; }
"""


def _esc(s: str | None) -> str:
    return html.escape(s or '')


def _fmt_date(d: date) -> str:
    return f"{d.day}. {d.month}. {d.year}"


def _generated_line() -> str:
    return datetime.now().strftime("%-d. %-m. %Y %H:%M")


def render_volunteer_pdf(
    first_name: str,
    last_name: str,
    year: int,
    month: int,
    entries: list,
) -> bytes:
    """Render a single-volunteer monthly report PDF and return raw bytes."""
    month_label = f"{_SL_MONTHS[month]} {year}"
    total = sum((e.hours for e in entries), Decimal("0"))

    rows = "".join(
        f"<tr>"
        f"<td class='num'>{_fmt_date(e.entry_date)}</td>"
        f"<td>{_esc(e.activity_description)}</td>"
        f"<td>{_esc(e.location)}</td>"
        f"<td class='num'>{float(e.hours):.1f}</td>"
        f"</tr>"
        for e in entries
    )

    doc = f"""<!DOCTYPE html>
<html lang="sl">
<head><meta charset="utf-8"><style>{_BASE_CSS}</style></head>
<body>
  <h1>Poročilo o prostovoljskem delu</h1>
  <p class="meta">
    <strong>Prostovoljec:</strong> {_esc(last_name)} {_esc(first_name)}<br>
    <strong>Obdobje:</strong> {month_label}
  </p>
  <table>
    <thead><tr>
      <th class="num">Datum</th>
      <th>Opis aktivnosti</th>
      <th>Lokacija</th>
      <th class="num">Ure</th>
    </tr></thead>
    <tbody>{rows or "<tr><td colspan='4'>Ni odobrenih vnosov.</td></tr>"}</tbody>
    <tfoot><tr>
      <td colspan="3">Skupaj</td>
      <td class="num">{float(total):.1f}</td>
    </tr></tfoot>
  </table>
  <p class="footer">Generirano: {_generated_line()}</p>
</body>
</html>"""

    return HTML(string=doc).write_pdf()


def render_summary_pdf(year: int, month: int, items: list) -> bytes:
    """Render an all-volunteer summary PDF and return raw bytes."""
    month_label = f"{_SL_MONTHS[month]} {year}"
    total_hours = sum((i.total_hours for i in items), Decimal("0"))
    total_entries = sum(i.entry_count for i in items)

    rows = "".join(
        f"<tr>"
        f"<td>{_esc(i.last_name)} {_esc(i.first_name)}</td>"
        f"<td class='num'>{float(i.total_hours):.1f}</td>"
        f"<td class='num'>{i.entry_count}</td>"
        f"</tr>"
        for i in items
    )

    doc = f"""<!DOCTYPE html>
<html lang="sl">
<head><meta charset="utf-8"><style>{_BASE_CSS}</style></head>
<body>
  <h1>Mesečno poročilo o prostovoljskem delu</h1>
  <p class="meta"><strong>Obdobje:</strong> {month_label}</p>
  <table>
    <thead><tr>
      <th>Prostovoljec</th>
      <th class="num">Skupaj ur</th>
      <th class="num">Odobrenih vnosov</th>
    </tr></thead>
    <tbody>{rows or "<tr><td colspan='3'>Ni aktivnih prostovoljcev.</td></tr>"}</tbody>
    <tfoot><tr>
      <td>Skupaj</td>
      <td class="num">{float(total_hours):.1f}</td>
      <td class="num">{total_entries}</td>
    </tr></tfoot>
  </table>
  <p class="footer">Generirano: {_generated_line()}</p>
</body>
</html>"""

    return HTML(string=doc).write_pdf()
