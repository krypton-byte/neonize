# Neonize Documentation

This directory contains the source files for Neonize documentation built with MkDocs Material.

## Quick Start

### Install Dependencies

```bash
pip install -e ".[docs]"
```

Or with uv:

```bash
uv sync --group docs
```

### Serve Documentation Locally

```bash
task docs-serve
```

Or manually:

```bash
mkdocs serve
```

Visit http://127.0.0.1:8000

### Build Documentation

```bash
task docs-build
```

Or manually:

```bash
mkdocs build
```

Output will be in `site/` directory.

## Documentation Structure

```
docs/
├── index.md                    # Home page
├── getting-started/            # Getting started guides
│   ├── index.md
│   ├── installation.md
│   ├── quickstart.md
│   └── authentication.md
├── user-guide/                 # User guides
│   ├── index.md
│   ├── client-configuration.md
│   ├── sending-messages.md
│   ├── receiving-messages.md
│   ├── event-system.md
│   ├── media-handling.md
│   ├── group-management.md
│   ├── contact-management.md
│   ├── newsletter.md
│   └── advanced-features.md
├── async/                      # Async client guides
│   ├── index.md
│   ├── quickstart.md
│   ├── events.md
│   └── best-practices.md
├── api-reference/              # API documentation
│   ├── index.md
│   ├── client.md
│   ├── async-client.md
│   ├── events.md
│   ├── types.md
│   ├── utils.md
│   └── exceptions.md
├── examples/                   # Code examples
│   ├── index.md
│   ├── basic-bot.md
│   ├── async-bot.md
│   ├── multi-session.md
│   ├── media-bot.md
│   └── group-bot.md
├── development/                # Development guides
│   ├── index.md
│   ├── contributing.md
│   ├── building.md
│   └── testing.md
├── faq.md                      # FAQ
└── changelog.md                # Changelog
```

## Writing Documentation

### Markdown

Documentation is written in Markdown with extensions:

- **Admonitions**: `!!! note`, `!!! warning`, etc.
- **Code blocks**: Triple backticks with language
- **Tables**: Standard Markdown tables
- **Links**: `[text](url)`

### Code Examples

Use fenced code blocks with language identifier:

````markdown
```python
from neonize.client import NewClient

client = NewClient("my_bot")
```
````

### Admonitions

```markdown
!!! tip "Pro Tip"
    This is a helpful tip

!!! warning "Important"
    Pay attention to this

!!! info "Information"
    Additional context

!!! example "Example"
    Code example
```

### API Documentation

Use mkdocstrings for API docs:

```markdown
::: neonize.client.NewClient
    options:
      show_root_heading: true
      show_source: true
```

## Taskipy Commands

Available documentation tasks:

```bash
# Serve with live reload
task docs-serve

# Build documentation
task docs-build

# Deploy to GitHub Pages
task docs-deploy

# Clean built files
task docs-clean

# Build with strict validation
task docs-validate
```

## Deployment

### GitHub Pages

Deploy to GitHub Pages:

```bash
task docs-deploy
```

This builds and pushes to the `gh-pages` branch.

### Manual Deployment

```bash
# Build
mkdocs build

# Upload site/ directory to your hosting
```

## Configuration

Documentation configuration is in `mkdocs.yml` at the repository root.

### Theme

We use Material for MkDocs with:

- Light/dark mode toggle
- Navigation tabs
- Search functionality
- Code syntax highlighting
- Mobile responsive design

### Plugins

- `search` - Full-text search
- `mkdocstrings` - API documentation from docstrings
- `autorefs` - Automatic cross-references

## Contributing

When contributing documentation:

1. Follow existing structure and style
2. Test locally with `task docs-serve`
3. Validate with `task docs-validate`
4. Check for broken links
5. Ensure code examples work

## Style Guide

### Headers

- Use ATX-style headers (`#` not underlines)
- One H1 per page (page title)
- Hierarchical structure (H2 → H3 → H4)

### Code

- Always specify language for code blocks
- Keep examples concise and focused
- Show both input and expected output when relevant

### Links

- Use relative links for internal pages
- Use absolute links for external resources
- Ensure links are descriptive

### Writing Style

- Professional but approachable tone
- Active voice preferred
- Short sentences and paragraphs
- Use examples liberally

## License

Documentation is licensed under Apache License 2.0, same as the code.
