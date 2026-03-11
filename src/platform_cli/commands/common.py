from __future__ import annotations

from pathlib import Path
from typing import Any

import typer

from platform_cli.client.api_client import APIClient
from platform_cli.client.auth import load_token
from platform_cli.config.loader import ConfigError, load_config
from platform_cli.services.platform_service import PlatformService
from platform_cli.utils.errors import CLIError, ConfigLoadError

OUTPUT_OPTION = typer.Option("table", "--output", help="Output mode: table|json|yaml")
PROFILE_OPTION = typer.Option("default", "--profile", help="Configuration profile to use")
CONFIG_OPTION = typer.Option(None, "--config", help="Path to config file")
API_URL_OPTION = typer.Option(None, "--api-url", help="Override API base URL")
API_KEY_OPTION = typer.Option(None, "--api-key", help="Override API key")


def build_service(
    profile: str,
    config: str | None,
    api_url: str | None,
    api_key: str | None,
    output: str,
) -> tuple[PlatformService, str]:
    overrides: dict[str, Any] = {
        "api_url": api_url,
        "api_key": api_key,
        "output": output,
    }
    cfg = load_config(profile=profile, config_path=config, overrides=overrides)
    token = load_token(Path(cfg.token_path))
    if token and not cfg.token:
        cfg = cfg.model_copy(update={"token": token})
    return PlatformService(APIClient(cfg)), cfg.output


def handle_cli_error(exc: Exception) -> None:
    if isinstance(exc, ConfigError):
        raise typer.Exit(code=ConfigLoadError(str(exc)).exit_code) from exc
    if isinstance(exc, CLIError):
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=exc.exit_code) from exc
    typer.echo(f"Unexpected error: {exc}", err=True)
    raise typer.Exit(code=1) from exc
