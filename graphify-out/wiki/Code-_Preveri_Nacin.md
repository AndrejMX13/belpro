# Code: Preveri Nacin

> 16 nodes

## Key Concepts

- **Common Gotchas** (9 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **1. ❌ Wrong: Hardcoded URLs** (2 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **✅ Correct: Use environment variables** (2 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **2. ❌ Wrong: Credentials in parameters** (2 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **✅ Correct: Use credentials system** (2 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **3. ❌ Wrong: No error handling** (2 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **✅ Correct: Handle errors** (2 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **✅ Correct: Use batching** (2 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript (url: "https://api.example.com/prod/users")** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript (url: "={{$env.API_BASE_URL}}/users")** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript (headerParameters: {)** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript (authentication: "predefinedCredentialType",)** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript (HTTP Request → Process (fails if API down))** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:javascript (HTTP Request (continueOnFail: true) → IF (error) → Handle)** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **4. ❌ Wrong: Blocking on large responses** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`
- **code:block54 (Split In Batches (100 items) → Process → Loop)** (1 connections) — `.claude/skills/n8n-workflow-patterns/http_api_integration.md`

## Relationships

- [[Community 353]] (1 shared connections)

## Source Files

- `.claude/skills/n8n-workflow-patterns/http_api_integration.md`

## Audit Trail

- EXTRACTED: 31 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*