"""Config router — public read-only settings for n8n workflow consumption."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from services.app_settings import AppSettings, get_app_settings

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/evolution-instance")
async def get_evolution_instance(
    settings: Annotated[AppSettings, Depends(get_app_settings)],
) -> dict:
    """Return the Evolution API instance name. No auth required. Used by n8n workflows."""
    return {"instance_name": settings.evolution_instance_name}
