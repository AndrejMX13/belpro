# =============================================================================
# Belpro — .env.example.sl  (slovenščina)
# Kopirajte to datoteko v .env in izpolnite vse vrednosti pred zagonom vsebnikov.
# .env je v gitignore — nikoli ga ne shranite v git repozitorij.
# =============================================================================

# -----------------------------------------------------------------------------
# PostgreSQL
# Ena instanca, tri logične baze podatkov: belpro, n8n (shema), evolution
# -----------------------------------------------------------------------------
POSTGRES_DB=belpro
POSTGRES_USER=belpro
POSTGRES_PASSWORD=change_me_strong_password

# Asinhroni DSN, ki ga uporablja FastAPI / SQLAlchemy
DATABASE_URL=postgresql+asyncpg://belpro:change_me_strong_password@postgres:5432/belpro

# -----------------------------------------------------------------------------
# Šifriranje
# EMSO_ENCRYPTION_KEY: 32-bajtni ključ, kodiran v base64url.
# Ustvarite z: python3 -c "import secrets,base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"
# -----------------------------------------------------------------------------
EMSO_ENCRYPTION_KEY=GENERATE_AND_PASTE_HERE

# -----------------------------------------------------------------------------
# FastAPI
# API_SECRET_KEY: uporabljen za podpisovanje sej / JWT (če bo dodan pozneje).
# Ustvarite z: python3 -c "import secrets; print(secrets.token_hex(32))"
# MANAGER_PASSWORD: začetno geslo za prijavo v spletno nadzorno ploščo.
#   To je geslo, ki se uporablja ob prvi prijavi in dokler upravljalec ne
#   spremeni gesla na strani Nastavitve. Ko je geslo enkrat spremenjeno prek
#   vmesnika, ima prednost zapis v bazi podatkov — sprememba te vrednosti
#   in ponovni zagon vsebnikov NE bo ponastavila prijave.
#
#   Obnovitev dostopa (pozabljeno geslo po spremembi prek vmesnika):
#     docker compose exec postgres psql -U belpro -d belpro \
#       -c "UPDATE managers SET password_hash = NULL;"
#   To izbriše zapis iz baze podatkov in se ponastavi na vrednost MANAGER_PASSWORD.
# -----------------------------------------------------------------------------
API_SECRET_KEY=GENERATE_AND_PASTE_HERE
MANAGER_PASSWORD=change_me_strong_password

# -----------------------------------------------------------------------------
# n8n
# -----------------------------------------------------------------------------
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=change_me_strong_password

# URL za webhooks mora biti dosegljiv iz Evolution API (za lokalni razvoj: localhost)
N8N_WEBHOOK_URL=http://localhost:5678/
N8N_HOST=localhost
N8N_PROTOCOL=http

# API ključ za n8n — ustvarite v vmesniku n8n po prvem zagonu (Nastavitve → API)
# Dodajte ga tudi v .mcp.json po kreiranju
N8N_API_KEY=FILL_IN_AFTER_FIRST_N8N_RUN

# -----------------------------------------------------------------------------
# Evolution API (prehod WhatsApp)
# AUTHENTICATION_API_KEY: globalni ključ, ki varuje sam strežnik Evolution API
#   (uporablja se za prijavo v upravljalsko nadzorno ploščo na :8180/manager/
#   in za administrativne klice API).
#   Ustvarite z: python3 -c "import secrets; print(secrets.token_hex(24))"
# EVOLUTION_API_KEY: ključ na ravni instance, ustvarjen ob vzpostavitvi instance
#   'belpro' znotraj Evolution API — razlikuje se od AUTHENTICATION_API_KEY.
#   Kopirajte s strani s podrobnostmi instance po njeni vzpostavitvi.
# EVOLUTION_INSTANCE_NAME: ime instance WhatsApp znotraj Evolution API.
#   Nujno je točno ujemanje z imenom, ki je bilo uporabljeno ob vzpostavitvi instance.
# EVOLUTION_SERVER_URL: javno dostopen URL strežnika Evolution API.
#   Brskalnik ga uporabi za odpiranje povezave do upravljalske nadzorne plošče
#   v nastavitvah. Za lokalni razvoj: http://localhost:8180
# NGO_WHATSAPP_PHONE: telefonska številka računa WhatsApp, povezanega z botom.
#   Samo številke, brez predpone '+' (npr. 38671234567).
#   Vneseno v bazo podatkov ob prvem zagonu, če je vrednost v bazi prazna.
#   Samodejno sinhronizirano z Evolution API, ko je instanca povezana — ročna
#   posodobitev ni potrebna po skeniranju QR kode; samo osvežite stran Nastavitve.
# -----------------------------------------------------------------------------
AUTHENTICATION_API_KEY=GENERATE_AND_PASTE_HERE
EVOLUTION_API_KEY=COPY_FROM_EVOLUTION_INSTANCE_DETAIL
EVOLUTION_INSTANCE_NAME=belpro
EVOLUTION_SERVER_URL=http://localhost:8180
NGO_WHATSAPP_PHONE=

# -----------------------------------------------------------------------------
# Faster-Whisper (prepoznavanje govora)
# WHISPER_MODEL: tiny/base/small/medium/large-v3
#   medium = dober kompromis med hitrostjo in natančnostjo za slovenščino
#   large-v3 = najboljša natančnost, ~4 GB RAM, počasnejši na procesorju (priporočeno)
# -----------------------------------------------------------------------------
WHISPER_MODEL=large-v3
WHISPER_LANGUAGE=sl

# -----------------------------------------------------------------------------
# E-pošta (odhodni — mesečni PDF-ji, obvestila)
# Deluje z vsakim ponudnikom SMTP: Gmail, Yahoo, Proton, institucionalni strežniki.
#
# smtp_host, smtp_port, smtp_user, smtp_from_name se nastavijo prek vmesnika
# Nastavitve (shranjeno v bazi podatkov). Samo geslo ostane v tej datoteki.
#
# Gmail: uporabite geslo za aplikacijo (ne vašega glavnega gesla).
#   Ustvarite na: https://accounts.google.com/AccountChooser?continue=https://myaccount.google.com/apppasswords
#   smtp_host = smtp.gmail.com, smtp_port = 587
# -----------------------------------------------------------------------------
SMTP_PASSWORD=xxxx_xxxx_xxxx_xxxx

# -----------------------------------------------------------------------------
# Testni pripomočki
# Uporablja ga scripts/switch_manager_phone.ps1 za preklapljanje telefonske
# številke upravljalca med pravo in testno številko pri testiranju end-to-end.
# -----------------------------------------------------------------------------
# Dejanska telefonska številka WhatsApp upravljalca (Mode=manager)
TEST_MANAGER_PHONE=386000000000
# Nadomestna številka za začasno nastavitev kot telefon upravljalca (Mode=volunteer)
TEST_VOLUNTEER_PHONE=38600000000
