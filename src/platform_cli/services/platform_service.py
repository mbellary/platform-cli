from __future__ import annotations

from typing import Any

from platform_cli.client.api_client import APIClient


class PlatformService:
    def __init__(self, client: APIClient):
        self.client = client

    def list_resources(self, resource: str, query: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.client.get(f"/{resource}", params=query)

    def get_resource(self, resource: str, resource_id: str) -> dict[str, Any]:
        return self.client.get(f"/{resource}/{resource_id}")

    def create_resource(self, resource: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.client.post(f"/{resource}", data=payload)

    def update_resource(
        self, resource: str, resource_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return self.client.put(f"/{resource}/{resource_id}", data=payload)

    def delete_resource(self, resource: str, resource_id: str) -> dict[str, Any]:
        return self.client.delete(f"/{resource}/{resource_id}")

    def start_execution(self, plan_id: str) -> dict[str, Any]:
        return self.client.post(f"/executions/start/{plan_id}")

    def registry_snapshot(self) -> dict[str, Any]:
        return self.client.get("/registry/snapshot")

    def health(self) -> dict[str, Any]:
        return self.client.get("/health")

    def whoami(self) -> dict[str, Any]:
        return self.client.get("/auth/whoami")
