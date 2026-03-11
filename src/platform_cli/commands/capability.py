import typer

from platform_cli.client.api_client import APIClient

app = typer.Typer()

client = APIClient()


@app.command("list")
def list_capabilities():
    resp = client.get("/capabilities")

    print(resp.json())
