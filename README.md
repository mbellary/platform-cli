# Platform CLI

Command line interface for the Deterministic AI Governance Platform.

## Installation

Using `uv` (recommended):

```bash
uv sync
```

Run the CLI:

```bash
uv run platform --help
```

## Development checks

```bash
uv run ruff check .
uv run pytest
```

## Authentication

```bash
platform login
```

## Example Usage

Submit intent:

```bash
platform intent create intent.yaml
```

Inspect plan:

```bash
platform plan show <plan_id>
```

Run execution:

```bash
platform execution start <plan_id>
```

List artifacts:

```bash
platform artifact list
```
