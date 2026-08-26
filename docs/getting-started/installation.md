# Installation

## Requirements

- Python 3.10 or newer
- FFmpeg (required for media conversion: stickers, audio, video, thumbnails)

## Install from PyPI

=== "pip"

    ```bash
    pip install neonize
    ```

=== "uv"

    ```bash
    uv add neonize
    ```

The PyPI wheel ships the compiled Go core (`.so` / `.dll` / `.dylib`) inside
the package. There is nothing else to download at runtime — the native
library is loaded directly from the wheel on import.

!!! note "Platform detection"
    Neonize selects the correct binary for your platform at import time via
    `neonize.utils.platform`. If no matching binary exists, an
    `UnsupportedPlatform` error is raised with the exact filename it looked
    for.

## Install FFmpeg

Sticker and audio/video handling shell out to FFmpeg for transcoding.

=== "Debian / Ubuntu"

    ```bash
    sudo apt install ffmpeg
    ```

=== "Fedora"

    ```bash
    sudo dnf install ffmpeg
    ```

=== "macOS (Homebrew)"

    ```bash
    brew install ffmpeg
    ```

=== "Windows (winget)"

    ```powershell
    winget install Gyan.FFmpeg
    ```

Text-only bots that never send or convert media work without FFmpeg.

## Verify the Installation

```python
import neonize

print(neonize.__version__)
from neonize.client import NewClient  # noqa: E402  (loads the native core)
```

If this prints a version and imports cleanly, both the Python layer and the
Go core are functional.

## Installing from Source

Building from source requires Go 1.25+, protoc, and a C compiler. See
[Building from Source](../development/building.md) for the full toolchain.
