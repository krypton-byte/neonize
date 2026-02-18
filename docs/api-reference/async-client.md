# NewClient

::: neonize.client.NewClient
    options:
      show_source: true
      heading_level: 2

## Overview

`NewClient` is the main synchronous client for interacting with WhatsApp through Neonize. It provides a complete interface for sending messages, handling media, managing groups, and responding to events.

## Constructor

```python
from neonize.client import NewClient

client = NewClient(
    name: str,
    database: str = None,
    props: DeviceProps = None
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | Required | Unique identifier for this client session |
| `database` | `str` | `None` | Database connection string (SQLite or PostgreSQL) |
| `props` | `DeviceProps` | `None` | Custom device properties |

### Examples

```python
# Basic client with default SQLite database
client = NewClient("my_bot")

# Custom database path
client = NewClient("my_bot", database="./sessions/bot.db")

# PostgreSQL database
client = NewClient(
    "production_bot",
    database="postgresql://user:pass@localhost:5432/whatsapp"
)

# Custom device properties
from neonize.proto.waCompanionReg.WAWebProtobufsCompanionReg_pb2 import DeviceProps

props = DeviceProps(os="Custom Bot v1.0")
client = NewClient("custom_bot", props=props)
```

## Connection Methods

### connect()

Establish connection to WhatsApp servers.

```python
client.connect()
```

**Raises:**
- `ConnectionError`: If connection fails

**Example:**
```python
try:
    client.connect()
    print("Connected successfully!")
except ConnectionError as e:
    print(f"Connection failed: {e}")
