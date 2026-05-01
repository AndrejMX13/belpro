# Belpro — Suggested Commands

> All commands run in WSL2 (Ubuntu) terminal — not Windows PowerShell.
> Docker Desktop must be running.

## Stack management
```bash
cp .env.example .env          # first time setup
docker compose up -d           # start all services
docker compose down            # stop all services
docker compose logs -f         # tail all logs
docker compose logs -f api     # tail specific service
docker compose ps              # check service status
docker compose build           # rebuild images after code change
```

## Database migrations
```bash
docker compose exec api alembic upgrade head      # apply migrations
docker compose exec api alembic revision --autogenerate -m "description"  # create migration
docker compose exec api alembic history           # show migration history
```

## Python (inside api container)
```bash
docker compose exec api black .       # format
docker compose exec api ruff check .  # lint
docker compose exec api pytest        # tests (when added)
```

## Access points
- Dashboard:      http://localhost:80
- FastAPI docs:   http://localhost:8100/docs
- n8n:            http://localhost:5678
- Evolution API:  http://localhost:8180

## Windows-specific
```powershell
# Check what's using a port (PowerShell)
netstat -ano | findstr ":8100"
```
