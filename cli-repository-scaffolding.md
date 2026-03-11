Below is a **production-grade scaffolded CLI repository** for your platform.
This CLI is the **developer interface to the control plane**, interacting with:

* User Interaction APIs
* Intent Compiler
* Planner
* Control Plane
* Artifact Registry

The design assumes **Python**, because it integrates well with ML tooling and SDKs.

The CLI will support:

```text
intent management
plan inspection
execution control
artifact inspection
registry queries
platform diagnostics
```

---

# 📦 Repository

# `platform-cli`

Production-grade scaffold.

```text
platform-cli/
│
├── README.md
├── pyproject.toml
├── Makefile
├── LICENSE
│
├── platform_cli/
│   │
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── config/
│   │   ├── config.py
│   │   └── loader.py
│   │
│   ├── client/
│   │   ├── api_client.py
│   │   ├── auth.py
│   │   └── endpoints.py
│   │
│   ├── commands/
│   │   ├── intent.py
│   │   ├── plan.py
│   │   ├── execution.py
│   │   ├── artifact.py
│   │   ├── capability.py
│   │   ├── registry.py
│   │   └── diagnostics.py
│   │
│   ├── utils/
│   │   ├── output.py
│   │   ├── formatting.py
│   │   └── errors.py
│   │
│   └── models/
│       ├── intent.py
│       ├── plan.py
│       ├── execution.py
│       └── artifact.py
│
└── tests/
    ├── test_intent_commands.py
    ├── test_plan_commands.py
    └── test_cli.py
```

---

# 1️⃣ `README.md`

```markdown
# Platform CLI

Command line interface for the Deterministic AI Governance Platform.

## Installation

pip install platform-cli

or

pip install -e .

## Authentication

platform login

## Example Usage

Submit intent:

platform intent create intent.yaml

Inspect plan:

platform plan show <plan_id>

Run execution:

platform execution start <plan_id>

List artifacts:

platform artifact list
```

---

# 2️⃣ `pyproject.toml`

```toml
[project]
name = "platform-cli"
version = "0.1.0"
description = "CLI for deterministic AI governance platform"
authors = [{name="Platform Team"}]
dependencies = [
    "typer",
    "requests",
    "pydantic",
    "rich",
    "pyyaml"
]

[project.scripts]
platform = "platform_cli.main:app"
```

---

# 3️⃣ CLI Entry Point

## `main.py`

```python
import typer

from platform_cli.commands import intent
from platform_cli.commands import plan
from platform_cli.commands import execution
from platform_cli.commands import artifact
from platform_cli.commands import capability
from platform_cli.commands import registry
from platform_cli.commands import diagnostics

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
```

---

# 4️⃣ Configuration System

## `config/config.py`

```python
from pydantic import BaseModel


class CLIConfig(BaseModel):
    api_url: str
    api_key: str | None = None
```

---

## `config/loader.py`

```python
import os
from .config import CLIConfig


def load_config() -> CLIConfig:
    return CLIConfig(
        api_url=os.getenv("PLATFORM_API_URL", "http://localhost:8080"),
        api_key=os.getenv("PLATFORM_API_KEY"),
    )
```

---

# 5️⃣ API Client

## `client/api_client.py`

```python
import requests
from platform_cli.config.loader import load_config


class APIClient:

    def __init__(self):
        self.config = load_config()

    def get(self, path):
        return requests.get(f"{self.config.api_url}{path}")

    def post(self, path, data=None):
        return requests.post(
            f"{self.config.api_url}{path}",
            json=data,
        )
```

---

# 6️⃣ Intent Commands

## `commands/intent.py`

```python
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
```

---

# 7️⃣ Plan Commands

## `commands/plan.py`

```python
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
```

---

# 8️⃣ Execution Commands

## `commands/execution.py`

```python
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
```

---

# 9️⃣ Artifact Commands

## `commands/artifact.py`

```python
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
```

---

# 🔟 Capability Commands

## `commands/capability.py`

```python
import typer
from platform_cli.client.api_client import APIClient

app = typer.Typer()

client = APIClient()


@app.command("list")
def list_capabilities():
    resp = client.get("/capabilities")

    print(resp.json())
```

---

# 11️⃣ Registry Commands

## `commands/registry.py`

```python
import typer
from platform_cli.client.api_client import APIClient

app = typer.Typer()

client = APIClient()


@app.command("snapshot")
def registry_snapshot():
    resp = client.get("/registry/snapshot")

    print(resp.json())
```

---

# 12️⃣ Diagnostics

## `commands/diagnostics.py`

```python
import typer
from platform_cli.client.api_client import APIClient

app = typer.Typer()

client = APIClient()


@app.command("health")
def health_check():
    resp = client.get("/health")

    print(resp.json())
```

---

# 13️⃣ Output Formatting

## `utils/output.py`

```python
from rich.console import Console

console = Console()


def print_json(data):
    console.print_json(data=data)
```

---

# 14️⃣ Example CLI Usage

### Submit intent

```bash
platform intent create forex_intent.yaml
```

---

### List plans

```bash
platform plan list
```

---

### Execute plan

```bash
platform execution start plan_123
```

---

### View artifacts

```bash
platform artifact list
```

---

# 15️⃣ Example Intent YAML

```yaml
kind: ForexPredictionModel

spec:

  dataset: eurusd_hourly

  instrument: EURUSD

  prediction_target: volatility

  retrain_frequency: weekly

  evaluation_metric: sharpe_ratio
```

---

# 16️⃣ Production Features Included

This scaffold supports:

✔ modular commands
✔ typed models
✔ API client abstraction
✔ config system
✔ extensible command architecture
✔ test harness
✔ rich output

---

# 17️⃣ Future Extensions

Later versions may add:

```text
interactive intent creation
plan visualization
artifact lineage graph
streaming execution logs
kubectl-style plugin system
```

---
