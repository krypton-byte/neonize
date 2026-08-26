# Building from Source

Build the Go core and the Python package yourself. Required when developing
`goneonize/`, or when no wheel exists for your platform.

## Toolchain

| Tool | Version | Purpose |
| --- | --- | --- |
| Go | 1.25+ | Compile the goneonize shared library |
| C compiler | gcc / clang / zig cc | CGO |
| protoc | 34.x | Regenerate protobuf bindings |
| protoc-gen-go | v1.36.12 | Go protobuf codegen |
| uv | latest | Python dependency management |

## Steps

### 1. Sync Python dependencies

```bash
uv sync --dev
```

### 2. Build the shared library

```bash
export CGO_ENABLED=1
uv run task build goneonize     # produces neonize/neonize-<os>-<arch>.so
```

Cross-compilation works by exporting `GOOS`, `GOARCH` and a suitable `CC`
before the task — the same pattern the release pipeline uses.

### 3. (Optional) Regenerate protocol definitions

Only needed when `goneonize/defproto/*.proto` changed:

```bash
export PATH="$HOME/go/bin:$PATH"
uv run task build proto
git diff --exit-code   # CI enforces that committed artifacts match
```

### 4. Verify the binder loads

```python
import ctypes, neonize.utils.platform as p
lib = ctypes.CDLL(f"neonize/{p.generated_name()}")
print(lib.GetVersion())
```

The printed version must equal `neonize.__version__`; the binder refuses to
load otherwise.

### 5. Build a wheel

```bash
uv build --wheel                 # plain wheel without the native binary
uv run task repack               # bundles the built .so into the wheel
```

`repack` reads `GOOS`/`GOARCH` from the environment to produce the correct
platform tag (for example `neonize-0.4.3-py310-none-manylinux2014_x86_64.whl`)
and embeds the matching shared library inside the wheel.

## Version Synchronization

Three files carry the version and must agree:

| File | Variable |
| --- | --- |
| `neonize/__init__.py` | `__version__` |
| `neonize/download.py` | `__GONEONIZE_VERSION__` |
| `goneonize/version.go` | `version := "..."` |

Set them together with:

```bash
uv run task version             # interactive version setter
```

Under normal releases Python Semantic Release rewrites all three
automatically.
