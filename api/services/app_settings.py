"""AppSettings — central authority for all configuration.

Wraps the env-only Settings class. The three DB-tunable fields are resolved
from the settings table with env fallback. All other attributes delegate
transparently to the underlying Settings instance via __getattr__.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import Settings, get_settings
from db.session import get_db
from models.app_setting import AppSetting


class AppSettings:
    """Central authority for all configuration — env base + DB runtime overrides."""

    def __init__(self, env: Settings, db_overrides: dict[str, str]) -> None:
        self._env = env
        self._db = db_overrides

    # ── typed helpers ──────────────────────────────────────────────────────────
    # All values are stored as TEXT in the DB. Each helper converts to the
    # correct Python type, falling back to the env default when the row is absent.

    def _int(self, name: str, default: int) -> int:
        """Resolve an integer setting: DB value first, env default fallback.

        Falls back to default if the stored value cannot be parsed as int
        (e.g. manual DB edit) to avoid locking out the manager on corrupt config.
        """
        raw = self._db.get(name)
        if raw is None:
            return default
        try:
            return int(raw)
        except ValueError:
            return default

    def _bool(self, name: str, default: bool) -> bool:
        """Resolve a boolean setting: 'true'/'1'/'yes' → True, else False."""
        raw = self._db.get(name)
        return raw.lower() in ("true", "1", "yes") if raw is not None else default

    def _str(self, name: str, default: str | None) -> str | None:
        """Resolve a string setting: DB value first, default fallback."""
        raw = self._db.get(name)
        return raw if raw is not None else default

    # ── DB-tunable properties ──────────────────────────────────────────────────

    @property
    def max_photos_per_entry(self) -> int:
        """Maximum photos allowed per log entry."""
        return self._int("max_photos_per_entry", self._env.max_photos_per_entry)

    @property
    def photo_retention_days(self) -> int:
        """Number of days approved entry photos are retained on disk."""
        return self._int("photo_retention_days", self._env.photo_retention_days)

    @property
    def session_duration_hours(self) -> int:
        """Manager session cookie lifetime in hours."""
        return self._int("session_duration_hours", self._env.session_duration_hours)

    @property
    def report_auto_day(self) -> int:
        """Day of month (1–28) on which monthly reports are auto-sent."""
        return max(1, min(self._int("report_auto_day", 28), 28))

    @property
    def report_auto_period(self) -> str:
        """Reporting period: 'current' (this month) or 'previous' (last month)."""
        raw = self._str("report_auto_period", "current") or "current"
        return raw if raw in ("current", "previous") else "current"

    @property
    def backup_hour(self) -> int:
        """Hour of day (0–23) at which the daily backup runs."""
        return max(0, min(self._int("backup_hour", 2), 23))

    @property
    def photo_cleanup_hour(self) -> int:
        """Hour of day (0–23) at which the daily photo cleanup runs."""
        return max(0, min(self._int("photo_cleanup_hour", 3), 23))

    @property
    def report_auto_hour(self) -> int:
        """Hour of day (0–23) at which the monthly report cron fires."""
        return max(0, min(self._int("report_auto_hour", 7), 23))

    @property
    def backup_retention_days(self) -> int:
        """Number of days local backup archives are kept before pruning."""
        return max(1, self._int("backup_retention_days", 30))

    # ── passthrough for all other env settings ─────────────────────────────────

    def __getattr__(self, name: str) -> object:
        """Delegate any non-overridden attribute to the underlying env Settings."""
        return getattr(self._env, name)


async def get_app_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
    env: Annotated[Settings, Depends(get_settings)],
) -> AppSettings:
    """FastAPI dependency — returns the central settings authority for this request."""
    rows = (await db.execute(select(AppSetting))).scalars().all()
    return AppSettings(env, {r.name: r.value for r in rows if r.value is not None})
