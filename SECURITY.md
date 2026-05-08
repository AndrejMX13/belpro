# Security Policy

## Reporting a vulnerability

**Do not open a public issue.** Report vulnerabilities privately via GitHub's
[Security Advisory](https://github.com/AndrejMX13/belpro/security/advisories/new)
page, or by emailing the maintainer directly.

Include as much detail as you can:

- Steps to reproduce
- Affected version(s)
- Potential impact
- Any suggested fixes (if you have them)

You should receive a response within **5 working days**. If the vulnerability
is accepted, we aim to publish a fix within **30 days** and will credit you in
the release notes (unless you prefer to remain anonymous).

## Scope

The following are in scope for security reports:

- The FastAPI backend (`api/`)
- The n8n workflows (`n8n/workflows/`)
- The frontend dashboard (`frontend/`)
- The Docker Compose configuration
- The setup wizard and scripts (`scripts/`)
- EMŠO encryption and key handling
- Authentication and authorization logic

## Out of scope

BelPro is **self-hosted** software. The following are the responsibility of the
instance operator and are not considered vulnerabilities in BelPro itself:

- Misconfigured `.env` files or exposed secrets
- Compromised host servers or Docker daemons
- Exposed ports due to missing firewall rules
- Weak passwords chosen by the operator
- Outdated Docker images or unpatched host OS
- WhatsApp account compromise (SIM swap, social engineering)

## EMŠO encryption

EMŠO (Slovenian national ID number) is encrypted at rest using AES-256 via
Python's `cryptography` library. The encryption key (`EMSO_ENCRYPTION_KEY`)
lives in `.env` and is never stored in the database.

If you discover a flaw in how EMŠO is encrypted, stored, logged, or transmitted,
report it — it is treated as **high severity**.

## Supported versions

Security patches are provided for the **latest release only**. Older versions
will not receive backported fixes.

| Version | Supported |
|---------|-----------|
| 0.8.x   | Yes       |
| < 0.8   | No        |

## Security model assumptions

BelPro assumes:

1. The host machine is trusted and not compromised.
2. The `.env` file is readable only by the operator and the Docker Compose services.
3. Network access to the Docker host is controlled by the operator.
4. The operator keeps Docker images up to date.

If any of these assumptions are violated, the security of the instance is at
risk in ways that BelPro cannot defend against.
