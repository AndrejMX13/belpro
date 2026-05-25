# Community 435

> 8 nodes

## Key Concepts

- **send_email()** (6 connections) — `api/services/email.py`
- **email.py** (5 connections) — `api/services/email.py`
- **SmtpNotConfiguredError** (5 connections) — `api/services/email.py`
- **_check_mx()** (3 connections) — `api/services/email.py`
- **Async email sender backed by aiosmtplib.  Reads SMTP config from the Manager row** (1 connections) — `api/services/email.py`
- **Raise ValueError if the recipient domain has no MX records.** (1 connections) — `api/services/email.py`
- **Raised when the manager has not configured SMTP.** (1 connections) — `api/services/email.py`
- **Send an email via STARTTLS SMTP.      Raises SmtpNotConfiguredError if host/port** (1 connections) — `api/services/email.py`

## Relationships

- [[GET /log-entries/{id}/photos/{pid}/file]] (2 shared connections)
- [[Maximum photos allowed per log entry.]] (1 shared connections)
- [[005_report_prefs.py]] (1 shared connections)
- [[LoginRequest (Schema)]] (1 shared connections)

## Source Files

- `api/services/email.py`

## Audit Trail

- EXTRACTED: 20 (87%)
- INFERRED: 3 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*