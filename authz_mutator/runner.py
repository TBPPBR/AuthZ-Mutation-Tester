from __future__ import annotations

from copy import deepcopy
from typing import List, Optional

from .http_client import HttpClient
from .mutations import parse_mutation
from .types import Config, EndpointTarget, MutationResult, RequestSpec


def _build_spec(cfg: Config, target: EndpointTarget) -> RequestSpec:
    headers = {**cfg.default_headers, **(target.headers or {})}
    url = target.path  # base_url handled by httpx Client
    return RequestSpec(method=target.method, url=url, headers=headers, json=deepcopy(target.body))


def run_target(cfg: Config, client: HttpClient, target: EndpointTarget) -> List[MutationResult]:
    results: List[MutationResult] = []

    baseline_spec = _build_spec(cfg, target)
    baseline_status: Optional[int] = None
    try:
        resp = client.send(baseline_spec)
        baseline_status = resp.status_code
    except Exception as e:
        # Treat baseline failure as a failure to proceed, but still attempt mutations for visibility
        results.append(
            MutationResult(
                target_name=target.name,
                mutation_description="baseline",
                baseline_status=None,
                mutated_status=None,
                passed=False,
                message=f"baseline request error: {e}",
            )
        )

    # Determine if baseline is considered success (allowed)
    baseline_allowed = baseline_status in set(target.expect_success_statuses) if baseline_status is not None else False

    for m_spec in target.mutations:
        mutation = parse_mutation(m_spec)
        mutated = deepcopy(baseline_spec)
        mutation.apply(mutated)
        mutated_status: Optional[int] = None
        message = ""
        try:
            resp = client.send(mutated)
            mutated_status = resp.status_code
        except Exception as e:
            message = f"mutated request error: {e}"

        # Policy: if baseline was allowed, mutated should be denied (status not in expect_success_statuses)
        # If baseline was denied, mutated should remain denied as well.
        expected_denied = True
        is_denied = (mutated_status not in set(target.expect_success_statuses)) if mutated_status is not None else True
        passed = is_denied is expected_denied

        results.append(
            MutationResult(
                target_name=target.name,
                mutation_description=mutation.describe(),
                baseline_status=baseline_status,
                mutated_status=mutated_status,
                passed=passed,
                message=message,
            )
        )

    return results


def run_all(cfg: Config) -> List[MutationResult]:
    all_results: List[MutationResult] = []
    with HttpClient(base_url=cfg.base_url, timeout_seconds=cfg.timeout_seconds) as client:
        for target in cfg.targets:
            all_results.extend(run_target(cfg, client, target))
    return all_results
