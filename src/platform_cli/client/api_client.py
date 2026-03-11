from __future__ import annotations

import time
from typing import Any

import requests

from platform_cli.config.config import CLIConfig
from platform_cli.utils.errors import AuthError, ServerError, TransportError


class APIClient:
    def __init__(self, config: CLIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if config.api_key:
            self.session.headers["X-API-Key"] = config.api_key
        if config.token:
            self.session.headers["Authorization"] = f"Bearer {config.token}"

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("GET", path, params=params)

    def post(self, path: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("POST", path, json=data)

    def put(self, path: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("PUT", path, json=data)

    def delete(self, path: str) -> dict[str, Any]:
        return self._request("DELETE", path)

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = f"{self.config.api_url.rstrip('/')}/{path.lstrip('/')}"
        errors: list[str] = []
        for attempt in range(1, self.config.retry_attempts + 1):
            try:
                response = self.session.request(
                    method,
                    url,
                    timeout=self.config.timeout_seconds,
                    **kwargs,
                )
                return self._handle_response(response)
            except requests.RequestException as exc:
                errors.append(str(exc))
                if attempt >= self.config.retry_attempts:
                    break
                time.sleep(self.config.retry_backoff_seconds * (2 ** (attempt - 1)))
        raise TransportError(f"Request failed after retries: {'; '.join(errors)}")

    def _handle_response(self, response: requests.Response) -> dict[str, Any]:
        if response.status_code in (401, 403):
            raise AuthError("Authentication failed. Run `platform auth login` and retry.")

        if response.status_code >= 500:
            raise ServerError(f"Server error ({response.status_code}): {response.text}")

        if response.status_code >= 400:
            raise TransportError(f"Request failed ({response.status_code}): {response.text}")

        if not response.content:
            return {"ok": True}
        try:
            payload = response.json()
        except ValueError as exc:
            raise TransportError(f"Invalid JSON response: {exc}") from exc
        if isinstance(payload, dict):
            return payload
        return {"data": payload}
