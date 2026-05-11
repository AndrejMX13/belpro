import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def write_env_key(key: str, value: str, env_path: Path) -> bool:
    """Update or append KEY=value in a .env file. Returns True on success, False on failure.

    Never raises — failures are logged as warnings. Existing key is replaced in-place;
    new keys are appended. Comments and unrelated lines are preserved.
    """
    try:
        if env_path.exists():
            lines = env_path.read_text(encoding="utf-8").splitlines(keepends=True)
            updated = False
            new_lines = []
            for line in lines:
                if line.startswith(f"{key}=") or line.startswith(f"{key} ="):
                    new_lines.append(f"{key}={value}\n")
                    updated = True
                else:
                    new_lines.append(line)
            if not updated:
                if new_lines and not new_lines[-1].endswith("\n"):
                    new_lines.append("\n")
                new_lines.append(f"{key}={value}\n")
            env_path.write_text("".join(new_lines), encoding="utf-8")
        else:
            env_path.write_text(f"{key}={value}\n", encoding="utf-8")
        return True
    except Exception as exc:
        logger.warning("Failed to write %s to %s: %s", key, env_path, exc)
        return False
