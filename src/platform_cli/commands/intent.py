from __future__ import annotations

import typer
import yaml

from platform_cli.commands.common import (
    API_KEY_OPTION,
    API_URL_OPTION,
    CONFIG_OPTION,
    OUTPUT_OPTION,
    PROFILE_OPTION,
    build_service,
    handle_cli_error,
)
from platform_cli.utils.output import emit

app = typer.Typer()


@app.command("create")
def create_intent(
    file: str,
    profile: str = PROFILE_OPTION,
    config: str | None = CONFIG_OPTION,
    api_url: str | None = API_URL_OPTION,
    api_key: str | None = API_KEY_OPTION,
    output: str = OUTPUT_OPTION,
):
    try:
        with open(file, encoding="utf-8") as f:
            payload = yaml.safe_load(f)
        service, out = build_service(profile, config, api_url, api_key, output)
        emit(service.create_resource("intents", payload), out)
    except Exception as exc:
        handle_cli_error(exc)


@app.command("list")
def list_intents(
    limit: int = typer.Option(50),
    offset: int = typer.Option(0),
    sort: str | None = typer.Option(None),
    profile: str = PROFILE_OPTION,
    config: str | None = CONFIG_OPTION,
    api_url: str | None = API_URL_OPTION,
    api_key: str | None = API_KEY_OPTION,
    output: str = OUTPUT_OPTION,
):
    try:
        service, out = build_service(profile, config, api_url, api_key, output)
        query = {"limit": limit, "offset": offset, "sort": sort}
        emit(service.list_resources("intents", query), out)
    except Exception as exc:
        handle_cli_error(exc)


@app.command("show")
def show_intent(
    intent_id: str,
    profile: str = PROFILE_OPTION,
    config: str | None = CONFIG_OPTION,
    api_url: str | None = API_URL_OPTION,
    api_key: str | None = API_KEY_OPTION,
    output: str = OUTPUT_OPTION,
):
    try:
        service, out = build_service(profile, config, api_url, api_key, output)
        emit(service.get_resource("intents", intent_id), out)
    except Exception as exc:
        handle_cli_error(exc)


@app.command("delete")
def delete_intent(
    intent_id: str,
    yes: bool = typer.Option(False, "--yes"),
    profile: str = PROFILE_OPTION,
    config: str | None = CONFIG_OPTION,
    api_url: str | None = API_URL_OPTION,
    api_key: str | None = API_KEY_OPTION,
    output: str = OUTPUT_OPTION,
):
    if not yes:
        typer.echo("Refusing destructive operation without --yes", err=True)
        raise typer.Exit(code=1)
    try:
        service, out = build_service(profile, config, api_url, api_key, output)
        emit(service.delete_resource("intents", intent_id), out)
    except Exception as exc:
        handle_cli_error(exc)
