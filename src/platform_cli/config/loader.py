from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from .config import CLIConfig, ConfigFile

ENV_MAP = {
    "api_url": "PLATFORM_API_URL",
    "api_key": "PLATFORM_API_KEY",
    "token": "PLATFORM_API_TOKEN",
    "timeout_seconds": "PLATFORM_TIMEOUT_SECONDS",
    "retry_attempts": "PLATFORM_RETRY_ATTEMPTS",
    "retry_backoff_seconds": "PLATFORM_RETRY_BACKOFF_SECONDS",
    "output": "PLATFORM_OUTPUT",
}


class ConfigError(ValueError):
    pass


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text()) or {}
    if not isinstance(loaded, dict):
        raise ConfigError(f"Config file must contain a YAML object: {path}")
    return loaded


def load_config(
    profile: str = "default",
    config_path: str | Path | None = None,
    overrides: dict[str, Any] | None = None,
) -> CLIConfig:
    overrides = overrides or {}
    path = Path(config_path).expanduser() if config_path else CLIConfig().config_path

    base_values = CLIConfig().model_dump()
    base_values["profile"] = profile
    base_values["config_path"] = path

    file_values: dict[str, Any] = {}
    raw = _read_yaml(path)
    if raw:
        parsed = ConfigFile.model_validate(raw)
        profile_values = parsed.profiles.get(profile)
        if profile_values is None:
            available = ", ".join(sorted(parsed.profiles)) or "none"
            raise ConfigError(f"Unknown profile '{profile}'. Available profiles: {available}")
        file_values = profile_values

    env_values: dict[str, Any] = {}
    for key, env_name in ENV_MAP.items():
        env_val = os.getenv(env_name)
        if env_val is not None:
            env_values[key] = env_val

    merged = {
        **base_values,
        **file_values,
        **env_values,
        **{k: v for k, v in overrides.items() if v is not None},
    }

    return CLIConfig.model_validate(merged)
