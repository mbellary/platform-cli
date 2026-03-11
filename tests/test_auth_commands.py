from __future__ import annotations

from typer.testing import CliRunner

from platform_cli.main import app

runner = CliRunner()


def test_login_logout(tmp_path):
    cfg = tmp_path / "config.yaml"
    token_path = tmp_path / "token.json"
    cfg.write_text(
        f"""
profiles:
  default:
    token_path: {token_path}
"""
    )

    result = runner.invoke(app, ["auth", "login", "--config", str(cfg), "--token", "abc"])
    assert result.exit_code == 0
    assert token_path.exists()

    result = runner.invoke(app, ["auth", "logout", "--config", str(cfg)])
    assert result.exit_code == 0
    assert not token_path.exists()
