from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def save_token(token_path: Path, token: str) -> None:
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(json.dumps({"token": token}))
    token_path.chmod(0o600)


def load_token(token_path: Path) -> str | None:
    if not token_path.exists():
        return None
    data: dict[str, Any] = json.loads(token_path.read_text())
    return data.get("token")


def clear_token(token_path: Path) -> None:
    if token_path.exists():
        token_path.unlink()
