import typer
from platform_cli.client.api_client import APIClient

app = typer.Typer()

client = APIClient()


@app.command("list")
def list_artifacts():
    resp = client.get("/artifacts")

    print(resp.json())


@app.command("show")
def show_artifact(artifact_id: str):
    resp = client.get(f"/artifacts/{artifact_id}")

    print(resp.json())
