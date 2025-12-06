# Development

Contributing to Neonize development.

## Overview

This section covers everything you need to know about contributing to Neonize, building from source, and testing.

## Quick Links

- [Contributing Guidelines](contributing.md) - How to contribute
- [Building from Source](building.md) - Build Neonize locally
- [Testing](testing.md) - Run tests and ensure quality

## Development Setup

### Clone the Repository

```bash
git clone https://github.com/krypton-byte/neonize.git
cd neonize
```

### Install Dependencies

Using uv (recommended):

```bash
uv sync --all-extras
```

Using pip:

```bash
pip install -e ".[dev,docs]"
```

### Verify Installation

```bash
python -c "import neonize; print(neonize.__version__)"
```

## Development Workflow

1. Create a feature branch
2. Make your changes
3. Run tests
4. Update documentation
5. Submit a pull request

## Code Style

We follow PEP 8 and use:

- **Ruff** for linting and formatting
- **mypy** for type checking
- **pytest** for testing

### Format Code

```bash
ruff format .
```

### Check Code

```bash
ruff check .
```

## Testing

Run tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=neonize
```

## Documentation

Build documentation locally:

```bash
task docs-serve
```

Then visit http://127.0.0.1:8000

## Need Help?

- Join [GitHub Discussions](https://github.com/krypton-byte/neonize/discussions)
- Open an [Issue](https://github.com/krypton-byte/neonize/issues)
- Read the [Contributing Guide](contributing.md)
