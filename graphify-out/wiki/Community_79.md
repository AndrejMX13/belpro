# Community 79

> 6 nodes · cohesion 0.40

## Key Concepts

- **send_email()** (5 connections) — `api/services/email.py`
- **email.py** (4 connections) — `api/services/email.py`
- **_check_mx()** (3 connections) — `api/services/email.py`
- **Async email sender backed by aiosmtplib.  Reads SMTP config from the Manager row** (1 connections) — `api/services/email.py`
- **Raise ValueError if the recipient domain has no MX records.** (1 connections) — `api/services/email.py`
- **Send an email via STARTTLS SMTP.      Raises SmtpNotConfiguredError if host/port** (1 connections) — `api/services/email.py`

## Relationships

- [[Community 32]] (2 shared connections)
- [[Community 69]] (1 shared connections)

## Source Files

- `api/services/email.py`

## Audit Trail

- EXTRACTED: 14 (93%)
- INFERRED: 1 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*