# Changelog

All notable changes to Neonize will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Breaking (async):** Replaced deprecated `asyncio.get_event_loop()` and `asyncio.new_event_loop()` with modern `asyncio.get_running_loop()` pattern
- `NewAClient.loop` is now `None` until `connect()` is called (was previously set via `get_event_loop()` in `__init__`)
- `ClientFactory.loop` is now `None` until `run()` is called (was previously set to a separate `new_event_loop()`)
- `event_global_loop` in `events.py` is now lazily initialized via `set_event_loop()` during `connect()` (was previously `asyncio.new_event_loop()` at module level)
- All examples updated to use `asyncio.run()` instead of `loop.run_until_complete()`

### Fixed
- Events never being dispatched in single-client mode because `event_global_loop` was created but never started (`run_forever()` was commented out)
- `DeprecationWarning` on Python 3.10+ and `RuntimeError` on Python 3.12+ caused by `asyncio.get_event_loop()` in non-async context
- Event loop mismatch between single-client (default loop) and event dispatch (`new_event_loop()`)

### Added
- `set_event_loop()` function in `events.py` for lazy event loop initialization
- Comprehensive documentation about event loop handling and migration guide in FAQ
- Comprehensive MkDocs documentation
- Enhanced type hints and documentation strings

## [0.3.12] - 2024-12-06

### Current Version

For the complete changelog, visit the [GitHub Releases](https://github.com/krypton-byte/neonize/releases) page.

## Version History

### Major Releases

- **0.3.x** - Current stable series
- **0.2.x** - Legacy support
- **0.1.x** - Initial releases

## Upgrade Guide

### Upgrading to 0.3.x

No breaking changes from 0.2.x series. Simply upgrade:

```bash
pip install --upgrade neonize
```

## Contributing

See [Contributing Guide](development/contributing.md) for information on how to contribute to Neonize.

## Links

- [GitHub Repository](https://github.com/krypton-byte/neonize)
- [PyPI Package](https://pypi.org/project/neonize/)
- [Documentation](https://krypton-byte.github.io/neonize)
