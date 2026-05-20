"""GDPR Article 13 consent notice PDF generation."""
from __future__ import annotations

import html as _html
from datetime import datetime

from weasyprint import HTML

from services.logo import logo_src
from services.report_pdf import BASE_CSS, NGOInfo, ngo_header_html

_CONSENT_CSS = """
section { margin-bottom: 1em; }
section h2 { font-size: 10pt; font-weight: bold; margin-bottom: 0.3em; color: #1e3a8a; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.15em; }
section p, section ul { margin: 0.2em 0 0; font-size: 9.5pt; line-height: 1.5; }
section ul { padding-left: 1.5em; }
.signature-block { margin-top: 2em; border-top: 2px solid #1e40af; padding-top: 1em; }
.signature-block h2 { font-size: 10pt; font-weight: bold; color: #1e3a8a; margin-bottom: 0.5em; }
.sig-row { display: flex; justify-content: space-between; margin-top: 2em; font-size: 9.5pt; }
.sig-row span { border-top: 1px solid #1a1a2e; padding-top: 0.25em; min-width: 10em; }
"""


def _esc(s: str | None) -> str:
    return _html.escape(s or "")


def _now_str() -> str:
    n = datetime.now()
    return f"{n.day}. {n.month}. {n.year} {n.strftime('%H:%M')}"


def render_consent_pdf(manager: object, photo_retention_days: int) -> bytes:
    """Render the GDPR Article 13 consent notice PDF and return raw bytes.

    `manager` must expose: ngo_name, ngo_street, ngo_postal_code, ngo_city,
    phone, email, ngo_davcna, gdpr_additional_clauses.
    """
    ngo = NGOInfo(
        name=manager.ngo_name,
        street=manager.ngo_street,
        postal_code=manager.ngo_postal_code,
        city=manager.ngo_city,
        phone=getattr(manager, "phone", None),
        email=getattr(manager, "email", None),
        ngo_davcna=getattr(manager, "ngo_davcna", None),
        logo_path=logo_src(),
    )
    header = ngo_header_html(ngo)

    clauses_html = ""
    raw_clauses = getattr(manager, "gdpr_additional_clauses", None)
    if raw_clauses and raw_clauses.strip():
        clauses_html = f"""
  <section>
    <h2>Dodatne določbe</h2>
    <p>{_esc(raw_clauses.strip())}</p>
  </section>"""

    doc = f"""<!DOCTYPE html>
<html lang="sl">
<head><meta charset="utf-8"><style>{BASE_CSS}{_CONSENT_CSS}</style></head>
<body>
  {header}
  <h1>Obvestilo posameznikom po 13. členu Splošne uredbe o varstvu podatkov (GDPR) glede obdelave osebnih podatkov</h1>
  <p class="meta"><strong>Zbirka:</strong> Evidenca prostovoljskega dela</p>

  <section>
    <h2>Upravljavec zbirke osebnih podatkov</h2>
    <p>{_esc(manager.ngo_name)}<br>
    {_esc(manager.ngo_street)}, {_esc(manager.ngo_postal_code)} {_esc(manager.ngo_city)}<br>
    {f"Davčna št.: {_esc(manager.ngo_davcna)}<br>" if getattr(manager, "ngo_davcna", None) else ""}
    {f"Tel: {_esc(manager.phone)}<br>" if getattr(manager, "phone", None) else ""}
    {f"E-pošta: {_esc(manager.email)}" if getattr(manager, "email", None) else ""}</p>
  </section>

  <section>
    <h2>Pooblaščena oseba za varstvo osebnih podatkov (DPO)</h2>
    <p>Ni imenovana.</p>
  </section>

  <section>
    <h2>Namen obdelave osebnih podatkov</h2>
    <p>Vodenje evidence prostovoljskega dela v skladu z Zakonom o prostovoljstvu (Ur. l. RS, št. 10/11 in nasl.).
    Zbiramo naslednje osebne podatke: EMŠO, telefonska številka, glasovni posnetki, fotografije.</p>
  </section>

  <section>
    <h2>Pravna podlaga za obdelavo osebnih podatkov</h2>
    <ul>
      <li>EMŠO in evidenca ur: člen 6(1)(c) Splošne uredbe — zakonska obveznost (Zakon o prostovoljstvu)</li>
      <li>Fotografije in glasovni posnetki: člen 6(1)(a) Splošne uredbe — privolitev posameznika</li>
    </ul>
  </section>

  <section>
    <h2>Uporabniki osebnih podatkov</h2>
    <p>Center za socialno delo (CSD) za namen mesečnega poročanja o prostovoljskem delu.
    Podatki se ne posredujejo v tretje države ali mednarodne organizacije.</p>
  </section>

  <section>
    <h2>Obdobje hrambe osebnih podatkov</h2>
    <ul>
      <li>Fotografije in glasovni posnetki: {photo_retention_days} dni od nastanka zapisa</li>
      <li>Evidence ur in aktivnosti: 10 let (zakonska arhivska obveznost)</li>
    </ul>
  </section>

  <section>
    <h2>Pravice posameznika</h2>
    <p>Imate pravico zahtevati dostop do vaših osebnih podatkov, njihov popravek ali izbris, omejitev obdelave,
    pravico do ugovora obdelavi ter pravico do prenosljivosti podatkov. Pravice uveljavljate z zahtevo,
    poslano na zgoraj navedene kontakte upravljavca.</p>
  </section>

  <section>
    <h2>Pravica do preklica privolitve</h2>
    <p>Privolitev za obdelavo fotografij in glasovnih posnetkov lahko kadar koli prekličete, ne da bi to vplivalo
    na zakonitost obdelave, ki se je na podlagi privolitve izvajala do njenega preklica.</p>
  </section>

  <section>
    <h2>Pravica do vložitve pritožbe pri nadzornem organu</h2>
    <p>Pritožbo lahko podate Informacijskemu pooblaščencu: Dunajska 22, 1000 Ljubljana,
    gp.ip@ip-rs.si, 01 230 97 30, www.ip-rs.si.</p>
  </section>

  <section>
    <h2>Avtomatizirano odločanje in profiliranje</h2>
    <p>Ne izvajamo avtomatiziranega sprejemanja odločitev niti profiliranja.</p>
  </section>
{clauses_html}
  <div class="signature-block">
    <h2>Izjava in podpis prostovoljca</h2>
    <p>S podpisom potrjujem, da sem bil/-a seznanjen/-a z vsebino tega obvestila in dajem privolitev
    za obdelavo fotografij in glasovnih posnetkov za namen vodenja evidence prostovoljskega dela.</p>
    <div class="sig-row">
      <span>Ime in priimek: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span>Datum: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
    </div>
    <div class="sig-row">
      <span>Podpis: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
    </div>
  </div>

  <p class="footer">Generirano: {_now_str()}</p>
</body>
</html>"""

    return HTML(string=doc).write_pdf()
