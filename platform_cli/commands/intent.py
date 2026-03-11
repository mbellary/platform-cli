import typer
import yaml
from platform_cli.client.api_client import APIClient

app = typer.Typer()

client = APIClient()


@app.command("create")
def create_intent(file: str):
    """Submit intent artifact"""

    with open(file) as f:
        intent = yaml.safe_load(f)

    resp = client.post("/intents", intent)

    print(resp.json())


@app.command("list")
def list_intents():
    """List intents"""

    resp = client.get("/intents")

    print(resp.json())


@app.command("show")
def show_intent(intent_id: str):
    """Show intent"""

    resp = client.get(f"/intents/{intent_id}")

    print(resp.json())
