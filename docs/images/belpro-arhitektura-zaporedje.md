# BelPro — Diagram zaporedja

Trije tokovi: oddaja delovnega vnosa, odobritev vodje in mesečno poročanje.
Odpri v katerem koli pregledovalniku Mermaid (VS Code + razširitev Mermaid, GitHub, Obsidian, mermaid.live).

```mermaid
sequenceDiagram
    actor V as 👤 Prostovoljec
    participant WA as Meta / WhatsApp
    participant EVO as Evolution API
    participant N8N as n8n
    participant API as API
    participant W as Whisper
    participant DB as PostgreSQL

    rect rgb(219, 234, 254)
        Note over V,DB: Tok 1 — Prostovoljec odda delovni vnos

        V->>WA: pošlje glasovno sporočilo + opcijska slika
        WA->>EVO: dostavi sporočilo (webhook)
        EVO->>N8N: posreduje dogodek (webhook)

        N8N->>API: ustvari osnutek vnosa
        API->>DB: shrani vnos (stanje: čaka prostovoljca)
        API-->>N8N: ID vnosa

        N8N->>W: prepiši zvočno datoteko
        W-->>N8N: besedilo transkripcije

        N8N->>API: posodobi vnos s transkripcijo
        API->>DB: shrani transkripcijo

        N8N->>EVO: pošlje potrditev prostovoljcu\n(datum, ure, opis dela)
        EVO->>WA: dostavi sporočilo WhatsApp
        WA->>V: "Je to pravilno? 1-Potrdi 2-Popravi 3-Dodaj sliko 4-Prekliči"

        V->>WA: odgovori "1" (potrdi)
        WA->>EVO: dostavi odgovor
        EVO->>N8N: posreduje odgovor
        N8N->>API: označi vnos kot čaka vodjo
        API->>DB: posodobi stanje
    end

    rect rgb(220, 252, 231)
        Note over V,DB: Tok 2 — Vodja odobri

        N8N->>API: preveri neobravnavane vnose
        API->>DB: poizvedba neobravnavanih vnosov
        DB-->>API: seznam vnosov
        API-->>N8N: vnosi

        N8N->>EVO: obvesti vodjo prek WhatsApp\n(ime prostovoljca, ure, opis)
        EVO->>WA: dostavi sporočilo
        WA->>V: (vodja prejme na telefon)

        Note over V,DB: Vodja odobri prek odgovora WhatsApp ALI nadzorne plošče

        API->>DB: posodobi stanje vnosa (odobreno / zavrnjeno)
        N8N->>EVO: pošlje rezultat prostovoljcu
        EVO->>WA: dostavi sporočilo WhatsApp
        WA->>V: "Vaš vnos je bil odobren ✓"
    end

    rect rgb(254, 243, 199)
        Note over V,DB: Tok 3 — Mesečno poročilo (samodejno, 28. v mesecu)

        N8N->>API: sproži mesečno poročilo
        API->>DB: poizvedba odobrenih vnosov za obdobje
        DB-->>API: podatki o vnosih
        API-->>N8N: poročilo PDF (za prostovoljca + zbirno)
        N8N->>N8N: pošlje PDF po e-pošti organizaciji
    end
```