```

### disconnect()

Gracefully disconnect from WhatsApp.

```python
client.disconnect()
```

**Example:**
```python
client.disconnect()
print("Disconnected")
```

### logout()

Logout from WhatsApp and clear session.

```python
client.logout()
```

**Example:**
```python
client.logout()
print("Logged out and session cleared")
```

## Message Methods

### send_message()

Send a text message or custom message object.

```python
response = client.send_message(
    to: str,
    message: Union[str, Message],
    link_preview: bool = False,
    ghost_mentions: str = "",
    add_msg_secret: bool = False
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `to` | `str` | Required | Recipient JID |
| `message` | `str\|Message` | Required | Message text or Message object |
| `link_preview` | `bool` | `False` | Enable link preview |
| `ghost_mentions` | `str` | `""` | Mention users without notification |
| `add_msg_secret` | `bool` | `False` | Add message secret |

**Returns:** `SendResponse` - Contains message ID and timestamp

**Example:**
```python
from neonize.utils import build_jid

recipient = build_jid("1234567890")

# Simple text
response = client.send_message(recipient, "Hello!")
print(f"Sent: {response.ID}")

# With link preview
client.send_message(
    recipient,
    "Check this: https://github.com/krypton-byte/neonize",
    link_preview=True
)

# With ghost mentions
client.send_message(
    recipient,
    "Secret mention",
    ghost_mentions="@1234567890"
)
```

### reply_message()

Reply to a message.

```python
response = client.reply_message(
    text: str,
    quoted: MessageEv,
    link_preview: bool = False,
    reply_privately: bool = False
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | Required | Reply text |
| `quoted` | `MessageEv` | Required | Message to reply to |
| `link_preview` | `bool` | `False` | Enable link preview |
| `reply_privately` | `bool` | `False` | Reply privately in groups |

**Example:**
```python
from neonize.events import MessageEv

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    # Reply to message
    client.reply_message("Thanks!", event)
    
    # Private reply in group
    client.reply_message(
        "This is private",
        event,
        reply_privately=True
    )
```

### edit_message()

Edit a sent message.

```python
client.edit_message(
    chat: str,
    message_id: str,
    new_message: Message
)
```

**Example:**
```python
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import Message

new_msg = Message(conversation="Updated text")
client.edit_message(chat_jid, "MSG_ID", new_msg)
```

### revoke_message()

Delete a message for everyone.

```python
client.revoke_message(
    chat: str,
    sender: str,
    message_id: str
)
```

**Example:**
```python
client.revoke_message(chat_jid, sender_jid, "MSG_ID")
```

## Media Methods

### send_image()

Send an image message.

```python
response = client.send_image(
    to: str,
    image: Union[str, bytes],
    caption: str = "",
    viewonce: bool = False
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `to` | `str` | Recipient JID |
| `image` | `str\|bytes` | Image path, URL, or bytes |
| `caption` | `str` | Image caption |
| `viewonce` | `bool` | View once mode |

**Example:**
```python
# From file
client.send_image(recipient, "photo.jpg", caption="Check this!")

# From URL
client.send_image(
    recipient,
    "https://example.com/image.jpg",
    caption="Downloaded image"
)

# From bytes
with open("image.jpg", "rb") as f:
    data = f.read()
client.send_image(recipient, data)

# View once
client.send_image(recipient, "secret.jpg", viewonce=True)
```

### send_video()

Send a video message.

```python
response = client.send_video(
    to: str,
    video: Union[str, bytes],
    caption: str = "",
    viewonce: bool = False,
    gifplayback: bool = False,
    is_gif: bool = False
)
```

**Example:**
```python
# Regular video
client.send_video(recipient, "video.mp4", caption="My video")

# As GIF
client.send_video(recipient, "animation.mp4", gifplayback=True)

# From GIF file
client.send_video(recipient, "animation.gif", is_gif=True)
```

### send_audio()

Send an audio message.

```python
response = client.send_audio(
    to: str,
    audio: Union[str, bytes],
    ptt: bool = False
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `to` | `str` | Recipient JID |
| `audio` | `str\|bytes` | Audio path or bytes |
| `ptt` | `bool` | Push-to-talk (voice note) |

**Example:**
```python
# Audio file
client.send_audio(recipient, "song.mp3")

# Voice note
client.send_audio(recipient, "voice.ogg", ptt=True)
```

### send_document()

Send a document.

```python
response = client.send_document(
    to: str,
    document: Union[str, bytes],
    filename: str = "",
    mimetype: str = "",
    caption: str = "",
    title: str = ""
)
```

**Example:**
```python
client.send_document(
    recipient,
    "report.pdf",
    filename="Monthly_Report.pdf",
    caption="Here's the report",
    title="Monthly Report"
)
```

### send_sticker()

Send a sticker.

```python
response = client.send_sticker(
    to: str,
    sticker: Union[str, bytes],
    name: str = "@MyBot",
    packname: str = "2024",
    crop: bool = False
)
```

**Example:**
```python
# Simple sticker
client.send_sticker(recipient, "sticker.webp")

# With metadata
client.send_sticker(
    recipient,
    "image.png",
    name="@MyBot",
    packname="2024",
    crop=True
)
```

### download_any()

Download media from a message.

```python
data = client.download_any(
    message: Message,
    path: str = None
)
```

**Returns:** `bytes` if path is None, else saves to file

**Example:**
```python
from neonize.events import MessageEv

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    msg = event.Message
    
    # Download to memory
    if msg.imageMessage:
        image_data = client.download_any(msg)
        print(f"Downloaded {len(image_data)} bytes")
    
    # Download to file
    if msg.documentMessage:
        filename = msg.documentMessage.fileName
        client.download_any(msg, path=f"downloads/{filename}")
```

## Group Methods

### get_group_info()

Get group information.

```python
info = client.get_group_info(group_jid: str)
```

**Returns:** Group metadata

### create_group()

Create a new group.

```python
group = client.create_group(
    name: str,
    participants: List[str]
)
```

### update_group_name()

Update group name.

```python
client.update_group_name(
    group_jid: str,
    name: str
)
```

## Utility Methods

### get_me()

Get own user information.

```python
me = client.get_me()
print(f"My JID: {me.JID.User}")
```

### is_on_whatsapp()

Check if numbers are on WhatsApp.

```python
results = client.is_on_whatsapp("1234567890", "0987654321")

for result in results:
    if result.is_in:
        print(f"{result.jid} is on WhatsApp")
```

### mark_read()

Mark messages as read.

```python
from neonize.utils.enum import ReceiptType

client.mark_read(
    message_ids: List[str],
    chat: str,
    sender: str,
    receipt: ReceiptType = ReceiptType.READ
)
```

## Event Decorator

### @client.event(EventType)

Register event handlers for a specific event type.

```python
from neonize.events import MessageEv, ReceiptEv

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    print("Message received!")

@client.event(ReceiptEv)
def on_receipt(client: NewClient, event: ReceiptEv):
    print("Receipt received!")
```

## Properties

### is_connected

Check if client is connected.

```python
if client.is_connected:
    print("Connected!")
```

### is_logged_in

Check if client is logged in.

```python
if client.is_logged_in:
    print("Logged in!")
```

## See Also

- [NewAClient](async-client.md) - Async version
- [Events](events.md) - Event types
- [Examples](../examples/index.md) - Usage examples
