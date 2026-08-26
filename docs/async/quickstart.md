# Async Quick Start

A complete asyncio echo bot:

```python
import signal
import asyncio

from neonize.aioze.client import ClientFactory, NewAClient
from neonize.aioze.events import ConnectedEv, MessageEv, PairStatusEv

factory = ClientFactory("session.db")


@factory.event(PairStatusEv)
async def on_paired(_: NewAClient, event: PairStatusEv) -> None:
    print(f"Paired as {event.ID.User}")


@factory.event(ConnectedEv)
async def on_connected(_: NewAClient, __: ConnectedEv) -> None:
    print("Connected")


@factory.event(MessageEv)
async def on_message(client: NewAClient, ev: MessageEv) -> None:
    text = ev.Message.conversation or ev.Message.extendedTextMessage.text
    if text == "ping":
        await client.reply_message("pong", ev.Message)


def interrupted(*_) -> None:
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(factory.stop(), loop)


signal.signal(signal.SIGINT, interrupted)


if __name__ == "__main__":
    factory.idle_all()   # blocks; starts all managed clients
```

## Step by Step

### 1. Create the factory or a single client

For one session, `NewAClient` alone is enough — call `await client.connect()`.

For several sessions in one database use `ClientFactory`, which owns client
lifecycle and shared event dispatch.

### 2. Register async handlers

Handlers are coroutines decorated the same way as sync code. The factory
dispatches events from every managed client through them.

### 3. Run

`factory.idle_all()` connects every client and parks until `factory.stop()`
is called (e.g. from a SIGINT handler). A single client uses
`await client.connect()` plus your own loop management, or
`await client.idle()`.

## Pairing

Identical to the sync flow: first connect prints the QR code, and
`PairPhone` returns a link code:

```python
code = await client.PairPhone("628123456789", True)
```

## Mixing Sync Libraries

Inside handlers you can still call blocking libraries freely — handler
coroutines run on your event loop, so wrap blocking calls with
`asyncio.to_thread` when they are slow:

```python
result = await asyncio.to_thread(expensive_blocking_function, arg)
```

See [Best Practices](best-practices.md) for pitfalls.
