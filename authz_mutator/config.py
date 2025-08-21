from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List

import yaml

from .types import Config, EndpointTarget


def _coerce_target(raw: Dict[str, Any]) -> EndpointTarget:
    name = str(raw["name"])
    path = str(raw["path"]) 
    method = str(raw.get("method", "GET")).upper()
    headers = dict(raw.get("headers", {}))
    body = raw.get("body")
    mutations = list(raw.get("mutations", []))
    expect_success_statuses = list(raw.get("expect_success_statuses", [200, 201, 202, 204]))
    return EndpointTarget(
        name=name,
        path=path,
        method=method,
        headers=headers,
        body=body,
        mutations=mutations,
        expect_success_statuses=expect_success_statuses,
    )


def load_config(path: str) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    base_url = str(data["base_url"])  # required
    default_headers = dict(data.get("default_headers", {}))
    timeout_seconds = float(data.get("timeout_seconds", 10.0))

    raw_targets: List[Dict[str, Any]] = list(data.get("targets", []))
    targets = [_coerce_target(t) for t in raw_targets]

    return Config(
        base_url=base_url,
        default_headers=default_headers,
        timeout_seconds=timeout_seconds,
        targets=targets,
    )
