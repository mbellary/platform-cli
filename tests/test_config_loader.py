from __future__ import annotations

from platform_cli.config.loader import load_config


def test_config_precedence(tmp_path, monkeypatch):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
profiles:
  default:
    api_url: https://file.example
    output: yaml
    retry_attempts: 2
"""
    )
    monkeypatch.setenv("PLATFORM_API_URL", "https://env.example")
    cfg = load_config(
        config_path=config_file,
        overrides={"api_url": "https://cli.example", "output": "json"},
    )
    assert cfg.api_url == "https://cli.example"
    assert cfg.output == "json"
    assert cfg.retry_attempts == 2


def test_unknown_profile_fails(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("profiles: {default: {api_url: https://file.example}}")
    try:
        load_config(profile="prod", config_path=config_file)
    except Exception as exc:
        assert "Unknown profile" in str(exc)
    else:
        raise AssertionError("Expected unknown profile failure")
