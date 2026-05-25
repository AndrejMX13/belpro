# BelPro Project Memory — Public Index

Project knowledge that travels with the repo. Load individual files when relevant.

## Conventions & Naming
- [BelPro name](feedback_belpro_name.md) — always "BelPro" (capital P), never "Belpro" or "belpro"
- [Issue workflow](feedback_issue_workflow.md) — ISS-NNN in commits is fine; remind user to manual-test before closing issue

## Packaging & Dependencies
- [email-validator pin](feedback_email_validator.md) — must be pinned explicitly alongside pydantic[email]
- [pydyf pin](feedback_pydyf_pin.md) — weasyprint==62.3 needs pydyf==0.10.0 pinned explicitly

## Docker & Dev Environment
- [Docker rebuild](feedback_docker_restart.md) — use `docker compose up -d --build <svc>`, NOT `restart`, after code changes
- [Docker exec patterns](feedback_docker_exec_patterns.md) — use PowerShell for docker compose; pytest path inside container is `tests/` not `api/tests/`

## Tooling — Serena
- [Serena replace_symbol_body pitfalls](feedback_serena_replace_symbol.md) — drops decorators; corrupts module-level strings; use Edit tool instead
- [Serena memory](reference_serena_memory.md) — Serena memory directory currently empty (all migrated to Claude Code memory); tools may be used again in future

## Tooling — graphify
- [graphify orientation](feedback_graphify_orientation.md) — always read graphify wiki first to locate files; grep/Serena only after
- [graphify update](feedback_graphify_update.md) — run `graphify update .` after every session that modifies code files
- [graphify recovery scripts](reference_graphify_recovery.md) — 4-step recovery order when subagents write results to notifications instead of disk
- [graphify HTML large graph](feedback_graphify_html.md) — graph.html skipped (8 553 nodes > 5 000 limit); use `node_limit=1` to get aggregated community meta-graph instead
- [graphify infra script](reference_graphify_infra_script.md) — scripts/graphify_infra.py patches graph.json with Docker service topology; run after compose/nginx changes

## n8n Workflows
- [n8n workflow edits](feedback_n8n_workflow_edits.md) — edit JSON on disk + import via script; never pass full workflow through subagents or n8n-mcp
- [n8n import script](feedback_n8n_import_script.md) — CRITICAL: always run `python scripts/n8n_workflows.py import` after any workflow JSON edit
- [n8n API access](n8n_api_access.md) — two API surfaces: /rest/ (cookie auth) vs /api/v1/ (API key); export via node inside container + docker cp

## Infrastructure
- [Evolution API QR fix](project_evolution_qr.md) — v2.2.3 needs CONFIG_SESSION_PHONE_VERSION set; QR modal broken; use API + qr.html workaround
- [Evolution API key distinction](feedback_evolution_api_keys.md) — AUTHENTICATION_API_KEY (global) ≠ EVOLUTION_API_KEY (per-instance); never treat as same

## Git & Commits
- [Commit git status check](feedback_commit_git_status.md) — always run git status before committing; graphify outputs must be in same commit
- [Plan file commit gap](feedback_plan_file_commit.md) — docs/superpowers/plans/ files are untracked after subagent runs; commit manually before push

## Architecture
- [Error reporting pattern](project_error_reporting_pattern.md) — external callers POST to /api/errors; internal API writes ErrorLog rows directly via DB session
- [AppSetting / Sistemske nastavitve](project_app_settings.md) — generic key-value settings table + AppSettings service; add new settings via property + schema + admin.js field
- [FastAPI lifespan](project_fastapi_lifespan.md) — startup/shutdown logic lives in lifespan context manager, not deprecated on_event handlers

## Release
- [Release versioning strategy](project_versioning.md) — alpha → beta (scope freeze) → RC1 → 1.0.0

## Superpowers
- [Superpowers discipline](feedback_superpowers_discipline.md) — always invoke relevant skills before starting any task, even complex ones already in progress

## Project State
- [README screenshots placeholder](project_readme_screenshots.md) — dashboard section in both READMEs ready to receive screenshots (ISS-019)
