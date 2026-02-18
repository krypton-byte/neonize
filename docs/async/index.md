# Async Client

Working with Neonize's asynchronous client.

## Overview

The async client (`NewAClient`) provides full async/await support for high-performance applications. Since Python 3.10+, Neonize uses **`asyncio.run()`** as the standard entry point and obtains the event loop via **`asyncio.get_running_loop()`** internally — no manual loop management needed.

## Quick Links

- [Getting Started](quickstart.md) - Start with async client
- [Event Handling](events.md) - Async event handlers
- [Best Practices](best-practices.md) - Async patterns and tips

## Basic Usage

```python
import asyncio
from neonize.aioze.client import NewAClient
from neonize.aioze.events import MessageEv, ConnectedEv

client = NewAClient("async_bot")

@client.event(ConnectedEv)
async def on_connected(client: NewAClient, event: ConnectedEv):
    print("✅ Connected!")

@client.event(MessageEv)
async def on_message(client: NewAClient, event: MessageEv):
    text = event.Message.conversation
    if text == "ping":
        await client.reply_message("pong!", event)

async def main():
    await client.connect()   # captures the running event loop internally
    await client.idle()       # keeps the client alive

asyncio.run(main())          # ← standard entry point
```

## Event Loop Architecture

Neonize receives events from Go callbacks running on separate OS threads.
These callbacks dispatch coroutines to the Python event loop using
`asyncio.run_coroutine_threadsafe()`. For this to work, Neonize needs a
reference to the **running** event loop.

### How It Works

1. **`asyncio.run(main())`** creates and starts an event loop.
2. Inside `main()`, **`await client.connect()`** calls `asyncio.get_running_loop()` and stores a reference.
3. Go callbacks use `run_coroutine_threadsafe(coro, loop)` to schedule your event handlers on that loop.
4. **`await client.idle()`** awaits the connection task, keeping the loop alive.

```
┌─────────────────────────────────┐
│       asyncio.run(main())       │  ← creates the event loop
│  ┌───────────────────────────┐  │
│  │  await client.connect()   │  │  ← stores get_running_loop()
│  │  await client.idle()      │  │  ← keeps loop alive
│  └───────────────────────────┘  │
│         ▲                       │
│         │ run_coroutine_threadsafe()
│  ┌──────┴────────────────────┐  │
│  │  Go callbacks (threads)   │  │  ← events from WhatsApp
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

### Why NOT `get_event_loop()` or `new_event_loop()`?

| Pattern | Problem |
|---------|---------|
| `asyncio.get_event_loop()` | **Deprecated** since Python 3.10. Raises `DeprecationWarning`. On Python 3.12+ it raises `RuntimeError` if no loop is running. |
| `asyncio.new_event_loop()` | Creates an **orphan** loop. Unless you manually call `loop.run_forever()` in a thread, any `run_coroutine_threadsafe()` call targeting it will silently fail — events are never executed. |
| `loop.run_until_complete()` | Works but is the **low-level API**. `asyncio.run()` is the recommended high-level replacement since Python 3.7. |

### Correct Pattern (Python 3.7+)

```python
# ✅ Always use asyncio.run() as the entry point
asyncio.run(main())
```

Inside `main()` (an async function), the event loop is guaranteed to be running.
Neonize's `connect()` captures it automatically — no manual loop passing required.

## Multi-Session (ClientFactory)

```python
import asyncio
from neonize.aioze.client import ClientFactory, NewAClient
from neonize.aioze.events import ConnectedEv, MessageEv

client_factory = ClientFactory("sessions.db")

for device in client_factory.get_all_devices():
    client_factory.new_client(device.JID)

@client_factory.event(ConnectedEv)
async def on_connected(client: NewAClient, event: ConnectedEv):
    print("⚡ Client connected")

@client_factory.event(MessageEv)
async def on_message(client: NewAClient, event: MessageEv):
    if event.Message.conversation == "ping":
        await client.reply_message("pong!", event)

async def main():
    await client_factory.run()       # connects all clients
    await client_factory.idle_all()  # keeps them alive

asyncio.run(main())  # ← single entry point for all sessions
```

## One-Shot Usage

Send a message and exit without keeping the bot alive:

```python
import asyncio
from neonize.aioze.client import NewAClient
from neonize.utils.jid import build_jid

client = NewAClient("db.sqlite3")

async def main():
    await client.connect()
    while not client.connected:
        await asyncio.sleep(0.1)
    await client.send_message(build_jid("1234567890"), "Hello!")
    await client.stop()

asyncio.run(main())
```

## Integration with Async Frameworks

### FastAPI

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from neonize.aioze.client import NewAClient
from neonize.aioze.events import MessageEv
from neonize.utils.jid import build_jid

wa = NewAClient("fastapi_bot")

@wa.event(MessageEv)
async def on_message(client: NewAClient, event: MessageEv):
    if event.Message.conversation == "status":
        await client.reply_message("API is running ✅", event)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await wa.connect()   # uses FastAPI's running loop
    yield
    await wa.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/send")
async def send(phone: str, msg: str):
    await wa.send_message(build_jid(phone), msg)
    return {"ok": True}
```

## When to Use Async

Use async client when you need:

- **High concurrency** - Handle many connections simultaneously
- **Non-blocking I/O** - Don't block on network operations
- **Integration** - Work with async frameworks (FastAPI, aiohttp)
- **Performance** - Maximum throughput

## Async vs Sync

| Feature | Async Client | Sync Client |
|---------|-------------|-------------|
| Entry point | `asyncio.run()` | `client.connect()` |
| Event handlers | `async def` | `def` |
| Performance | ⚡ Higher | 🐌 Lower |
| Concurrency | ✅ Excellent | ⚠️ Limited |
| Complexity | 🔴 Higher | 🟢 Lower |
| Best For | Production | Prototyping |

## Next Steps

Continue to:

- [Async Quick Start](quickstart.md) - Build your first async bot
- [Async Events](events.md) - Handle events asynchronously
- [Best Practices](best-practices.md) - Write efficient async code
