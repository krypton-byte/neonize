# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added

- Zensical-powered documentation site with version selector (mike), mkdocstrings API reference, and embedded runnable examples.
- Continuous integration gate for pull requests: ruff lint, Go build/vet, proto drift check, pytest, and FFI smoke test.
- Branching model documented in CONTRIBUTING.md: feature branches target `dev`, merges to `master` trigger the release pipeline.

### Changed

- Migrated versioning from bump-my-version to Python Semantic Release (tag-driven, conventional commits).
- Release pipeline redesigned: PSR computes version, paths-filter detects goneonize changes, prebuilt binaries reused when unchanged.
- Pinned ruff to a deterministic rule set (`E4`, `E7`, `E9`, `F`, `I`) to prevent CI drift across versions.
- Weekly dependency/proto update workflow now targets `dev` instead of `master`.

### Fixed

- Bootstrap tag resolution in release workflow uses GitHub Releases API to avoid downloading from asset-less tags.
- Removed stale references to bump-my-version, tools/flow.py, and tools/docs.py.

## [0.4.3.post0] - 2025-07-01

### Added

- `RejectCall` binding: decline incoming WhatsApp calls from Python.
- `JoinedGroup` event now carries `Sender` and `SenderPN` fields (who added the bot).
- `new_device` flag on `NewClient` for pairing a fresh device even when the database holds other sessions.
- Configurable bot node injection via `NEONIZE_BOT_SCOPE` environment variable.

### Fixed

- `JoinedGroup.Type` was incorrectly populated with the `Reason` value.
- `GetVersion` alignment with released version.

### Changed

- Updated whatsmeow and Go dependencies.

## [0.4.2.post0] - 2025-05-15

### Fixed

- Release workflow: restored `uv run task build proto` in cross-compilation job steps.

## [0.4.1.post0] - 2025-04-20

### Fixed

- Thread handling and stop mechanism for Neonize connections.

## [0.4.0.post0] - 2025-03-10

### Added

- Proxy address support: `set_proxy_address` and `connect_with_proxy` methods.
- Interactive message builders (`neonize.ext.interactive_message`): buttons, lists, carousels.

### Changed

- Major whatsmeow update with protobuf v6 compatibility.

## [0.3.18.post0] - 2025-01-15

### Fixed

- Async connect task cancellation: stop the Go side properly.
- Goneonize binary download retry limit instead of infinite loop.
- Download timeout for goneonize binary.
- Events with no registered handler no longer raise `KeyError`.
- C strings returned across the Go/Python FFI boundary are now freed properly.

## [0.3.17.post0] - 2024-12-20

### Added

- New WhatsApp protocol fields via updated protobuf definitions.

## [0.3.16.post0] - 2024-11-10

### Fixed

- Protobuf 6 compatibility: regenerated with protoc 30.2.

## [0.3.15.post0] - 2024-10-05

### Fixed

- Critical bugs, memory leaks, and Go-Python FFI boundary optimizations.
- Buffer pooling and Bytes struct usage.

## [0.3.14.post0] - 2024-09-01

### Added

- Auto-compile and versioning pipeline.

## [0.3.13.post0] - 2024-08-15

### Added

- Button support for WhatsApp messages.

<!-- version list -->

## v0.4.4 (2026-08-26)

### Bug Fixes

- Correct PSR flags in release workflow (--noop does not exist)
  ([`0ffc642`](https://github.com/krypton-byte/neonize/commit/0ffc642cbbafd94c7da41e3a09f21d7e261e8bb2))

- Populate CHANGELOG.md with missing entries from recent releases
  ([`a064ed5`](https://github.com/krypton-byte/neonize/commit/a064ed55477a719f9e523f8d909c2cab283f265d))

- Resolve go vet errors, ruff format drift and PSR action bug
  ([`77c76bb`](https://github.com/krypton-byte/neonize/commit/77c76bbbc42eaaea6d0cacb23ab1bc6479bf4956))
