# BelPro Architecture Document EN

> 17 nodes

## Key Concepts

- **Docker Compose (all services containerised)** (11 connections) — `CLAUDE.md`
- **SQL Pro Skill** (7 connections) — `.claude/skills/sql-pro/SKILL.md`
- **Manager Web Dashboard** (6 connections) — `SPEC.md`
- **PostgreSQL 18 Database** (6 connections) — `SPEC.md`
- **SQL Query Patterns Reference (CTEs, JOINs, Subqueries)** (5 connections) — `.claude/skills/sql-pro/references/query-patterns.md`
- **FastAPI Backend + PDF Generation** (4 connections) — `CLAUDE.md`
- **SQL Query Optimization Reference (EXPLAIN, Indexes, Partitioning)** (4 connections) — `.claude/skills/sql-pro/references/optimization.md`
- **n8n as Workflow Engine** (3 connections) — `CLAUDE.md`
- **SQL Window Functions Reference (ROW_NUMBER, RANK, LAG/LEAD)** (3 connections) — `.claude/skills/sql-pro/references/window-functions.md`
- **nginx Reverse Proxy** (2 connections) — `SPEC.md`
- **Database Design Reference (Normalization, Keys, Constraints)** (2 connections) — `.claude/skills/sql-pro/references/database-design.md`
- **SQL Dialect Differences Reference (PostgreSQL, MySQL, SQL Server, Oracle)** (2 connections) — `.claude/skills/sql-pro/references/dialect-differences.md`
- **Alembic DB Migrations** (1 connections) — `CLAUDE.md`
- **Redis 7 (Cache/Queue)** (1 connections) — `README.md`
- **EXPLAIN ANALYZE Query Plan Analysis** (1 connections) — `.claude/skills/sql-pro/references/optimization.md`
- **Common Table Expressions (CTEs)** (1 connections) — `.claude/skills/sql-pro/references/query-patterns.md`
- **SQL Window Functions** (1 connections) — `.claude/skills/sql-pro/references/window-functions.md`

## Relationships

- [[render_consent_pdf()]] (7 shared connections)
- [[CLAUDE.md — Project AI Instructions]] (3 shared connections)
- [[Community 361]] (2 shared connections)
- [[Community 513]] (1 shared connections)
- [[Serena Project Configuration]] (1 shared connections)
- [[Node.js Essentials Reference]] (1 shared connections)
- [[007_add_ngo_davcna.py]] (1 shared connections)

## Source Files

- `.claude/skills/sql-pro/SKILL.md`
- `.claude/skills/sql-pro/references/database-design.md`
- `.claude/skills/sql-pro/references/dialect-differences.md`
- `.claude/skills/sql-pro/references/optimization.md`
- `.claude/skills/sql-pro/references/query-patterns.md`
- `.claude/skills/sql-pro/references/window-functions.md`
- `CLAUDE.md`
- `README.md`
- `SPEC.md`

## Audit Trail

- EXTRACTED: 52 (87%)
- INFERRED: 8 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*