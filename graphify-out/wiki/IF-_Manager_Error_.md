# IF: Manager Error?

> 15 nodes

## Key Concepts

- **Handling API Responses** (4 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **Pagination** (4 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **Error Responses (400-599)** (4 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **Pattern 1: Offset-based** (3 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **Success Response (200-299)** (2 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **Pattern 2: Cursor-based** (2 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **Pattern 3: Link Header** (2 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript (// Entire response)** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:block19 (1. Set (initialize: page=1, has_more=true))** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript (const items = $input.first().json;)** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:block21 (1. HTTP Request (GET /api/items))** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript (// Code node - parse Link header)** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript ({)** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:block24 (HTTP Request (continueOnFail: true))** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript ({{$json.error}} is empty)** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`

## Relationships

- [[IF: Has Entry?]] (1 shared connections)

## Source Files

- `.claude/skills/n8n-workflow-patterns/http_api_integration.md`

## Audit Trail

- EXTRACTED: 29 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*