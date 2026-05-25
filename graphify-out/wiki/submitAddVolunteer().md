# submitAddVolunteer()

> 21 nodes

## Key Concepts

- **Common Gotchas** (11 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **1. ❌ Wrong: Connecting tools to main port** (2 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **✅ Correct: Use ai_tool connection type** (2 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **2. ❌ Wrong: Vague tool descriptions** (2 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **✅ Correct: Specific descriptions** (2 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **3. ❌ Wrong: No memory for conversations** (2 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **✅ Correct: Add memory** (2 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **4. ❌ Wrong: Giving AI write access** (2 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **✅ Correct: Read-only access** (2 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **5. ❌ Wrong: Unbounded tool responses** (2 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **✅ Correct: Limit tool output** (2 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **code:block44 (HTTP Request → AI Agent  // Won't work as tool!)** (1 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **code:block45 (HTTP Request --[ai_tool]--> AI Agent)** (1 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **code:block46 (description: "Get data"  // AI won't know when to use this)** (1 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **code:block47 (description: "Query customer orders by email address. Return)** (1 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **code:block48 (Every message is standalone - no context!)** (1 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **code:block49 (Window Buffer Memory --[ai_memory]--> AI Agent)** (1 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **code:block50 (Postgres (full access) as tool  // AI could DELETE data!)** (1 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **code:block51 (Postgres (read-only user) as tool  // Safe)** (1 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **code:block52 (Tool returns 10MB of data → exceeds token limit)** (1 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`
- **code:javascript ({)** (1 connections) — `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`

## Relationships

- [[Je v urejanju?]] (1 shared connections)

## Source Files

- `.claude/skills/n8n-workflow-patterns/ai_agent_workflow.md`

## Audit Trail

- EXTRACTED: 41 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*