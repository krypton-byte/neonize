# Async Event Handling

## Registering on a Client or Factory

Both `NewAClient` and `ClientFactory` expose the same decorator. Handlers
are coroutines:

```python
from neonize.aioze.client import NewAClient, ClientFactory
from neonize.aioze.events import MessageEv, ConnectedEv

client = NewAClient("session.db")

@client.event(MessageEv)
async def on_message(client: NewAClient, ev: MessageEv) -> None:
    await client.reply_message("ack", ev.Message)

# Factory-wide handlers see events from every managed client:
factory = ClientFactory("sessions.db")

@factory.event(ConnectedEv)
async def on_connected(client: NewAClient, ev: ConnectedEv) -> None:
    print(f"{client.me.JID.User} connected")
```

The handler's first argument is always the specific client instance that
received the event — with factories this tells you which session produced
it.

## Event Payloads

Payload classes come from `neonize.aioze.events`; their fields match the
sync catalog exactly (see the [event model](../core-concepts/event-model.md)
for the complete list).

```python
from neonize.aioze.events import (
    CallOfferEv, ChatPresenceEv, GroupInfoEv, JoinedGroupEv,
    MessageEv, ReceiptEv, UndecryptableMessageEv,
)
```

## Concurrency Guarantees

- Handlers for **different clients** may interleave.
- A slow handler does not block the Go event thread — but it can delay other
  coroutines on your loop.
- Exceptions in a handler are logged; they do not stop dispatch or other
  handlers.

For CPU-heavy work, hand off to executors:

```python
result = await loop.run_in_executor(None, parse_media, data)
```

## Per-Client State

Store per-session state keyed by the client UUID rather than globals:

```python
state: dict[str, dict] = {}

@client.event(MessageEv)
async def on_message(client: NewAClient, ev: MessageEv) -> None:
    session_state = state.setdefault(client.uuid.decode(), {})
```

## Stopping from Within a Handler

```python
await client.stop()          # stops this client only
await factory.stop()         # stops everything and exits idle_all()
```
