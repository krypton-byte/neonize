# Quick Start

This page builds a working echo bot in under five minutes.

## 1. Create the Client

```python
from neonize.client import NewClient

client = NewClient("session.db")
```

The `name` argument is the path of the SQLite file where the session is
persisted. On the first run it is created empty; on every later run the
stored session is reused and no re-pairing is needed.

## 2. Register Event Handlers

Handlers are plain functions decorated with `@client.event(EventType)`.
Each handler receives the client instance and the typed event object.

```python
from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, PairStatusEv

@client.event(PairStatusEv)
def on_paired(client: NewClient, event: PairStatusEv) -> None:
    print(f"Paired as {event.ID.User}")

@client.event(ConnectedEv)
def on_connected(client: NewClient, event: ConnectedEv) -> None:
    print("Connected to WhatsApp")

@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv) -> None:
    ...
```

## 3. Handle Incoming Messages

`MessageEv` carries two important members:

| Member | Description |
| --- | --- |
| `message.Message` | The protobuf `Message` payload (conversation text, image, document, ...) |
| `message.Info.MessageSource.Chat` | The `JID` of the chat the message belongs to |

```python
@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv) -> None:
    from neonize import extract_text

    text = extract_text(message.Message)
    chat = message.Info.MessageSource.Chat

    if text == "ping":
        client.reply_message("pong", message)
```

`extract_text()` handles plain text, extended text (with mentions/links),
and the caption fields of image, video and document messages in one call.

## 4. Connect

```python
client.connect()
```

On the first run a QR code is printed to the terminal — scan it with
WhatsApp (Settings > Linked Devices > Link a Device). The session is then
stored and every future `connect()` reuses it silently.

## Complete Example

```python
from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv

client = NewClient("session.db")

@client.event(ConnectedEv)
def on_connected(client: NewClient, _: ConnectedEv) -> None:
    print("Connected")

@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv) -> None:
    from neonize import extract_text

    text = extract_text(message.Message)
    chat = message.Info.MessageSource.Chat

    if text == "ping":
        client.reply_message("pong", message)

if __name__ == "__main__":
    client.connect()
```

Run it:

```bash
python bot.py
```

## Next Steps

- Pair without scanning a QR code: [Authentication](authentication.md)
- Send images, videos, documents and stickers: [Sending Messages](../guides/sending-messages.md)
- Understand the event system in depth: [Event Model](../core-concepts/event-model.md)
- Use asyncio instead of threads: [Async Client](../async/index.md)

!!! info "Phone number strings"
    You can pass a phone number string directly to `send_message()` without
    building a JID first:

    ```python
    client.send_message("6281234567890", "Hello!")
    ```
