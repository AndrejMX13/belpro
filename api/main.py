"""Belpro FastAPI application entry point."""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from db.session import AsyncSessionLocal
from routers.analytics import router as analytics_router
from routers.log_entries import router as log_entries_router
from routers.managers import router as managers_router
from routers.reports import router as reports_router
from routers.volunteers import router as volunteers_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Fail fast if the database is unreachable on startup."""
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))
    yield


app = FastAPI(
    title="BelPro API",
    description="Volunteer diary management API for Slovenian NGOs.",
    version="0.9.3",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics_router, prefix="/api")
app.include_router(log_entries_router, prefix="/api")
app.include_router(managers_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(volunteers_router, prefix="/api")


@app.get("/api/health")
async def health() -> dict[str, str]:
    """Health check — returns ok when the service is up."""
    return {"status": "ok"}
