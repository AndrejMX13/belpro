# n8n Code Node Pattern

> 13 nodes

## Key Concepts

- **_Handler** (7 connections) — `whisper/transcribe.py`
- **._respond()** (5 connections) — `whisper/transcribe.py`
- **.do_POST()** (3 connections) — `whisper/transcribe.py`
- **.do_GET()** (3 connections) — `whisper/transcribe.py`
- **BaseHTTPRequestHandler** (2 connections)
- **transcribe.py** (2 connections) — `whisper/transcribe.py`
- **.log_message()** (2 connections) — `whisper/transcribe.py`
- **Thin HTTP wrapper around Faster-Whisper for local speech-to-text.  Exposes a sin** (1 connections) — `whisper/transcribe.py`
- **Handle POST /transcribe requests.** (1 connections) — `whisper/transcribe.py`
- **Transcribe the uploaded audio and return plain-text.** (1 connections) — `whisper/transcribe.py`
- **Health check — GET /health returns 200 ok.** (1 connections) — `whisper/transcribe.py`
- **Send a simple HTTP response.** (1 connections) — `whisper/transcribe.py`
- **Route access logs to stdout.** (1 connections) — `whisper/transcribe.py`

## Relationships

- [[012_settings_table.py]] (1 shared connections)
- [[005_report_prefs.py]] (1 shared connections)

## Source Files

- `whisper/transcribe.py`

## Audit Trail

- EXTRACTED: 29 (97%)
- INFERRED: 1 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*