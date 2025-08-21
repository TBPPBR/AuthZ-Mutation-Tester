from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RequestSpec:
    method: str
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    json: Optional[Any] = None


@dataclass
class EndpointTarget:
    name: str
    path: str
    method: str
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None
    mutations: List[Dict[str, Any]] = field(default_factory=list)
    expect_success_statuses: List[int] = field(default_factory=lambda: [200, 201, 202, 204])


@dataclass
class Config:
    base_url: str
    default_headers: Dict[str, str] = field(default_factory=dict)
    timeout_seconds: float = 10.0
    targets: List[EndpointTarget] = field(default_factory=list)


@dataclass
class MutationResult:
    target_name: str
    mutation_description: str
    baseline_status: Optional[int]
    mutated_status: Optional[int]
    passed: bool
    message: str = ""
