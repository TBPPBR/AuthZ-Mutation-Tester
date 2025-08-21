from __future__ import annotations

import typer

from .config import load_config
from .reporter import print_results, print_results_json
from .runner import run_all


def main(
    config: str = typer.Argument(..., help="Path to YAML config"),
    json_output: bool = typer.Option(False, "--json", help="Output results as JSON"),
    pretty: bool = typer.Option(False, "--pretty", help="Pretty-print JSON output"),
) -> None:
    cfg = load_config(config)
    results = run_all(cfg)
    if json_output:
        failures = print_results_json(results, pretty=pretty)
    else:
        failures = print_results(results)
    raise typer.Exit(code=1 if failures else 0)


if __name__ == "__main__":
    typer.run(main)
