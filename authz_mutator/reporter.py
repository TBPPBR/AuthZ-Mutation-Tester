from __future__ import annotations

from typing import List
import json
from dataclasses import asdict

from rich.console import Console
from rich.table import Table

from .types import MutationResult


def print_results(results: List[MutationResult]) -> int:
    console = Console()
    table = Table(title="AuthZ Mutation Results")
    table.add_column("Target")
    table.add_column("Mutation")
    table.add_column("Baseline")
    table.add_column("Mutated")
    table.add_column("Result")
    table.add_column("Message")

    failures = 0
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        if not r.passed:
            failures += 1
        table.add_row(
            r.target_name,
            r.mutation_description,
            str(r.baseline_status) if r.baseline_status is not None else "-",
            str(r.mutated_status) if r.mutated_status is not None else "-",
            status,
            r.message or "",
        )

    console.print(table)
    console.print(f"Failures: {failures}")
    return failures


def print_results_json(results: List[MutationResult], *, pretty: bool = False) -> int:
    data = {
        "summary": {
            "total": len(results),
            "failures": sum(1 for r in results if not r.passed),
            "passes": sum(1 for r in results if r.passed),
        },
        "results": [
            {
                "target": r.target_name,
                "mutation": r.mutation_description,
                "baseline_status": r.baseline_status,
                "mutated_status": r.mutated_status,
                "passed": r.passed,
                "message": r.message,
            }
            for r in results
        ],
    }
    print(json.dumps(data, indent=2 if pretty else None))
    return data["summary"]["failures"]
