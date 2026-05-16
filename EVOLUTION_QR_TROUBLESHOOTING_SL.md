[English](EVOLUTION_QR_TROUBLESHOOTING.md)

# Evolution API — Odpravljanje težav s QR kodo WhatsApp

## Težava

Po nastavitvi nove instance Evolution API z integracijo Baileys se QR koda ni nikoli pojavila. Simptomi:

- Gumb »Get QR Code« v nadzorni plošči odpre pojavno okno samo z naslovom, brez slike QR
- Gumb »Get Pairing Code« prikazuje animacijo nalaganja v nedogled
- `GET /instance/connect/belpro` vrne `{"count":0}`
- `GET /instance/connectionState/belpro` vrne `{"instance":{"instanceName":"belpro","state":"connecting"}}`

## Vzroki

### 1. Zastarela različica odjemalca WhatsApp (pravi krivec)

Evolution API v2.2.3 vključuje Baileys z različico odjemalca WhatsApp `2.3000.1015901307`. WhatsAppovi strežniki to različico zavrnejo — Baileys se poveže, poskusi registracijo in takoj prejme `Error: Connection Failure`. Ta cikel se ponavlja v nedogled in QR koda se nikoli ne ustvari.

**Rešitev:** Nastavi `CONFIG_SESSION_PHONE_VERSION` v docker-compose.yml na vrednost, ki ustreza trenutni različici Baileys.

Preveri trenutno pravilno vrednost na:
```
https://raw.githubusercontent.com/WhiskeySockets/Baileys/master/src/Defaults/baileys-version.json
```

Vrednost je polje, npr. `[2, 3000, 1035194821]` — poveži z pikami: `2.3000.1035194821`.

V `docker-compose.yml` pod storitvijo `evolution-api`:
```yaml
environment:
  CONFIG_SESSION_PHONE_VERSION: "2.3000.1035194821"
```

> **Opomba:** Ta spremenljivka je bila odstranjena v Evolution API v2.3.1+. Potrebna je samo za v2.2.x.

### 2. Napaka v uporabniškem vmesniku nadzorne plošče (ločena težava)

Tudi po odpravi težave z različico pojavno okno nadzorne plošče ne prikaže slike QR — prejme base64 niz iz zalednega sistema, a ga ne more prikazati. To je znana napaka, ki jo spremlja [Evolution API issue #1602](https://github.com/EvolutionAPI/evolution-api/issues/1602).

**Rešitev:** Pridobi QR prek API-ja in ga prikaži ročno (glej spodaj).

### 3. Napačno mapiranje okoljske spremenljivke (odkrito med preiskavo)

`docker-compose.yml` je imel `AUTHENTICATION_API_KEY: ${EVOLUTION_API_KEY}` — globalni skrbniški ključ je bil preslikan na spremenljivko žetona za posamezno instanco. To sta dve različni stvari:

- `AUTHENTICATION_API_KEY` — globalni skrbniški ključ Evolution API (uporablja se v curl `-H "apikey: ..."`)
- `EVOLUTION_API_KEY` — žeton na ravni instance, ki ga n8n uporablja za klicanje določene instance

Popravljeno na `AUTHENTICATION_API_KEY: ${AUTHENTICATION_API_KEY}` v docker-compose.yml.

---

## Koraki namestitve (čista instanca od začetka)

### 1. Preveri, da ima docker-compose.yml popravek različice

```yaml
evolution-api:
  environment:
    CONFIG_SESSION_PHONE_VERSION: "2.3000.1035194821"
    AUTHENTICATION_API_KEY: ${AUTHENTICATION_API_KEY}
```

### 2. Znova zaženi Evolution API

```bash
docker compose up -d evolution-api
```

### 3. Izbriši morebitno obstoječo pokvarjeno instanco

```bash
curl -X DELETE \
  -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/delete/belpro
```

### 4. Ustvari instanco in se poveži v enem koraku

```bash
curl -s -X POST \
  -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"instanceName":"belpro","integration":"WHATSAPP-BAILEYS"}' \
  http://localhost:8180/instance/create \
&& sleep 3 \
&& curl -s \
  -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/connect/belpro
```

### 5. Pridobi QR kodo in jo skeniraj

Nadzorna plošča ne bo prikazala QR. Namesto tega uporabi spodnji postopek — QR shrani kot HTML datoteko, ki jo odpreš v brskalniku:

```bash
curl -s -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/connect/belpro \
  | python /tmp/makeqr.py \
  && cp /tmp/qr.html /path/to/BelPro/qr.html
```

Kjer `/tmp/makeqr.py` vsebuje:

```python
import json, sys

data = json.load(sys.stdin)
html = '<html><body><img src="' + data['base64'] + '" style="width:300px"></body></html>'
with open('/tmp/qr.html', 'w') as f:
    f.write(html)
print('saved, count=' + str(data['count']))
```

Odpri `qr.html` v brskalniku in skeniraj z WhatsAppom: **Nastavitve → Povezane naprave → Poveži napravo**. QR koda poteče v ~60 sekundah.

---

## Ponovna vzpostavitev povezave (telefon odklopljen, seja potekla)

Samo ponovi korak 5 — ni treba brisati ali znova ustvarjati instance:

```bash
curl -s -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/connect/belpro \
  | python /tmp/makeqr.py \
  && cp /tmp/qr.html /mnt/d/Andrej/vsCode-workspace/BelPro/qr.html \
  && echo "Odpri qr.html v brskalniku"
```

---

## Preverjanje stanja instance

```bash
# Stanje povezave
curl -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/connectionState/belpro

# Celotne informacije o instanci
curl -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/fetchInstances
```

Pričakovano stanje ob vzpostavljeni povezavi: `{"instance":{"instanceName":"belpro","state":"open"}}`

---

## Ključne okoljske spremenljivke v .env

```
AUTHENTICATION_API_KEY=...   # Globalni skrbniški ključ Evolution API — uporablja se v vseh curl -H "apikey: ..." klicih
EVOLUTION_API_KEY=...        # Žeton na ravni instance — n8n delovni procesi ga uporabljajo za pošiljanje sporočil
EVOLUTION_INSTANCE_NAME=belpro
EVOLUTION_SERVER_URL=http://localhost:8180
```

---

## Informacije o različici

- Evolution API: `2.2.3` (slika: `atendai/evolution-api:latest` z dne 2026-05-05)
- Popravek različice Baileys: `2.3000.1035194821`
- Povezane GitHub težave: [#1602](https://github.com/EvolutionAPI/evolution-api/issues/1602), [#2068](https://github.com/EvolutionAPI/evolution-api/issues/2068), [#2380](https://github.com/EvolutionAPI/evolution-api/issues/2380)
