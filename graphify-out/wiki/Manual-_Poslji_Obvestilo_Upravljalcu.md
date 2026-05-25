# Manual: Poslji Obvestilo Upravljalcu

> 14 nodes

## Key Concepts

- **Common Use Cases** (6 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **1. Form Submissions** (3 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **3. Chat Platform Integrations (Slack, Discord, Teams)** (3 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **4. GitHub/GitLab Webhooks** (3 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **2. Payment Webhooks (Stripe, PayPal)** (2 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **5. IoT Device Data** (2 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **code:block7 (1. Webhook (path: "contact-form", POST))** (1 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **code:javascript (Name: {{$json.body.name}})** (1 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **code:javascript (// Code node - verify Stripe signature)** (1 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **code:block10 (1. Webhook (path: "slack-command", POST))** (1 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **code:javascript (Command: {{$json.body.command}})** (1 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **code:block12 (1. Webhook (path: "github", POST))** (1 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **code:javascript (Event Type: {{$json.headers['x-github-event']}})** (1 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`
- **code:block14 (1. Webhook (path: "sensor-data", POST))** (1 connections) — `.claude/skills/n8n-workflow-patterns/webhook_processing.md`

## Relationships

- [[Community 388]] (1 shared connections)

## Source Files

- `.claude/skills/n8n-workflow-patterns/webhook_processing.md`

## Audit Trail

- EXTRACTED: 27 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*