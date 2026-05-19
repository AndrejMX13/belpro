"""Belpro FastAPI application entry point."""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import Settings, get_settings
from db.session import AsyncSessionLocal
from models.manager import Manager
from utils.phone import normalize_phone
from routers.auth import router as auth_router
from routers.analytics import router as analytics_router
from routers.log_entries import router as log_entries_router
from routers.logo import router as logo_router
from routers.managers import router as managers_router
from routers.reports import router as reports_router
from routers.volunteers import router as volunteers_router

__version__ = "0.10.0-beta.2"


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

app.include_router(auth_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(log_entries_router, prefix="/api")
app.include_router(logo_router, prefix="/api")
app.include_router(managers_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(volunteers_router, prefix="/api")


@app.get("/api/health")
async def health() -> dict[str, str]:
    """Health check — returns ok when the service is up."""
    return {"status": "ok"}
