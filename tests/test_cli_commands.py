from __future__ import annotations

from typer.testing import CliRunner

from platform_cli.main import app

runner = CliRunner()


def test_intent_delete_requires_yes():
    result = runner.invoke(app, ["intent", "delete", "abc"])
    assert result.exit_code == 1
    assert "--yes" in result.stderr
