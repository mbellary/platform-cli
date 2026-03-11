from __future__ import annotations

import typer

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


@app.command("snapshot")
def registry_snapshot(
    profile: str = PROFILE_OPTION,
    config: str | None = CONFIG_OPTION,
    api_url: str | None = API_URL_OPTION,
    api_key: str | None = API_KEY_OPTION,
    output: str = OUTPUT_OPTION,
):
    try:
        service, out = build_service(profile, config, api_url, api_key, output)
        emit(service.registry_snapshot(), out)
    except Exception as exc:
        handle_cli_error(exc)
