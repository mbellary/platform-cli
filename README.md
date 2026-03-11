# platform-cli

Deterministic governance platform CLI.

## Quickstart

```bash
pip install -e .
platform --help
```

## Configuration

Configuration precedence: defaults < config file profile < environment variables < CLI flags.

Default config path: `~/.platform-cli/config.yaml`

```yaml
profiles:
  default:
    api_url: https://api.example.com
    timeout_seconds: 10
    retry_attempts: 3
    output: table
```

## Authentication

```bash
platform auth login --token <token>
platform auth whoami
platform auth logout
```

## Output modes

All commands support `--output table|json|yaml`.
