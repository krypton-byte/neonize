# Sending Messages

Learn how to send different types of messages using Neonize.

## Text Messages

### Simple Text Message

```python
from neonize.client import NewClient
from neonize.utils import build_jid

client = NewClient("my_bot")

# Build recipient JID
recipient = build_jid("1234567890")

# Send message
response = client.send_message(recipient, "Hello, World!")
print(f"Message ID: {response.ID}")
```

### Text with Link Preview

```python
# Enable link preview
client.send_message(
    recipient,
    "Check this out: https://github.com/krypton-byte/neonize",
    link_preview=True
)
```

### Mentioning Users

```python
# Auto-detect mentions
message = "Hello @1234567890, how are you?"
client.send_message(recipient, message)

# Manual mentions (ghost mentions)
client.send_message(
    recipient,
    "Secret mention here",
    ghost_mentions="@1234567890 @0987654321"
)
```

## Media Messages

### Sending Images

```python
# From file path
client.send_image(
    recipient,
    "path/to/image.jpg",
    caption="Beautiful sunset! 🌅"
)

# From URL
client.send_image(
    recipient,
    "https://example.com/image.jpg",
    caption="Check this image"
)

# From bytes
with open("image.jpg", "rb") as f:
    image_data = f.read()

client.send_image(recipient, image_data, caption="Image from bytes")

# View once image
client.send_image(
    recipient,
    "secret.jpg",
    caption="This will disappear",
    viewonce=True
)
```

### Sending Videos

```python
# Video message
client.send_video(
    recipient,
    "video.mp4",
    caption="Amazing video! 🎥"
)

# Video as GIF
client.send_video(
    recipient,
    "animation.mp4",
    gifplayback=True
)

# From actual GIF file
client.send_video(
    recipient,
    "animation.gif",
    is_gif=True,
    gifplayback=True
)
```

### Sending Audio

```python
# Audio message
client.send_audio(
    recipient,
    "audio.mp3"
)

# Voice note (PTT)
client.send_audio(
    recipient,
    "voice.ogg",
    ptt=True
)
```

### Sending Documents

```python
# Document with custom filename
client.send_document(
    recipient,
    "report.pdf",
    filename="Monthly_Report.pdf",
    caption="Here's the report",
    title="Monthly Report"
)

# With custom mime type
client.send_document(
    recipient,
    "data.csv",
    filename="data.csv",
    mimetype="text/csv",
    caption="Data export"
)
```

### Sending Stickers

```python
# Simple sticker
client.send_sticker(
    recipient,
    "sticker.webp"
)

# With metadata
client.send_sticker(
    recipient,
    "image.png",
    name="@MyBot",
    packname="2024",
    crop=True  # Auto crop to sticker size
)
```

### Sending Albums

```python
# Send multiple images/videos as album
files = [
    "photo1.jpg",
    "photo2.jpg",
    "video1.mp4",
]

client.send_album(
    recipient,
    files,
    caption="My vacation photos! 🏖️"
)
```

## Special Messages

### Contact Card

```python
client.send_contact(
    recipient,
    contact_name="John Doe",
    contact_number="1234567890"
)
```

### Polls

```python
from neonize.utils.enum import VoteType

# Single choice poll
poll = client.build_poll_vote_creation(
    "What's your favorite color?",
    ["Red 🔴", "Blue 🔵", "Green 🟢", "Yellow 🟡"],
    VoteType.SINGLE
)

client.send_message(recipient, poll)

# Multiple choice poll
poll = client.build_poll_vote_creation(
    "Select your hobbies:",
    ["Reading 📚", "Gaming 🎮", "Sports ⚽", "Music 🎵"],
    VoteType.MULTIPLE
)

client.send_message(recipient, poll)
```

### Reactions

```python
# React to a message
reaction = client.build_reaction(
    chat=chat_jid,
    sender=sender_jid,
    message_id="MESSAGE_ID",
    reaction="❤️"
)

client.send_message(chat_jid, reaction)
```

## Reply Messages

### Reply to Message

```python
from neonize.events import MessageEv

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    # Reply to received message
    client.reply_message("Thanks for your message!", event)
```

### Reply with Link Preview

```python
client.reply_message(
    "Check this: https://github.com/krypton-byte/neonize",
    event,
    link_preview=True
)
```

### Private Reply in Group

```python
# Reply privately (DM) to group message
client.reply_message(
    "This is a private reply",
    event,
    reply_privately=True
)
```

## Message Editing and Deletion

### Edit Message

```python
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import Message

# Edit sent message
client.edit_message(
    chat_jid,
    message_id="MSG_ID",
    new_message=Message(conversation="Updated text")
)
```

### Revoke/Delete Message

```python
# Delete message for everyone
client.revoke_message(
    chat_jid,
    sender_jid,
    message_id="MSG_ID"
)
```

## Advanced Features

### Building Messages

For more control, build messages before sending:

```python
# Build image message
image_msg = client.build_image_message(
    "photo.jpg",
    caption="Custom image",
    viewonce=False
)

# Send built message
client.send_message(recipient, image_msg)
```

### Message Context

```python
# Add message secret for extra security
client.send_message(
    recipient,
    "Secure message",
    add_msg_secret=True
)
```

### Quoted Messages

```python
# Build reply message without sending
reply_msg = client.build_reply_message(
    "This is my reply",
    quoted=original_message,
    link_preview=True
)

# Customize and send later
client.send_message(recipient, reply_msg)
```

## Best Practices

### 1. Handle Errors

```python
from neonize.exc import SendMessageError

try:
    response = client.send_message(recipient, "Hello!")
    print(f"Sent: {response.ID}")
except SendMessageError as e:
    print(f"Failed to send: {e}")
```

### 2. Rate Limiting

```python
import time

# Send multiple messages with delay
messages = ["Message 1", "Message 2", "Message 3"]

for msg in messages:
    client.send_message(recipient, msg)
    time.sleep(2)  # Wait 2 seconds between messages
```

### 3. Validate Recipients

```python
# Check if number is on WhatsApp
results = client.is_on_whatsapp("1234567890", "0987654321")

for result in results:
    if result.is_in:
        print(f"{result.jid} is on WhatsApp")
        client.send_message(
            build_jid(result.jid.User),
            "Hello!"
        )
```

### 4. Use Async for Bulk Operations

```python
import asyncio
from neonize.aioze.client import NewAClient

async def send_bulk_messages(recipients, message):
    client = NewAClient("bulk_bot")
    await client.connect()
    
    tasks = [
        client.send_message(build_jid(number), message)
        for number in recipients
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

## Next Steps

- [Receiving Messages](receiving-messages.md) - Handle incoming messages
- [Media Handling](media-handling.md) - Advanced media operations
- [Event System](event-system.md) - Event-driven messaging
