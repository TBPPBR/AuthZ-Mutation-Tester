from __future__ import annotations

from typing import Optional

import httpx

from .types import RequestSpec


class HttpClient:
    def __init__(self, base_url: str, timeout_seconds: float) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout_seconds, follow_redirects=True)

    def close(self) -> None:
        self._client.close()

    def send(self, spec: RequestSpec) -> httpx.Response:
        return self._client.request(
            method=spec.method,
            url=spec.url,
            headers=spec.headers or None,
            json=spec.json,
        )

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
