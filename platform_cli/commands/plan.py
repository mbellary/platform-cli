import typer
from platform_cli.client.api_client import APIClient

app = typer.Typer()

client = APIClient()


@app.command("list")
def list_plans():
    resp = client.get("/plans")

    print(resp.json())


@app.command("show")
def show_plan(plan_id: str):
    resp = client.get(f"/plans/{plan_id}")

    print(resp.json())
