"""Belpro FastAPI application entry point."""
from __future__ import annotations

import shutil
import time
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Annotated, AsyncGenerator

import httpx
from fastapi import Depends, FastAPI
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import Settings, get_settings
from db.session import AsyncSessionLocal, get_db
from models.log_entry import LogEntry
from models.manager import Manager
from models.monthly_report import MonthlyReport
from utils.phone import normalize_phone
from routers.admin import router as admin_router
from routers.auth import router as auth_router
from routers.analytics import router as analytics_router
from routers.log_entries import router as log_entries_router
from routers.logo import router as logo_router
from routers.managers import router as managers_router
from routers.reports import router as reports_router
from routers.volunteers import router as volunteers_router
from routers.documents import router as documents_router
from routers.errors import router as errors_router
from routers.config import router as config_router

__version__ = "0.11.1-beta.0"


async def seed_whatsapp_phone_from_env(
    session: AsyncSession, settings: Settings
) -> None:
    """Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null."""
    if not settings.ngo_whatsapp_phone:
        return
    normalized = normalize_phone(settings.ngo_whatsapp_phone)
    if not normalized:
        return
    manager = (await session.execute(select(Manager).limit(1))).scalar_one_or_none()
    if manager and not manager.ngo_whatsapp_phone:
        manager.ngo_whatsapp_phone = normalized
        await session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Fail fast if DB unreachable; seed WhatsApp phone from .env if DB null."""
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))

    settings = get_settings()
    async with AsyncSessionLocal() as session:
        await seed_whatsapp_phone_from_env(session, settings)

    yield


app = FastAPI(
    title="BelPro API",
    description="Volunteer diary management API for Slovenian NGOs.",
    version=__version__,
    lifespan=lifespan,
)

app.include_router(admin_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(log_entries_router, prefix="/api")
app.include_router(logo_router, prefix="/api")
app.include_router(managers_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(volunteers_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(errors_router, prefix="/api")
app.include_router(config_router, prefix="/api")


@app.get("/api/health")
async def health() -> dict[str, str]:
    """Health check — returns ok when the service is up."""
    return {"status": "ok"}


@app.get("/api/health/detailed")
async def health_detailed(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Per-service health status for the manager dashboard widget."""
    result: dict = {}
    settings = get_settings()

    # PostgreSQL
    try:
        t0 = time.monotonic()
        await db.execute(text("SELECT 1"))
        result["postgres"] = {
            "status": "ok",
            "response_ms": round((time.monotonic() - t0) * 1000),
        }
    except Exception as exc:
        result["postgres"] = {"status": "error", "detail": str(exc)}

    # Whisper
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get("http://whisper:8001/health")
        result["whisper"] = {"status": "ok" if r.status_code == 200 else "error"}
    except Exception as exc:
        result["whisper"] = {"status": "error", "detail": str(exc)}

    # n8n
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get("http://n8n:5678/healthz")
        result["n8n"] = {"status": "ok" if r.status_code == 200 else "error"}
    except Exception as exc:
        result["n8n"] = {"status": "error", "detail": str(exc)}

    # Evolution API — fetch instance connection state
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(
                "http://evolution-api:8080/instance/fetchInstances",
                headers={"apikey": settings.authentication_api_key},
            )
        if r.status_code == 200:
            instances = r.json()
            instance = next(
                (i for i in instances if i.get("name") == settings.evolution_instance_name),
                None,
            )
            state = instance.get("connectionStatus", "unknown") if instance else "not_found"
            result["evolution"] = {
                "status": "ok" if state == "open" else "warning",
                "connection_state": state,
            }
        else:
            result["evolution"] = {"status": "error", "detail": f"HTTP {r.status_code}"}
    except Exception as exc:
        result["evolution"] = {"status": "error", "detail": str(exc)}

    # Disk
    try:
        usage = shutil.disk_usage("/app/photos")
        free_pct = usage.free / usage.total * 100
        result["disk"] = {
            "status": "ok" if free_pct > 15 else ("warning" if free_pct > 5 else "error"),
            "free_gb": round(usage.free / 1_000_000_000, 1),
            "free_pct": round(free_pct, 1),
        }
    except Exception as exc:
        result["disk"] = {"status": "error", "detail": str(exc)}

    # Heartbeat
    try:
        last_entry = (
            await db.execute(select(func.max(LogEntry.created_at)))
        ).scalar()
        last_report = (
            await db.execute(select(func.max(MonthlyReport.generated_at)))
        ).scalar()
        result["heartbeat"] = {
            "last_entry": last_entry.isoformat() if last_entry else None,
            "last_report": last_report.isoformat() if last_report else None,
        }
    except Exception as exc:
        result["heartbeat"] = {"status": "error", "detail": str(exc)}

    return result
