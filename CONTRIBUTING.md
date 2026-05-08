# Contributing to BelPro

Thanks for taking the time to contribute. BelPro is a self-hosted system for Slovenian NGOs that automates volunteer work diaries, built to meet Slovenian legal requirements.

## Quick links

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security policy](SECURITY.md)
- [Full system specification](SPEC.md)

## How to contribute

### Report a bug

Found something wrong? Open an issue using the **Bug Report** template. Include:

- What you were doing
- What you expected to happen
- What actually happened
- Steps to reproduce
- Docker logs if relevant (`docker compose logs`)

### Suggest a feature

Open an issue using the **Feature Request** template. Describe the problem you want to solve, not just the solution. Features that serve Slovenian NGO volunteers and managers are prioritized.

### Submit code

1. **Fork** the repository.
2. **Create a branch** from `main` — name it `fix/short-description` or `feat/short-description`.
3. **Make your changes.** Keep them focused. If a change spans multiple concerns, open a draft PR and discuss first.
4. **Follow coding standards.** The main ones:
   - Python: type hints, `black` formatting, `ruff` linting, Pydantic schemas, async FastAPI routes
   - Frontend: plain HTML/CSS/vanilla JS — no frameworks
   - n8n: export workflow JSON and commit to `n8n/workflows/`
   - Database: all schema changes via Alembic migrations
   - ASCII-only identifiers (Slovenian characters in user-facing text only)
5. **Open a PR** against `main`. Use the pull request template.
6. **PRs that add features** should also update `SPEC.md` if the feature changes behaviour.

### First-time contributors

Look for issues labeled `good first issue`. These are scoped small and have context in the issue description.

## Development setup

Follow the [README — Installation](README.md#installation) to get a local instance running. The stack runs in Docker Compose.

```bash
git clone https://github.com/AndrejMX13/belpro.git
cd belpro
cp .env.example .env   # fill in required values
docker compose up -d
docker compose exec api alembic upgrade head
```

## Communication

Discussions happen on GitHub Issues. If you have a question that isn't a bug or feature request, open a **Discussion** (if enabled) or a regular issue.

## What's in scope (v1)

BelPro is intentionally focused: single manager per instance, Slovenian language only, no multi-tenancy. Read [SPEC.md](SPEC.md) and the README's [Out of scope](README.md#out-of-scope-v1) section before proposing new directions.
