# Receiving Messages

## The MessageEv Event

Everything arrives through `MessageEv`. The two members you need most:

```python
from neonize.client import NewClient
from neonize.events import MessageEv

@client.event(MessageEv)
def on_message(client: NewClient, ev: MessageEv) -> None:
    text = ev.Message.conversation or ev.Message.extendedTextMessage.text
    chat = ev.Info.MessageSource.Chat
    sender = ev.Info.MessageSource.Sender
```

| Member | Description |
| --- | --- |
| `ev.Message` | Protobuf `Message` — inspect fields to learn the content type |
| `ev.Info.ID` | Message ID; keep it for replies, reactions, mark-read, pinning |
| `ev.Info.MessageSource.Chat` | Destination JID (user, group or channel) |
| `ev.Info.MessageSource.Sender` | Actual sender JID (differs from `Chat` in groups) |
| `ev.Info.Timestamp` | Unix timestamp |

## Detecting Content Types

The protobuf payload has one populated field per type:

```python
m = ev.Message

if m.conversation:
    ...  # plain text
elif m.imageMessage:
    ...  # image — caption in .caption, media key for download
elif m.videoMessage:
    ...
elif m.audioMessage:
    ...  # ptt=True means voice note
elif m.documentMessage:
    ...  # filename in .fileName
elif m.extendedTextMessage:
    ...  # reply, link preview, or mention text
elif m.reactionMessage:
    ...
```

!!! tip "Text shortcut"
    `m.conversation or m.extendedTextMessage.text` covers nearly all text
    messages. Guard against `None` when the message is media-only.

## Downloading Media

`download_any` extracts the payload from any message and either returns the
bytes or writes them to a path:

```python
data: bytes = client.download_any(ev.Message)

client.download_any(ev.Message, "downloads/photo.jpg")   # saved to disk
```

Works with images, videos, audio, documents and stickers. See
[Media Handling](media-handling.md).

## Ignoring Your Own Messages and Status

Filter early to keep handlers clean:

```python
@client.event(MessageEv)
def on_message(client: NewClient, ev: MessageEv) -> None:
    if ev.Info.MessageSource.Chat.Server == "broadcast":
        return                      # status updates
    if ev.Info.MessageSource.Sender == client.me.JID:
        return                      # own outgoing echo
    ...
```

## Marking Messages as Read

```python
from neonize.utils.enum import ReceiptType

client.mark_read(
    ev.Info.ID,
    chat=ev.Info.MessageSource.Chat,
    sender=ev.Info.MessageSource.Sender,
    receipt=ReceiptType.READ,       # or DELIVERED
)
```

`mark_read` accepts several IDs at once for batch acknowledgement.

## Typing Indicators

Show a composing indicator while preparing an answer:

```python
from neonize.utils.enum import ChatPresence, ChatPresenceMedia

client.send_chat_presence(chat, ChatPresence.COMPOSING, ChatPresenceMedia.TEXT)
# ... do work ...
client.send_chat_presence(chat, ChatPresence.PAUSED, ChatPresenceMedia.TEXT)
```

## Undecryptable Messages

If a message cannot be decrypted (e.g. sent with a protocol feature this
build predates), you receive `UndecryptableMessageEv` instead of
`MessageEv`. Register both when completeness matters.

## Receipts for Outgoing Messages

After sending, acknowledgements arrive as `ReceiptEv` — delivered, read, or
played — keyed by the original message ID returned in `SendResponse.ID`.
