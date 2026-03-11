from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CLIConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    api_url: str = "http://localhost:8080"
    api_key: str | None = None
    token: str | None = None
    profile: str = "default"
    timeout_seconds: float = 10.0
    retry_attempts: int = 3
    retry_backoff_seconds: float = 0.4
    output: str = "table"
    config_path: Path = Field(default_factory=lambda: Path.home() / ".platform-cli" / "config.yaml")
    token_path: Path = Field(default_factory=lambda: Path.home() / ".platform-cli" / "token.json")

    @field_validator("output")
    @classmethod
    def validate_output(cls, value: str) -> str:
        supported = {"table", "json", "yaml"}
        if value not in supported:
            raise ValueError(f"output must be one of {sorted(supported)}")
        return value


class ConfigFile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    profiles: dict[str, dict] = Field(default_factory=dict)
