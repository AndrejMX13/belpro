# Community 337

> 10 nodes

## Key Concepts

- **Example 3: Multi-Node Data Flow** (4 connections) — `.claude/skills/n8n-expression-syntax/EXAMPLES.md`
- **Node 3: Email** (4 connections) — `.claude/skills/n8n-expression-syntax/EXAMPLES.md`
- **Node 2: HTTP Request** (3 connections) — `.claude/skills/n8n-expression-syntax/EXAMPLES.md`
- **Node 1: Webhook** (2 connections) — `.claude/skills/n8n-expression-syntax/EXAMPLES.md`
- **code:json ({)** (1 connections) — `.claude/skills/n8n-expression-syntax/EXAMPLES.md`
- **code:block8 (https://api.example.com/orders/{{$json.body.order_id}})** (1 connections) — `.claude/skills/n8n-expression-syntax/EXAMPLES.md`
- **code:json ({)** (1 connections) — `.claude/skills/n8n-expression-syntax/EXAMPLES.md`
- **code:block10 (Order {{$node["Webhook"].json.body.order_id}} Confirmed)** (1 connections) — `.claude/skills/n8n-expression-syntax/EXAMPLES.md`
- **code:block11 (Dear {{$node["HTTP Request"].json.order.customer}},)** (1 connections) — `.claude/skills/n8n-expression-syntax/EXAMPLES.md`
- **code:block12 (Subject: Order ORD-12345 Confirmed)** (1 connections) — `.claude/skills/n8n-expression-syntax/EXAMPLES.md`

## Relationships

- [[Community 335]] (1 shared connections)

## Source Files

- `.claude/skills/n8n-expression-syntax/EXAMPLES.md`

## Audit Trail

- EXTRACTED: 19 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*