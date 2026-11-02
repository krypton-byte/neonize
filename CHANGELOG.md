# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added

- `extract_text()` exported as a public top-level function (`from neonize import extract_text`) for convenient text extraction from incoming messages.
- `check_ffmpeg_available()` runs at connect time and logs a clear warning if FFmpeg is missing, instead of crashing later during media operations.
- Zensical-powered documentation site with version selector (mike), mkdocstrings API reference, and embedded runnable examples.
- Continuous integration gate for pull requests: ruff lint, Go build/vet, proto drift check, pytest, and FFI smoke test.
- Branching model documented in CONTRIBUTING.md: feature branches target `dev`, merges to `master` trigger the release pipeline.

### Changed

- **BREAKING:** `reject_call()`, `leave_group()`, `set_group_name()`, and `send_chat_presence()` no longer return error strings on failure -- they now **raise** their corresponding exception. Update any code that captured the return value:

  ```python
  # Before (0.4.x and earlier)
  result = client.reject_call(call)  # returns str on error
  if result:
      print("error:", result)

  # After
  try:
      client.reject_call(call)  # raises RejectCallError on error
  except RejectCallError as e:
      print("error:", e)
  ```

  Affected exceptions: `RejectCallError`, `LeaveGroupError`, `SetGroupNameError`, `SendPresenceError`.

- **All custom exceptions now inherit from `NeonizeError`** instead of bare `Exception`. Code using `except Exception` will still work, but you can now use the more specific `except NeonizeError` to catch all library errors.
- `send_message()` accepts plain phone-number strings directly: `client.send_message("6281234567890", "hello")` -- no need to call `build_jid()` first for individual chats.
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

## v0.7.0 (2026-11-02)

### Bug Fixes

