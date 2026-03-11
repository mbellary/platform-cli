import typer
from platform_cli.client.api_client import APIClient

app = typer.Typer()

client = APIClient()


@app.command("snapshot")
def registry_snapshot():
    resp = client.get("/registry/snapshot")

    print(resp.json())
