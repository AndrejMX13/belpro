# test_migrations.py

> 21 nodes

## Key Concepts

- **Common Gotchas** (11 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **1. ❌ Wrong: Ignoring timezone** (2 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **✅ Correct: Set workflow timezone** (2 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **2. ❌ Wrong: Overlapping executions** (2 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **✅ Correct: Add execution lock** (2 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **3. ❌ Wrong: No error handling** (2 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **✅ Correct: Add error workflow** (2 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **4. ❌ Wrong: Processing all data at once** (2 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **✅ Correct: Batch processing** (2 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **5. ❌ Wrong: Hardcoded dates** (2 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **✅ Correct: Dynamic dates** (2 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **code:javascript (Schedule (9 AM)  // 9 AM in which timezone?)** (1 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **code:javascript (// Workflow settings)** (1 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **code:block34 (Schedule (every 5 min) → Long-running task (10 min))** (1 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **code:block35 (Schedule → Redis (check lock))** (1 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **code:block36 (Schedule → API call → Process (fails silently))** (1 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **code:block37 (Main: Schedule → Execute)** (1 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **code:block38 (Schedule → SELECT 1000000 records → Process (OOM))** (1 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **code:block39 (Schedule → SELECT with pagination → Split In Batches → Proce)** (1 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **code:javascript (query: "SELECT * FROM orders WHERE date = '2024-01-15'")** (1 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`
- **code:javascript (query: "SELECT * FROM orders WHERE date = CURRENT_DATE - INT)** (1 connections) — `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`

## Relationships

- [[Je v urejanju?]] (1 shared connections)

## Source Files

- `.claude/skills/n8n-workflow-patterns/scheduled_tasks.md`

## Audit Trail

- EXTRACTED: 41 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*