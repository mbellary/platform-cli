from __future__ import annotations

import typer

from platform_cli.client.auth import clear_token, save_token
from platform_cli.commands.common import (
    API_KEY_OPTION,
    API_URL_OPTION,
    CONFIG_OPTION,
    OUTPUT_OPTION,
    PROFILE_OPTION,
    build_service,
    handle_cli_error,
)
from platform_cli.config.loader import load_config
from platform_cli.utils.output import emit

app = typer.Typer()


@app.command("login")
def login(
    token: str = typer.Option(..., prompt=True, hide_input=True),
    profile: str = PROFILE_OPTION,
    config: str | None = CONFIG_OPTION,
):
    try:
        cfg = load_config(profile=profile, config_path=config)
        save_token(cfg.token_path, token)
        typer.echo("Login successful.")
    except Exception as exc:
        handle_cli_error(exc)


@app.command("logout")
def logout(profile: str = PROFILE_OPTION, config: str | None = CONFIG_OPTION):
    try:
        cfg = load_config(profile=profile, config_path=config)
        clear_token(cfg.token_path)
        typer.echo("Logged out.")
    except Exception as exc:
        handle_cli_error(exc)


@app.command("whoami")
def whoami(
    profile: str = PROFILE_OPTION,
    config: str | None = CONFIG_OPTION,
    api_url: str | None = API_URL_OPTION,
    api_key: str | None = API_KEY_OPTION,
    output: str = OUTPUT_OPTION,
):
    try:
        service, out = build_service(profile, config, api_url, api_key, output)
        emit(service.whoami(), out)
    except Exception as exc:
        handle_cli_error(exc)
