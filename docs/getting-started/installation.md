# Installation

This guide will walk you through the process of installing Neonize on your system.

## System Requirements

### Python Version

Neonize requires Python 3.10 or higher. You can check your Python version by running:

```bash
python --version
```

If you need to upgrade Python, visit [python.org](https://www.python.org/downloads/).

## Installation Methods

### Using pip (Recommended)

The simplest way to install Neonize is using pip:

```bash
pip install neonize
```

### Using uv

If you're using the modern [uv](https://github.com/astral-sh/uv) package manager:

```bash
uv add neonize
```

### Using Poetry

For projects managed with Poetry:

```bash
poetry add neonize
```

### Development Installation

To install Neonize with development dependencies:

```bash
# Clone the repository
git clone https://github.com/krypton-byte/neonize.git
cd neonize

# Install with development dependencies
pip install -e ".[dev]"
```

## Verifying Installation

After installation, verify that Neonize is correctly installed:

```python
import neonize
print(neonize.__version__)
```

This should print the installed version of Neonize without any errors.

## Optional Dependencies

### FFmpeg (For Media Processing)

Neonize uses FFmpeg for video and audio processing. Install it based on your operating system:

=== "Ubuntu/Debian"
    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```

=== "macOS"
    ```bash
    brew install ffmpeg
    ```

=== "Windows"
    Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### Database Drivers

#### PostgreSQL Support

If you plan to use PostgreSQL as your database:

```bash
pip install psycopg2-binary
```

Or for production environments:

```bash
pip install psycopg2
```

## Platform-Specific Notes

### Linux

On Linux systems, you may need to install additional system libraries:

```bash
# Ubuntu/Debian
sudo apt install libmagic1

# Fedora/RHEL
sudo dnf install file-libs
```

### Windows

On Windows, Neonize automatically installs `python-magic-bin` which includes the necessary libraries.

### macOS

On macOS, you may need to install libmagic:

```bash
brew install libmagic
```

## Troubleshooting

### Common Installation Issues

#### Issue: `ModuleNotFoundError: No module named 'neonize'`

**Solution**: Ensure you've activated the correct Python environment and that the installation completed successfully.

```bash
pip list | grep neonize
```

#### Issue: FFmpeg not found

**Solution**: Make sure FFmpeg is installed and available in your system PATH.

```bash
ffmpeg -version
```

#### Issue: Permission denied during installation

**Solution**: Use a virtual environment or install with the `--user` flag:

```bash
pip install --user neonize
```

### Getting Help

If you encounter issues not covered here:

1. Check the [FAQ](../faq.md) section
2. Search [GitHub Issues](https://github.com/krypton-byte/neonize/issues)
3. Open a new issue with detailed information about your problem

## Next Steps

Now that you have Neonize installed, proceed to:

- [Quick Start Guide](quickstart.md) - Create your first bot
- [Authentication](authentication.md) - Learn about WhatsApp authentication
- [User Guide](../user-guide/index.md) - Explore Neonize features

!!! success "Installation Complete"
    You're now ready to build amazing WhatsApp bots with Neonize! 🎉
