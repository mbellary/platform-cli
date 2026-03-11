import typer
from platform_cli.client.api_client import APIClient

app = typer.Typer()

client = APIClient()


@app.command("start")
def start_execution(plan_id: str):
    resp = client.post(f"/executions/start/{plan_id}")

    print(resp.json())


@app.command("status")
def execution_status(exec_id: str):
    resp = client.get(f"/executions/{exec_id}")

    print(resp.json())
