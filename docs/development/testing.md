# Testing

## Python Tests

```bash
uv run --with pytest python -m pytest tests/ -q
```

The suite includes a binder test that verifies the FFI contract. It runs in
two modes:

| Mode | Trigger | Behavior |
| --- | --- | --- |
| Metadata mode | `SPHINX=1` (default in CI docs contexts) | Validates binder declarations without loading the library |
| Full mode | built `.so` present | Loads the native core and checks symbols |

## Building the Library for Local Tests

```bash
export CGO_ENABLED=1
uv run task build goneonize
```

Then a full smoke check:

```python
from neonize.client import NewClient
assert hasattr(NewClient, "reject_call")
```

## Go-Side Checks

```bash
cd goneonize
go build ./...
go vet ./...
```

`go vet` findings are advisory; `go build` must always pass.

## Proto Drift Check

CI regenerates protobuf artifacts with pinned toolchain versions (protoc
34.x, protoc-gen-go v1.36.12) and fails if committed files differ:

```bash
uv run task build proto
git diff --exit-code
```

Run this before committing changes to any `.proto` or generated file.

## Continuous Integration

Every pull request runs: ruff lint, Go build/vet, proto drift check,
pytest, and an FFI smoke test — see `.github/workflows/ci.yml`.
