# Building from Source

Learn how to build Neonize from source code.

## Prerequisites

### Required Tools

- **Python 3.10+**
- **Go 1.19+** (for building goneonize)
- **Git**
- **C Compiler** (gcc/clang)

### Optional Tools

- **uv** - Modern Python package manager (recommended)
- **Docker** - For containerized builds

## Quick Build

### 1. Clone Repository

```bash
git clone https://github.com/krypton-byte/neonize.git
cd neonize
```

### 2. Install Dependencies

Using uv:

```bash
uv sync --all-extras
```

Using pip:

```bash
pip install -e ".[dev]"
```

### 3. Build goneonize

```bash
task build
```

Or manually:

```bash
cd goneonize
go build -buildmode=c-shared -o neonize-linux-amd64.so
```

## Platform-Specific Builds

### Linux

```bash
cd goneonize
CGO_ENABLED=1 GOOS=linux GOARCH=amd64 \
  go build -buildmode=c-shared -o neonize-linux-amd64.so
```

### macOS

```bash
cd goneonize
CGO_ENABLED=1 GOOS=darwin GOARCH=amd64 \
  go build -buildmode=c-shared -o neonize-darwin-amd64.dylib
```

For Apple Silicon:

```bash
CGO_ENABLED=1 GOOS=darwin GOARCH=arm64 \
  go build -buildmode=c-shared -o neonize-darwin-arm64.dylib
```

### Windows

```bash
cd goneonize
set CGO_ENABLED=1
set GOOS=windows
set GOARCH=amd64
go build -buildmode=c-shared -o neonize-windows-amd64.dll
```

## Building Documentation

### Install Documentation Dependencies

```bash
pip install -e ".[docs]"
```

### Build HTML Documentation

```bash
task docs-build
```

Or manually:

```bash
mkdocs build
```

### Serve Documentation Locally

```bash
task docs-serve
```

Visit http://127.0.0.1:8000

## Building Distribution Packages

### Build Wheel

```bash
pip install build
python -m build
```

This creates:
- `dist/neonize-*.whl` - Wheel package
- `dist/neonize-*.tar.gz` - Source distribution

### Install from Wheel

```bash
pip install dist/neonize-*.whl
```

## Development Build

For active development:

```bash
# Editable install
pip install -e .

# With all extras
pip install -e ".[dev,docs]"
```

## Docker Build

### Build Image

```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    golang-go \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone and build
WORKDIR /app
COPY . .
RUN pip install -e .

CMD ["python"]
```

Build:

```bash
docker build -t neonize .
```

## Cross-Compilation

### Using Docker for Cross-Platform Builds

```bash
# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t neonize:latest .
```

## Troubleshooting

### Go Build Errors

**Issue**: `go: cannot find main module`

**Solution**:
```bash
cd goneonize
go mod tidy
```

### C Compiler Not Found

**Issue**: `gcc: command not found`

**Solution**:

=== "Ubuntu/Debian"
    ```bash
    sudo apt install build-essential
    ```

=== "macOS"
    ```bash
    xcode-select --install
    ```

=== "Windows"
    Install MinGW or Visual Studio Build Tools

### Python Extension Build Fails

**Issue**: Missing Python headers

**Solution**:

=== "Ubuntu/Debian"
    ```bash
    sudo apt install python3-dev
    ```

=== "Fedora"
    ```bash
    sudo dnf install python3-devel
    ```

## Verification

After building, verify the installation:

```python
import neonize
print(neonize.__version__)

# Test basic functionality
from neonize.client import NewClient
client = NewClient("test")
print("✅ Build successful!")
```

## Build Optimization

### Optimized Go Build

```bash
go build -ldflags="-s -w" -buildmode=c-shared
```

Flags:
- `-s` - Strip symbol table
- `-w` - Strip DWARF debugging info

### Python Build Options

```bash
# Build with specific Python version
python3.11 -m build

# Build only wheel
python -m build --wheel
```

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - uses: actions/setup-go@v4
        with:
          go-version: '1.20'
      - name: Build
        run: |
          pip install build
          python -m build
```

## Next Steps

- [Testing](testing.md) - Run tests
- [Contributing](contributing.md) - Contribute code
- [Development Guide](index.md) - Development overview
