# Async Client Overview

`neonize.aioze.client.NewAClient` is the asyncio-native mirror of the
synchronous client. The method surface is identical — every sync method has
an async counterpart with the same name and parameters, awaited instead of
called:

```python
from neonize.aioze.client import NewAClient

client = NewAClient("session.db")

await client.send_message(chat, "Hello")   # instead of client.send_message(...)
```

## When to Choose Async

| Scenario | Recommendation |
| --- | --- |
| Web service (FastAPI, aiohttp) handling WhatsApp in-process | Async client |
| Many concurrent sessions | Async + `ClientFactory` |
| Simple single-session scripts | Sync client |

Both clients can coexist; they share nothing at runtime.

## Multi-Session with ClientFactory

`ClientFactory` manages a fleet of clients over one SQLite database:

```python
from neonize.aioze.client import ClientFactory

factory = ClientFactory("sessions.db")

# Resume every stored device:
for device in factory.get_all_devices():
    factory.new_client(device.JID)

# Or create a fresh pairing slot:
factory.new_client(uuid="bot-3")
```

Events registered on the factory fan out across **all** managed clients.

```python
@factory.event(MessageEv)
async def on_message(client: NewAClient, ev: MessageEv):
    await client.reply_message("pong", ev.Message)
```

Run until interrupted:

```python
await factory.idle_all()
```

The full walkthrough lives in [Quick Start](quickstart.md).

## What Stays the Same

- Event types (`neonize.aioze.events`) carry identical payloads.
- Constructors take the same options.
- Errors (`neonize.exc`) are shared between both clients.
