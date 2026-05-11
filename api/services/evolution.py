import logging

import httpx

from utils.phone import normalize_phone

logger = logging.getLogger(__name__)


class EvolutionClient:
    """Async HTTP client for the Evolution API WhatsApp gateway."""

    def __init__(self, base_url: str, api_key: str, instance_name: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._instance_name = instance_name

    async def get_connected_phone(self) -> tuple[str | None, str]:
        """Return (normalized_phone, state) for the configured instance.

        States: "open" | "connecting" | "close" | "unreachable" | "lid_unsupported"
        phone is non-None only when state is "open" and owner is a resolvable E.164 JID.

        v2.3.7 note: Android users may appear as @lid JIDs which cannot be resolved.
        Upgrade to v2.4.0+ if @lid owners are seen. See docs/evolution-lid-resolution.md.
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(
                    f"{self._base_url}/instance/fetchInstances",
                    headers={"apikey": self._api_key},
                )
                resp.raise_for_status()
                instances: list = resp.json()
        except Exception as exc:
            logger.warning("Evolution API unreachable at %s: %s", self._base_url, exc)
            return None, "unreachable"

        for item in instances:
            inst = item.get("instance", {})
            if inst.get("instanceName") != self._instance_name:
                continue

            # "status" is standard in v2.3.x; "state" appears in some versions
            state: str = inst.get("status") or inst.get("state") or "close"
            owner: str | None = inst.get("owner")

            if not owner:
                return None, state

            if owner.endswith("@lid"):
                logger.warning(
                    "Evolution API returned @lid JID for instance '%s' — "
                    "upgrade to v2.4.0+ to resolve. See docs/evolution-lid-resolution.md.",
                    self._instance_name,
                )
                return None, "lid_unsupported"

            phone = normalize_phone(owner.split("@")[0])
            return phone, state

        return None, "close"
