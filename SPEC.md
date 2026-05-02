│   └── restore.sh
│
└── db/
    └── init.sql                       # Initial schema
```

---

## 10. Deployment

- Single Docker Compose stack.
- Target: any Linux host (local dev machine, VPS, on-premise server).
- **Local development:** Windows 10 with WSL2 + Docker Desktop. All `docker compose` commands and shell scripts run inside WSL2 (Ubuntu). Do not assume native Windows paths or tooling.
- Services: `postgres`, `n8n`, `whisper`, `api`, `frontend` (nginx), `evolution-api`.
- All configuration via `.env` file.
- `setup.sh` guides initial configuration (manager credentials, Gmail, WhatsApp number linking).
- No Kubernetes, no cloud-specific dependencies.

### 10.1 Deployment Requirements (per NGO)

#### WhatsApp Phone Number
- Each deployment requires a **dedicated phone number** registered with WhatsApp.
- A Slovenian prepaid SIM (A1, Telekom, T-2) is sufficient — approximately €5 to activate.
- The number must remain active (WhatsApp session connected) at all times for the system to receive volunteer messages. Since volunteers message regularly, natural traffic will keep the number alive.
- **Never use a personal number** — Evolution API takes over the WhatsApp session for that number, which will disconnect the personal phone and may result in WhatsApp banning the number.
- If the WhatsApp number needs to change (e.g. SIM lost or expired), the process is: unlink the old instance in Evolution API, obtain a new number, and scan a new QR code. All volunteer records in PostgreSQL are tied to volunteer phone numbers, not the bot number, so no data is lost.
- Estimated ongoing cost: €0–30/year depending on operator and traffic. Most operators require a top-up or outgoing activity every 6–12 months to keep a prepaid SIM active. Regular inbound WhatsApp traffic does not count as activity for most operators — schedule a monthly automated outgoing ping if needed.

#### Gmail Account
- A dedicated Gmail account for the NGO is recommended (e.g. `prostovoljci.ngo@gmail.com`).
- A Gmail App Password must be generated (not the main account password).
- The same account is used for both outgoing monthly PDF emails and optional system notifications.

#### Server / Hosting
- Any Linux host with Docker and Docker Compose installed.
- Minimum recommended: 2 CPU cores, 4GB RAM (Whisper `medium` model requires ~2GB).
- For `large-v3` Whisper model: 8GB RAM recommended.
- **No public IP or open inbound port is required for WhatsApp connectivity.** Evolution API works like a WhatsApp Web client: it makes an outbound connection to WhatsApp servers, so it passes through a standard NAT/firewall with no port-forwarding needed. When a WhatsApp message arrives, Evolution API receives it over that outbound connection and fires an internal webhook to n8n — both services run in the same Docker network, so the webhook never leaves the host. The system is fully functional on a private LAN or behind a corporate firewall.
- A public domain/IP is only needed if the manager dashboard must be reachable from outside the local network (e.g. manager works remotely). For a single on-site deployment this is not required.

---

## 11. Out of Scope (v1)

- Multi-tenant / SaaS mode
- Multiple managers per NGO
- Non-Slovenian language support
- Mobile native app
- Integration with IRSD / government systems
- Automatic face detection in photos
- Volunteer self-registration via WhatsApp
