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


@app.command("list")
def list_plans(
    limit: int = typer.Option(50),
    offset: int = typer.Option(0),
    profile: str = PROFILE_OPTION,
    config: str | None = CONFIG_OPTION,
    api_url: str | None = API_URL_OPTION,
    api_key: str | None = API_KEY_OPTION,
    output: str = OUTPUT_OPTION,
):
    try:
        service, out = build_service(profile, config, api_url, api_key, output)
        emit(service.list_resources("plans", {"limit": limit, "offset": offset}), out)
    except Exception as exc:
        handle_cli_error(exc)


@app.command("show")
def show_plan(
    plan_id: str,
    profile: str = PROFILE_OPTION,
    config: str | None = CONFIG_OPTION,
    api_url: str | None = API_URL_OPTION,
    api_key: str | None = API_KEY_OPTION,
    output: str = OUTPUT_OPTION,
):
    try:
        service, out = build_service(profile, config, api_url, api_key, output)
        emit(service.get_resource("plans", plan_id), out)
    except Exception as exc:
        handle_cli_error(exc)


@app.command("create")
def create_plan(
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
        emit(service.create_resource("plans", payload), out)
    except Exception as exc:
        handle_cli_error(exc)
