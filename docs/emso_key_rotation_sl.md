# Rotacija ključa za šifriranje EMŠO — Navodila za postopek

Ta dokument zajema vse, kar morate vedeti pred, med in po rotaciji šifrirnega ključa za EMŠO. Preberite ga v celoti, preden začnete.

---

## Kdaj se to opravi

Samo kadar je treba zamenjati `EMSO_ENCRYPTION_KEY` — na primer ob sumu na kompromitacijo ključa ali zahtevi varnostne revizije. To ni redno vzdrževanje. V normalnem delovanju ključa ni treba nikoli menjati.

---

## Predpogoji

Vse spodnje mora biti izpolnjeno, preden začnete:

- Celoten Docker stack teče (`docker compose ps` prikazuje vse storitve kot zdrave).
- Slika vsebnika `api` je **aktualna** — mora biti zgrajena po tem, ko je bil `api/scripts/rotate_emso_key.py` dodan v repozitorij. Če ste pravkar klonirali ali povlekli repozitorij, zaženite `docker compose up -d --build api` preden nadaljujete.
- Imate delujočo terminalno sejo z dostopom do projektnega imenika.
- Imate na voljo **drugi terminalski okno** za korake sredi rotacije (posodobitev `.env` in ponovni zagon vsebnika).

---

## Korak 1 — Shranite trenutni ključ

Preden karkoli generirate, pridobite trenutni ključ in ga shranite na varno mesto zunaj terminala (upravljalnik gesel, šifrirana beležka):

```bash
grep EMSO_ENCRYPTION_KEY .env
```

Zapišite si ga. Brez njega ne morete razveljaviti rotacije, če gre kaj narobe.

---

## Korak 2 — Ustvarite nov ključ

Generirajte nov ključ v spremenljivko lupine, da se izognete napakam pri kopiranju. Ključ, kodiran z base64url za 32 bajtov, mora imeti natanko **44 znakov** (43 podatkovnih znakov + en `=` za oblazinjenje).

```bash
NEW_KEY=$(python3 -c "import secrets,base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())")

# Preverite: mora izpisati 44
echo -n "$NEW_KEY" | wc -c

# Prikažite ključ, da ga shranite
echo "$NEW_KEY"
```

Shranite nov ključ skupaj s starim, preden nadaljujete.

---

## Korak 3 — Zaženite skript za rotacijo

Stari ključ podajte neposredno, novega pa prek spremenljivke:

```bash
bash scripts/rotate_emso_key.sh <STAR_KLJUC> "$NEW_KEY"
```

Zamenjajte `<STAR_KLJUC>` z vrednostjo iz Koraka 1.

Skript bo:

1. Zahteval potrditev, da imate stari ključ shranjen — vtipkajte `DA`.
2. Samodejno ustvaril celotno varnostno kopijo baze podatkov.
3. Ustvaril ciljno varnostno kopijo tabele prostovoljcev (s starim ključem) znotraj vsebnika na `/app/pdfs/temp/`.
4. Preveril vsak shranjeni EMŠO (kontrolna vsota + oblika) pred kakršnimikoli spremembami.
5. V eni atomski transakciji znova šifriral vse EMŠO z novim ključem.
6. Preveril vzorec znova šifriranih zapisov pred potrditvijo.
7. **Zaustavil se** — in vas navodil, da opravite Koraka 4 in 5, preden karkoli vtipkate.

---

## Korak 4 — Posodobite `.env` in znova zaženite API (med pavzo skripta)

Odprite **drugi terminal**, nato:

```bash
# Uredite .env — spremenite EMSO_ENCRYPTION_KEY na novo vrednost
# Nato znova zaženite vsebnik api:
docker compose up -d api

# Preverite, da se je pravilno zagnal:
docker compose logs api --tail 20
```

Poiščite vrstico zagona, ki potrjuje, da API posluša. Ne sme biti napak glede šifriranja ali povezave z bazo podatkov.

---

## Korak 5 — Potrdite čiščenje v prvem terminalu

Ko je API v drugem terminalu potrjen kot zdrav, se vrnite v prvi terminal in na poziv za čiščenje odgovorite z `DA`.

Skript bo izbrisal datoteko ciljne varnostne kopije iz `/app/pdfs/temp/`. Ta datoteka vsebuje stari šifrirni ključ in staro šifrirano besedilo — dokler obstaja, z njo ravnajte kot z zaupno.

---

## Varnostne kopije ustvarjene pred rotacijo

Vsaka varnostna kopija baze podatkov, ustvarjena pred rotacijo ključa, vsebuje EMŠO podatke šifrirane s **starim** ključem. Če obnovite takšno kopijo po tem, ko ste stari ključ zavrglo, bo obnova baze uspela, a aplikacija ne bo mogla dešifrirati nobenega EMŠO — vsi zapisi prostovoljcev bodo neberljivi.

**Pravilo:** Stari `EMSO_ENCRYPTION_KEY` hranite na varnem mestu vsaj toliko dni, kolikor znaša vaša doba hrambe varnostnih kopij (`BACKUP_RETENTION_DAYS`, privzeto 30 dni). Stari ključ trajno izbrišite šele, ko so vse varnostne kopije iz časa pred rotacijo že potekle.

Za ugotovitev, kateri ključ zahteva določena varnostna kopija, preverite datoteko `manifest.txt` v mapi varnostne kopije. Vsebuje polje `EMSO key prefix` — prvih 8 znakov `EMSO_ENCRYPTION_KEY`, ki je bil aktiven ob ustvarjanju kopije. Primerjajte ga s shranjenimi ključi, da poiščete pravega.

---

## Če gre kaj narobe

Če rotacija spodleti na pol poti, baza podatkov ni spremenjena — Python skript uporablja transakcijo vse ali nič. Vaš stari ključ še vedno deluje. Preprosto odpravite težavo in zaženite znova.

Če je rotacija uspela, a se API ne zažene z novim ključem:

```bash
bash scripts/rotate_emso_key.sh --restore
```

Skript bo zahteval pot do datoteke ciljne varnostne kopije (izpisana med potekom rotacije, npr. `/app/pdfs/temp/emso_rotation_20260518_170050.json`). V eni transakciji bo obnovil staro šifrirano besedilo. Po obnovi nastavite `EMSO_ENCRYPTION_KEY` nazaj na staro vrednost v `.env` in znova zaženite API.

---

## Znane težave, odkrite med razvojem

Te so bile odkrite med prvim živim testom in so že popravljene v kodi — zapisane tukaj za referenco:

| Težava | Vzrok | Popravek |
|--------|-------|----------|
| `No module named 'services'` | `docker compose exec` ne uporabi `WORKDIR` vsebnika kot Python pot | Skript sedaj posreduje `-e PYTHONPATH=/app` pri vseh klicih exec |
| `Invalid base64-encoded string` | `load_key()` je uporabljal `base64.b64decode`, ki zavrne `-` in `_` iz base64url ključev | `load_key()` sedaj normalizira `-`→`+` in `_`→`/` pred dekodiranjem |
| Ključ poškodovan pri kopiranju | Prelom vrstice v terminalu ali odložišče odreže znake | Generirajte ključ v spremenljivko lupine in ga podajte kot `"$NEW_KEY"` |
| `No such file or directory` za Python skript | Slika vsebnika je bila zgrajena pred dodajanjem skripta v repozitorij | Po svežem klonu ali vleku vedno zaženite `docker compose up -d --build api` |
