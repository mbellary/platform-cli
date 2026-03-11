import typer

from platform_cli.commands import (
    artifact,
    capability,
    diagnostics,
    execution,
    intent,
    plan,
    registry,
)

app = typer.Typer()

app.add_typer(intent.app, name="intent")
app.add_typer(plan.app, name="plan")
app.add_typer(execution.app, name="execution")
app.add_typer(artifact.app, name="artifact")
app.add_typer(capability.app, name="capability")
app.add_typer(registry.app, name="registry")
app.add_typer(diagnostics.app, name="diagnostics")

if __name__ == "__main__":
    app()
