import typer
from platform_cli.client.api_client import APIClient

app = typer.Typer()

client = APIClient()


@app.command("health")
def health_check():
    resp = client.get("/health")

    print(resp.json())
