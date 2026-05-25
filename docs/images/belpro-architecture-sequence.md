# BelPro — Sequence Diagram

Two flows: volunteer submitting a work entry, and manager approving it.
Render with any Mermaid-compatible viewer (VS Code + Mermaid extension, GitHub, Obsidian, mermaid.live).

```mermaid
sequenceDiagram
    actor V as 👤 Volunteer
    participant WA as Meta / WhatsApp
    participant EVO as Evolution API
    participant N8N as n8n
    participant API as API
    participant W as Whisper
    participant DB as PostgreSQL

    rect rgb(219, 234, 254)
        Note over V,DB: Flow 1 — Volunteer submits a work entry

        V->>WA: sends voice message + optional photo
        WA->>EVO: delivers message (webhook)
        EVO->>N8N: forwards event (webhook)

        N8N->>API: create draft log entry
        API->>DB: save entry (status: pending_volunteer)
        API-->>N8N: entry ID

        N8N->>W: transcribe audio file
        W-->>N8N: transcript text

        N8N->>API: update entry with transcript
        API->>DB: save transcript

        N8N->>EVO: send confirmation to volunteer\n(shows date, hours, description)
        EVO->>WA: deliver WhatsApp message
        WA->>V: "Is this correct? 1-Confirm 2-Edit 3-Add photo 4-Cancel"

        V->>WA: replies "1" (confirm)
        WA->>EVO: delivers reply
        EVO->>N8N: forwards reply
        N8N->>API: mark entry as pending_manager
        API->>DB: update status
    end

    rect rgb(220, 252, 231)
        Note over V,DB: Flow 2 — Manager approves

        N8N->>API: poll for pending entries
        API->>DB: query pending entries
        DB-->>API: entry list
        API-->>N8N: entries

        N8N->>EVO: notify manager via WhatsApp\n(volunteer name, hours, description)
        EVO->>WA: deliver message
        WA->>V: (manager receives on their phone)

        Note over V,DB: Manager can approve via WhatsApp reply OR web dashboard

        API->>DB: update entry status (approved / rejected)
        N8N->>EVO: send result back to volunteer
        EVO->>WA: deliver WhatsApp message
        WA->>V: "Your entry has been approved ✓"
    end

    rect rgb(254, 243, 199)
        Note over V,DB: Flow 3 — Monthly report (automated, 28th of each month)

        N8N->>API: trigger monthly report
        API->>DB: query approved entries for period
        DB-->>API: entry data
        API-->>N8N: PDF report (per volunteer + consolidated)
        N8N->>N8N: send PDF by email to NGO
    end
```
