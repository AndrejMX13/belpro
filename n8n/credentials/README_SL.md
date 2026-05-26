[English](README.md)

# n8n Prijavni podatki (Credentials)

Datoteke JSON s prijavnimi podatki so **gitignorirane** in jih nikoli ne smete objaviti v repozitorij.

## Zahtevani prijavni podatki

| Ime prijavnih podatkov | Tip | Ustvari |
|----------------|------|---------|
| `BelPro Postgres` | PostgreSQL | `scripts/setup.sh` (samodejno) |
| `BelPro API (Basic Auth)` | Basic Auth | `scripts/setup.sh` (samodejno) |
| `BelPro API Internal Key` | HTTP Header Auth | `scripts/setup.sh` (samodejno) |
| `BelPro Evolution API` | HTTP Header Auth | Ročno (po namestitvi WhatsApp) |
| `BelPro SMTP` | SMTP (vozlišče Send Email) | Ročno (po namestitvi SMTP) |

## Nastavitev

`scripts/setup.sh` samodejno ustvari prve tri prijavne podatke med namestitvijo.
Preostala dva zahtevata vrednosti, ki ob namestitvi še niso na voljo.

### Ročno — BelPro Evolution API
Po ustvaritvi instance Evolution API in vnosu ključa v `.env` kot `EVOLUTION_API_KEY`:
- Tip: HTTP Header Auth
- Ime glave: `apikey`
- Vrednost: `EVOLUTION_API_KEY` iz datoteke `.env`

Nato znova zaženite: `python scripts/n8n_workflows.py import`

### Ročno — BelPro SMTP
- Tip: SMTP (vozlišče Send Email)
- Geslo: `SMTP_PASSWORD` iz datoteke `.env`
- Gostitelj, vrata, uporabnik in prikazno ime: nastavljeno prek vmesnika BelPro Nastavitve (shranjeno v zbirki podatkov)
- Deluje z Gmail (smtp.gmail.com:587 + Geslo za aplikacijo), Yahoo, Proton ali katerim koli SMTP strežnikom.
