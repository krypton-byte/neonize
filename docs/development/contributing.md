# Contributing

Thank you for improving Neonize. This page summarizes the workflow; the
authoritative document is
[`CONTRIBUTING.md`](https://github.com/krypton-byte/neonize/blob/master/CONTRIBUTING.md)
in the repository root.

## Branching Model

```text
feature/xxx --> PR --> dev ----------> PR --> master
                       (CI gate)             (CI gate + auto release)
hotfix ---------------^
```

| Branch | Purpose | Releases |
| --- | --- | --- |
| `dev` | Integration branch; all feature PRs land here first | No |
| `master` | Release branch; merges trigger the release pipeline | Yes |

## Commit Conventions

Commits follow [Conventional Commits](https://www.conventionalcommits.org);
the version is computed from them by Python Semantic Release:

| Prefix | Effect |
| --- | --- |
| `feat:` | Minor bump |
| `fix:`, `perf:` | Patch bump |
| `feat!:` / `BREAKING CHANGE:` | Major bump |
| `docs:`, `chore:`, `ci:`, `style:`, `test:`, `refactor:` | No bump |

## Local Development

```bash
git clone git@github.com:krypton-byte/neonize.git
cd neonize
uv sync --dev --group docs

# lint and test
uvx ruff check .
uv run --with pytest python -m pytest tests/ -q
```

Go-side changes live under `goneonize/` and are validated with:

```bash
cd goneonize && go build ./... && go vet ./...
```

## Pull Requests

1. Branch from `dev`.
2. Keep commits conventional.
3. Ensure the CI checks pass locally (lint, Go build/vet, proto drift,
   tests).
4. Open the PR against **dev** with a clear description of behavior change.
