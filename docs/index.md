# Neonize

<img src="assets/mascot.png" alt="Neonize" style="max-width: 320px" />

Neonize is a Python library for WhatsApp automation. A native Go core built on
[whatsmeow](https://github.com/tulir/whatsmeow) is compiled into a shared
library and exposed to Python through a zero-copy FFI layer, combining
Go-grade protocol reliability with Python's expressiveness.

<div class="tx-feature-grid" markdown>

<div class="tx-feature" markdown>

### :material-language-python: Native Python API

A fully typed, idiomatic Python surface. Every method is documented with
parameters, return types and raised exceptions.

</div>

<div class="tx-feature" markdown>

### :material-lightning-bolt: Go Core Performance

The WhatsApp multidevice protocol is implemented in Go (whatsmeow) and called
directly through ctypes — no subprocesses, no bridges over HTTP.

</div>

<div class="tx-feature" markdown>

### :material-sync: Sync and Async

Two mirrored clients with identical APIs: `NewClient` for synchronous code and
`NewAClient` for asyncio applications. Switch between them without relearning
anything.

</div>

<div class="tx-feature" markdown>

### :material-database: Persistent Sessions

Sessions are stored in SQLite automatically. Pair once with a QR code or a
phone-number link code and reconnect forever after.

</div>

</div>

## Minimal Example

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

## Where to Go Next

| Goal | Page |
| --- | --- |
| Install the library and its prerequisites | [Installation](getting-started/installation.md) |
| Build your first bot | [Quick Start](getting-started/quickstart.md) |
| Link a device via QR or phone number | [Authentication](getting-started/authentication.md) |
| Understand how Neonize works internally | [Architecture](core-concepts/architecture.md) |
| Browse every available method | [API Reference](api-reference/index.md) |

## Platform Support

| Platform | Architectures | Wheel Tag |
| --- | --- | --- |
| Linux | x86_64, arm64, s390x, riscv64 (library only) | `manylinux2014_*` |
| macOS | x86_64, arm64 | `macosx_*` |
| Windows | x86_64, arm64, x86 | `win_*` |
| Android (Termux) | arm64, arm, x86_64, x86 | `linux_*` |

Python 3.10 or newer is required.