- Decrypt secret-encrypted WhatsApp message edits
  ([`4f8ef91`](https://github.com/krypton-byte/neonize/commit/4f8ef911c94ad8082bfef35bced8cdd873df9aca))

- Fail closed on unsupported SPR group send transport
  ([`8afebf4`](https://github.com/krypton-byte/neonize/commit/8afebf45a54ac9a94e0925044ddb9fe5fd3b3c76))

- Handle LID senders in revoke and quotes
  ([`ca6b24d`](https://github.com/krypton-byte/neonize/commit/ca6b24d15707a8b2309e8a34ded42e377ed8eb33))

- **ffi**: Correct a few binding declarations
  ([`7439b2f`](https://github.com/krypton-byte/neonize/commit/7439b2f3e322655c434053004efe0fd8fd7b969d))

- **goneonize**: Build with current whatsmeow
  ([`38a0d3a`](https://github.com/krypton-byte/neonize/commit/38a0d3a2296e7df239ed3fbac5b6e8fb4765df59))

- **goneonize**: Don't block forever in FetchMe after Stop
  ([`551ff67`](https://github.com/krypton-byte/neonize/commit/551ff67e0090c8484b91f02d231e83ee3c9b311c))

- **goneonize**: Let Stop end the QR and pair-code login waits
  ([`5eb236e`](https://github.com/krypton-byte/neonize/commit/5eb236e903d6e107de87fd91b835bc3eef60cda4))

- **goneonize**: Stop waiting for QR events once the client is stopped
  ([`ce75a7c`](https://github.com/krypton-byte/neonize/commit/ce75a7c6630a4a6d75d4a2fcaa7ccb204f0e832d))

### Continuous Integration

- Update workflow actions to current majors
  ([`d8dd283`](https://github.com/krypton-byte/neonize/commit/d8dd28301e00a548e0326e9afab01ee60007e075))

### Features

- Add spoiler option for images, videos and albums
  ([`c979b5f`](https://github.com/krypton-byte/neonize/commit/c979b5f59f1b1d7e6526fd62b881a4771e92e96b))

- Decrypt secret-encrypted message edits
  ([`938573d`](https://github.com/krypton-byte/neonize/commit/938573dfcd74fbc952d804b83d8a869fe858d1bc))

- Support emoji and duration in set_status_message
  ([`bb73f7f`](https://github.com/krypton-byte/neonize/commit/bb73f7f07b1c1dc582ad1fa5bf67262c4d9a3df1))

- **sticker**: Expose quality and compression_level
  ([`f445e79`](https://github.com/krypton-byte/neonize/commit/f445e791f0dbb244b1280f6b2274bffac282dbf2))

- **video**: Remux H.264 videos and attach a streaming sidecar
  ([`3f9b51b`](https://github.com/krypton-byte/neonize/commit/3f9b51b269689ff3b67e8e67e562e7c32d216ab4))


## v0.6.1 (2026-11-02)

### Bug Fixes

- **goneonize**: Build with current whatsmeow
  ([`38a0d3a`](https://github.com/krypton-byte/neonize/commit/38a0d3a2296e7df239ed3fbac5b6e8fb4765df59))

### Continuous Integration

- Update workflow actions to current majors
  ([`d8dd283`](https://github.com/krypton-byte/neonize/commit/d8dd28301e00a548e0326e9afab01ee60007e075))


## v0.6.0 (2026-10-15)

### Documentation

- Switch the README and docs banners to the light/dark artwork
  ([`84bb1b2`](https://github.com/krypton-byte/neonize/commit/84bb1b2f49ea8a3a24673dc680d008dad921b787))

### Features

- Add SPR group send transport
  ([`9e188d1`](https://github.com/krypton-byte/neonize/commit/9e188d19ca6f017f1dc6064b5a338c21194fcead))


## v0.5.2 (2026-09-21)

### Bug Fixes

- **ci**: Checkout repository and publish downloaded wheels in publish job
  ([`3f7c691`](https://github.com/krypton-byte/neonize/commit/3f7c691053a320c1e228bd9eb8e0d39601b15f14))


## v0.5.1 (2026-09-21)

### Bug Fixes

- **ci**: Fix shared library copy path in linux and darwin release jobs
  ([`00d1502`](https://github.com/krypton-byte/neonize/commit/00d1502859d61053acf3163859ee091b961daf28))


## v0.5.0 (2026-09-21)

### Bug Fixes

- **ci**: Harden release workflow against existing tags and non-fast-forward
  ([`3f00f55`](https://github.com/krypton-byte/neonize/commit/3f00f55eeb343ab437d3d30fa9024c11e95b3e90))

- **memory**: FFI memory safety, weakref GC protection, and code cleanup
  ([`6ae24e7`](https://github.com/krypton-byte/neonize/commit/6ae24e7c415191788384f96035b6ca8afb3bebcb))

- **proto**: Regenerate with protoc 34.1 to match CI toolchain
  ([`81160e2`](https://github.com/krypton-byte/neonize/commit/81160e2b1ec9e9538c42568ada52e11af2954cc2))

### Documentation

- Convert text flow diagrams to Mermaid and add Context7 chat widget
  ([`0905e05`](https://github.com/krypton-byte/neonize/commit/0905e05df901e48f0e0cf457e88b02b95e8d20a5))

### Features

- **whatsmeow**: Update whatsmeow, sync protobufs, and fix edge-case panics
  ([`6a12440`](https://github.com/krypton-byte/neonize/commit/6a1244026845d813147a948eba477f65c894b1cd))


## v0.4.7 (2026-08-26)

### Bug Fixes

- **ci**: Prevent release failure when tag already exists
  ([`5275cc1`](https://github.com/krypton-byte/neonize/commit/5275cc1393a025f3a96366b40daa91b0bb0a4562))

### Documentation

- Wrap snippet includes in code fences for example pages
  ([`10f4a81`](https://github.com/krypton-byte/neonize/commit/10f4a81d6ef998b3bbc5579857d4a0e7cf916e3d))


## v0.4.6 (2026-08-26)

### Bug Fixes

- Prevent Go panics in UploadNewsletter and GetNewsletterMessages
  ([`85d4a89`](https://github.com/krypton-byte/neonize/commit/85d4a89faa10625530378ff6b43cf010f9935e38))

- **ci**: Resolve lint-python and proto-sync CI failures
  ([`1982d68`](https://github.com/krypton-byte/neonize/commit/1982d6821551070c39cfad7e335a003cc72d38c3))

### Documentation

- Rewrite README and replace branding assets with mascot
  ([`a29bfae`](https://github.com/krypton-byte/neonize/commit/a29bfae261d089b6ca227564a8fe922cb1f2c483))

- Sync mascot.png from assets/ to docs/assets/
  ([`c112f9b`](https://github.com/krypton-byte/neonize/commit/c112f9bd1f24438b6e84e4e1ea730dd4a7252cf1))

- **logo**: Mascot
  ([`6c9c4be`](https://github.com/krypton-byte/neonize/commit/6c9c4be85b9bda6f10eac91ceb21aaa939f2da0d))


## v0.4.5 (2026-08-26)

### Bug Fixes

- Improve error hierarchy, DX, and documentation for Priority 1 + 2
  ([`222fbb6`](https://github.com/krypton-byte/neonize/commit/222fbb698bd6270ca40b22fa510795ab91edb3fe))


## v0.4.4 (2026-08-26)

### Bug Fixes

- Correct PSR flags in release workflow (--noop does not exist)
  ([`0ffc642`](https://github.com/krypton-byte/neonize/commit/0ffc642cbbafd94c7da41e3a09f21d7e261e8bb2))

- Populate CHANGELOG.md with missing entries from recent releases
  ([`a064ed5`](https://github.com/krypton-byte/neonize/commit/a064ed55477a719f9e523f8d909c2cab283f265d))

- Resolve go vet errors, ruff format drift and PSR action bug
  ([`77c76bb`](https://github.com/krypton-byte/neonize/commit/77c76bbbc42eaaea6d0cacb23ab1bc6479bf4956))
