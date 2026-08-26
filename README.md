<div align="center">
<img src="assets/mascot.png" width="20%" alt="Neonize">

# Neonize

### WhatsApp Automation for Python

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://golang.org)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/github/v/release/krypton-byte/neonize?style=for-the-badge)](https://github.com/krypton-byte/neonize/releases)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://whatsapp.com/)

A Python library for WhatsApp automation. A native Go core built on
[whatsmeow](https://github.com/tulir/whatsmeow) is compiled into a shared
library and exposed to Python through a zero-copy FFI layer.

[Getting Started](#getting-started) | [Features](#features) | [Examples](#examples) | [Documentation](https://neonize.readthedocs.io/) | [Contributing](#contributing)

</div>

---

## Why Neonize?

| | |
|---|---|
| **Go core performance** | The WhatsApp multidevice protocol runs in Go, called directly through ctypes. No subprocesses, no HTTP bridges. |
| **Python native** | Fully typed, idiomatic API. Sync and async clients with identical surfaces. |
| **Persistent sessions** | SQLite or PostgreSQL. Pair once, reconnect forever. |
| **Enterprise ready** | Structured error hierarchy, FFmpeg diagnostics, robust FFI with retry logic. |

---

## Features

**Messaging**
- Send and receive text, images, videos, documents, audio, voice notes, stickers
- Message replies, reactions, polls, interactive buttons and lists
- Receipt and presence tracking

**Groups and Channels**
- Create, update, and manage groups (name, description, photo, participants)
- Newsletter/channel operations: fetch messages, update profile, send media

**Contacts and Presence**
- Profile picture retrieval, push name updates
- Typing and recording indicators
- Contact sync and blocklist management

**Architecture**
- Sync (`NewClient`) and async (`NewAClient`) with identical APIs
- Multi-session support via `ClientFactory`
- Event-driven with 37+ typed event classes
- QR code and phone-number pairing

---

## Getting Started

### Prerequisites

- Python 3.10 or newer
- FFmpeg (required for media operations: stickers, audio, video, thumbnails)

### Installation

```bash
pip install neonize
```

### Quick Start

```python
from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv

client = NewClient("session.db")

@client.event(ConnectedEv)
def on_connected(client: NewClient, _: ConnectedEv) -> None:
    print("Connected")

@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv) -> None:
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    if text == "ping":
        client.reply_message("pong", message)

client.connect()
```

### Async Quick Start

```python
import asyncio
from neonize.aioze.client import NewAClient
from neonize.aioze.events import ConnectedEv, MessageEv

client = NewAClient("async_session.db")

@client.event(ConnectedEv)
async def on_connected(client: NewAClient, _: ConnectedEv) -> None:
    print("Connected")

@client.event(MessageEv)
async def on_message(client: NewAClient, message: MessageEv) -> None:
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    if text == "ping":
        await client.reply_message("pong", message)

async def main():
    await client.connect()
    await client.idle()

asyncio.run(main())
```

---

## Examples

### Sending Media

```python
from neonize.utils.jid import build_jid

jid = build_jid("1234567890", "s.whatsapp.net")

# Text
client.send_message(jid, "Hello from Neonize")

# Image with caption
with open("photo.jpg", "rb") as f:
    msg = client.build_image_message(f.read(), caption="Photo", mime_type="image/jpeg")
    client.send_message(jid, message=msg)

# Document
with open("report.pdf", "rb") as f:
    msg = client.build_document_message(f.read(), filename="report.pdf", mime_type="application/pdf")
    client.send_message(jid, message=msg)
```

### Handling Incoming Messages

```python
from neonize.events import MessageEv, ReceiptEv, PresenceEv
from neonize.utils.message import extract_text

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv) -> None:
    text = extract_text(event.Message)
    sender = event.Info.MessageSource.Sender

    if text == "help":
        client.reply_message("Available commands: help, time", event)

@client.event(ReceiptEv)
def on_receipt(client: NewClient, event: ReceiptEv) -> None:
    print(f"Receipt: {event.Receipt.Type} for {event.MessageIDs}")

@client.event(PresenceEv)
def on_presence(client: NewClient, event: PresenceEv) -> None:
    print(f"{event.MessageSource.Sender} is {event.Presence}")
```

### Group Management

```python
from neonize.utils.jid import build_jid

# Create group
participants = [build_jid("1234567890"), build_jid("0987654321")]
info = client.create_group("Project Team", participants)
print(f"Group created: {info.JID}")

# Update settings
client.set_group_name(info.JID, "New Name")
client.set_group_description(info.JID, "Updated description")

# Manage participants
client.update_group_participants(info.JID, [build_jid("5555555555")], "add")
```

### Multi-Session (Async)

```python
import asyncio
from neonize.aioze.client import ClientFactory, NewAClient
from neonize.aioze.events import MessageEv, ConnectedEv

factory = ClientFactory("multisession.db")

# Load existing sessions
for device in factory.get_all_devices():
    factory.new_client(device.JID)

# Pair a new account
factory.new_client(uuid="second-account", new_device=True)

@factory.event(ConnectedEv)
async def on_connected(client: NewAClient, event: ConnectedEv) -> None:
    print("Client connected")

@factory.event(MessageEv)
async def on_message(client: NewAClient, event: MessageEv) -> None:
    if event.Message.conversation == "ping":
        await client.reply_message("pong", event)

async def main():
    await factory.run()
    await factory.idle_all()

asyncio.run(main())
```

### Integration with FastAPI

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from neonize.aioze.client import NewAClient
from neonize.aioze.events import MessageEv
from neonize.utils.jid import build_jid

client = NewAClient("fastapi_bot")

@client.event(MessageEv)
async def on_message(client: NewAClient, event: MessageEv) -> None:
    if event.Message.conversation == "/status":
        await client.reply_message("API is running", event)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.connect()
    yield
    await client.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/send")
async def send(phone: str, message: str):
    await client.send_message(build_jid(phone), message)
    return {"status": "sent"}
```

---

## Database Configuration

Neonize stores session data in a database. The default is SQLite, which works
well for development and single-instance deployments.

```python
# SQLite (default)
client = NewClient("bot", database="./session.db")

# PostgreSQL (recommended for production)
client = NewClient("bot", database="postgres://user:pass@localhost:5432/neonize")

# Connection pooling
client = NewClient("bot", database="postgres://user:pass@localhost/neonize?pool_min_conns=5&pool_max_conns=20")

# In-memory (testing only)
client = NewClient("bot", database=":memory:")
```

---

## Project Structure

```
neonize/
├── examples/               # Runnable example bots
│   ├── basic.py
│   ├── async_basic.py
│   ├── multisession.py
│   ├── multisession_async.py
│   └── paircode.py
├── goneonize/              # Go shared library (FFI core)
│   ├── main.go
│   ├── defproto/           # Generated protobuf definitions
│   └── utils/              # Go encoder helpers
├── neonize/                # Python package
│   ├── __init__.py
│   ├── client.py           # Sync client (NewClient)
│   ├── aioze/              # Async client (NewAClient)
│   ├── events.py           # Event types and dispatcher
│   ├── exc.py              # Exception hierarchy
│   ├── ext/                # Extensions (interactive messages)
│   ├── proto/              # Python protobuf bindings
│   └── utils/              # Helpers (JID, media, FFmpeg, etc.)
├── docs/                   # Zensical documentation source
├── tools/                  # Build, release, and dev scripts
└── pyproject.toml          # Project metadata and dependencies
```

---

## Contributing

We welcome contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
branching model, conventional-commit standards, and release process.

```bash
# Clone and setup
git clone https://github.com/krypton-byte/neonize.git
cd neonize
uv sync --dev

# Build the Go shared library
CGO_ENABLED=1 uv run task build goneonize

# Run tests
uv run --with pytest python -m pytest

# Lint
uv run ruff check .
uv run ruff format --check .
```

**Workflow:** feature branches target `dev`, merges to `master` trigger the
automated release pipeline.

---

## Documentation

Full documentation is available at **[neonize.readthedocs.io](https://neonize.readthedocs.io/)**

- [Installation](https://neonize.readthedocs.io/getting-started/installation/)
- [Quick Start](https://neonize.readthedocs.io/getting-started/quickstart/)
- [Authentication](https://neonize.readthedocs.io/getting-started/authentication/)
- [Architecture](https://neonize.readthedocs.io/core-concepts/architecture/)
- [API Reference](https://neonize.readthedocs.io/api-reference/)

---

## Related Projects

| Project | Description |
|---|---|
| [Thundra](https://github.com/krypton-byte/thundra) | High-level bot framework built on Neonize |
| [Tryx](https://github.com/krypton-byte/tryx) | Rust-powered Python SDK for WhatsApp automation |
| [Neonize Dart](https://github.com/krypton-byte/neonize-dart) | Dart/Flutter wrapper for Neonize |
| [Whatsmeow](https://github.com/tulir/whatsmeow) | Go WhatsApp Web API library that powers Neonize |

---

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

---

<div align="center">

**Built by [krypton-byte](https://github.com/krypton-byte) and contributors**

</div>
