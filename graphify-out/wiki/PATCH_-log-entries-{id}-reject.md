# PATCH /log-entries/{id}/reject

> 17 nodes

## Key Concepts

- **Common Gotchas** (9 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **1. ❌ Wrong: Unbounded queries** (2 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **✅ Correct: Use LIMIT** (2 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **2. ❌ Wrong: String concatenation in queries** (2 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **✅ Correct: Parameterized queries** (2 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **3. ❌ Wrong: No transaction for multi-step operations** (2 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **✅ Correct: Use transaction** (2 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **4. ❌ Wrong: Processing all items at once** (2 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **✅ Correct: Batch processing** (2 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **code:sql (SELECT * FROM large_table  -- Could return millions)** (1 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **code:sql (SELECT * FROM large_table)** (1 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **code:javascript (query: "SELECT * FROM users WHERE id = '{{$json.id}}'")** (1 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **code:javascript (query: "SELECT * FROM users WHERE id = $1",)** (1 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **code:block45 (INSERT into orders)** (1 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **code:block46 (BEGIN)** (1 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **code:block47 (SELECT 1000000 records → Process all → OOM error)** (1 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`
- **code:block48 (SELECT records → Split In Batches (1000) → Process → Loop)** (1 connections) — `.claude/skills/n8n-workflow-patterns/database_operations.md`

## Relationships

- [[HTTP: Pridobi Upravljalca]] (1 shared connections)

## Source Files

- `.claude/skills/n8n-workflow-patterns/database_operations.md`

## Audit Trail

- EXTRACTED: 33 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*