# AuthZ Mutation Tester (Python)

A CLI tool to perform authorization mutation testing against HTTP APIs (authorized environments only).

- Sends a baseline request per target
- Applies configured mutations (headers, method, JSON body)
- Asserts that mutated requests are rejected
- Reports results in a table or JSON

## Quick start

1. Create a virtualenv and install deps:

```bash
python -m venv .venv
# PowerShell
. .venv/Scripts/Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

2. Run sample against httpbin:

```bash
python -m authz_mutator samples/example.yaml
```

JSON output (for CI):
```bash
python -m authz_mutator samples/example.yaml --json --pretty
```

Exit codes:
- 0: all mutations behaved as expected (denied)
- 1: one or more mutations were allowed (potential authz weakness) or there were errors

## Config

See `samples/example.yaml` for a documented example. Mutations supported:
- remove_header: name
- replace_header: name, value
- method: method
- body_replace: path (dot notation), value

## Notes
- Use only with explicit authorization.
- Network errors/timeouts are reported as failures for safety.
