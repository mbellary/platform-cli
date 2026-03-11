from __future__ import annotations

import requests

from platform_cli.client.api_client import APIClient
from platform_cli.config.config import CLIConfig
from platform_cli.utils.errors import TransportError


class DummyResponse:
    def __init__(self, status_code=200, payload=None, text="", content=b"x"):
        self.status_code = status_code
        self._payload = payload or {"ok": True}
        self.text = text
        self.content = content

    def json(self):
        return self._payload


def test_client_retries(monkeypatch):
    cfg = CLIConfig(retry_attempts=2)
    client = APIClient(cfg)
    calls = {"count": 0}

    def flaky(*args, **kwargs):
        calls["count"] += 1
        raise requests.Timeout("timeout")

    monkeypatch.setattr(client.session, "request", flaky)

    try:
        client.get("/health")
    except TransportError:
        pass
    else:
        raise AssertionError("expected transport error")

    assert calls["count"] == 2


def test_client_success(monkeypatch):
    cfg = CLIConfig()
    client = APIClient(cfg)
    monkeypatch.setattr(
        client.session, "request", lambda *args, **kwargs: DummyResponse(payload={"a": 1})
    )
    assert client.get("/x") == {"a": 1}
