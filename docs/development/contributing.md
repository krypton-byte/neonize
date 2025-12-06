# Contributing to Neonize

Thank you for your interest in contributing to Neonize! This guide will help you get started.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug is already reported in [Issues](https://github.com/krypton-byte/neonize/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, Neonize version)
   - Code samples if applicable

### Suggesting Features

1. Check [Discussions](https://github.com/krypton-byte/neonize/discussions) for similar ideas
2. Create a new discussion explaining:
   - The problem you're trying to solve
   - Your proposed solution
   - Why this would be useful

### Contributing Code

#### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/neonize.git
cd neonize
```

#### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

#### 3. Make Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation

#### 4. Test Your Changes

```bash
# Run tests
pytest

# Check code style
ruff check .
ruff format .

# Type checking
mypy neonize
```

#### 5. Commit

Write clear commit messages:

```bash
git commit -m "feat: add support for new feature"
git commit -m "fix: resolve issue with message handling"
git commit -m "docs: update installation guide"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance

#### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots if applicable

## Development Guidelines

### Code Style

We use:
- **Ruff** for linting and formatting
- **Type hints** for all functions
- **Docstrings** in Sphinx style

Example:

```python
def send_message(
    self,
    to: JID,
    message: str,
    link_preview: bool = False
) -> SendResponse:
    """Send a text message to the specified JID.

    :param to: The recipient's JID
    :type to: JID
    :param message: The message text to send
    :type message: str
    :param link_preview: Enable link previews, defaults to False
    :type link_preview: bool, optional
    :return: Response from the server
    :rtype: SendResponse
    """
    # Implementation
```

### Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for good code coverage

### Documentation

- Update docstrings
- Update relevant markdown files
- Add examples for new features

## Project Structure

```
neonize/
├── neonize/           # Main package
│   ├── client.py      # Sync client
│   ├── events.py      # Event system
│   ├── aioze/         # Async client
│   └── utils/         # Utilities
├── goneonize/         # Go bindings
├── examples/          # Example scripts
├── docs/              # Documentation
├── tests/             # Test files
└── tools/             # Build tools
```

## Communication

- **Bugs & Features**: [GitHub Issues](https://github.com/krypton-byte/neonize/issues)
- **Questions & Discussions**: [GitHub Discussions](https://github.com/krypton-byte/neonize/discussions)
- **Security Issues**: Email maintainers privately

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Recognition

Contributors will be recognized in:
- README.md
- Release notes
- Contributors page

## Questions?

Feel free to ask questions in [Discussions](https://github.com/krypton-byte/neonize/discussions) or open an issue.

Thank you for contributing to Neonize! 🎉
