[English](README.md)

# n8n Prijavni podatki (Credentials)

Datoteke JSON s prijavnimi podatki so **gitignorirane** in jih nikoli ne smete objaviti v repozitorij.

## Zahtevani prijavni podatki

| Ime prijavnih podatkov | Tip | Uporablja |
|----------------|------|---------|
| `BelPro Postgres` | PostgreSQL | Vsa vozlišča za dostop do zbirke podatkov |
| `BelPro SMTP` | SMTP (vozlišče Send Email) | Dostava mesečnih PDF-jev, obvestila |
| `BelPro Evolution API` | HTTP Header Auth | Vozlišča za pošiljanje WhatsApp sporočil |
| `BelPro API (Basic Auth)` | Basic Auth | Vsi klici zaledja FastAPI (skoraj vsako vozlišče) |
| `BelPro API Internal Key` | HTTP Header Auth | Potek dela za napake (`error_handler.json`) |

## Nastavitev

Po zagonu sklada (`docker compose up -d`) odpri n8n na naslovu
http://localhost:5678 in ročno ustvari vse prijavne podatke pod
**Settings → Credentials → New Credential**.

- **PostgreSQL:** gostitelj `postgres`, vrata `5432`, zbirka podatkov `belpro`,
  uporabnik/geslo iz datoteke `.env`
- **SMTP:** uporabi prijavne podatke za vozlišče Send Email. Gostitelj, vrata, uporabnik in prikazno ime
  se nastavijo prek vmesnika BelPro Nastavitve (shranjeno v zbirki podatkov). Geslo iz `SMTP_PASSWORD`
  v datoteki `.env`. Deluje z Gmail (smtp.gmail.com:587 + Geslo za aplikacijo), Yahoo, Proton
  ali katerim koli SMTP strežnikom.
- **Evolution API:** glava `apikey: <EVOLUTION_API_KEY iz .env>`
- **BelPro API (Basic Auth):** uporabniško ime = `manager`, geslo = `MANAGER_PASSWORD` iz datoteke `.env`.
- **BelPro API Internal Key:** Ime glave `X-Internal-Key`, vrednost = `API_SECRET_KEY` iz datoteke `.env`.
