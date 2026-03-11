from __future__ import annotations

from typing import Any

import typer
import yaml
from rich.console import Console
from rich.table import Table

console = Console()


def emit(data: Any, output_format: str = "table") -> None:
    if output_format == "json":
        console.print_json(data=data)
        return
    if output_format == "yaml":
        console.print(yaml.safe_dump(data, sort_keys=False))
        return
    _print_table(data)


def _print_table(data: Any) -> None:
    if isinstance(data, list):
        if not data:
            typer.echo("No records found.")
            return
        if isinstance(data[0], dict):
            table = Table(show_header=True)
            keys = list(data[0].keys())
            for k in keys:
                table.add_column(str(k))
            for row in data:
                table.add_row(*[str(row.get(k, "")) for k in keys])
            console.print(table)
            return
    if isinstance(data, dict):
        table = Table(show_header=False)
        table.add_column("key")
        table.add_column("value")
        for key, value in data.items():
            table.add_row(str(key), str(value))
        console.print(table)
        return
    typer.echo(str(data))
