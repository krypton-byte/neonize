# Receiving Messages

Learn how to receive and handle different types of messages in Neonize.

## Basic Message Handling

### Simple Message Handler

```python
from neonize.client import NewClient
from neonize.events import MessageEv, event

client = NewClient("my_bot")

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    # Get message text
    text = event.Message.conversation
    
    if text:
        print(f"Received: {text}")
        client.reply_message(f"You said: {text}", event)

client.connect()
event.wait()
```

## Message Types

### Text Messages

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    msg = event.Message
    
    # Simple text
    if msg.conversation:
        text = msg.conversation
        print(f"Text: {text}")
    
    # Extended text (with formatting, links, etc.)
    elif msg.extendedTextMessage:
        text = msg.extendedTextMessage.text
        print(f"Extended text: {text}")
        
        # Check if it's a reply
        if msg.extendedTextMessage.contextInfo.quotedMessage:
            print("This is a reply to another message")
```

### Media Messages

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    msg = event.Message
    
    # Image message
    if msg.imageMessage:
        caption = msg.imageMessage.caption
        print(f"Received image: {caption}")
        
        # Download image
        image_data = client.download_any(msg)
        with open("received_image.jpg", "wb") as f:
            f.write(image_data)
    
    # Video message
    elif msg.videoMessage:
        caption = msg.videoMessage.caption
        print(f"Received video: {caption}")
        video_data = client.download_any(msg)
    
    # Audio message
    elif msg.audioMessage:
        is_voice = msg.audioMessage.PTT  # Push-to-talk (voice note)
        audio_data = client.download_any(msg)
    
    # Document message
    elif msg.documentMessage:
        filename = msg.documentMessage.fileName
        print(f"Received document: {filename}")
        doc_data = client.download_any(msg)
    
    # Sticker message
    elif msg.stickerMessage:
        print("Received sticker")
        sticker_data = client.download_any(msg)
```

### Special Messages

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    msg = event.Message
    
    # Contact card
    if msg.contactMessage:
        name = msg.contactMessage.displayName
        vcard = msg.contactMessage.vcard
        print(f"Received contact: {name}")
    
    # Location message
    elif msg.locationMessage:
        lat = msg.locationMessage.degreesLatitude
        lon = msg.locationMessage.degreesLongitude
        print(f"Location: {lat}, {lon}")
    
    # Poll message
    elif msg.pollCreationMessage:
        question = msg.pollCreationMessage.name
        options = [opt.optionName for opt in msg.pollCreationMessage.options]
        print(f"Poll: {question}")
        print(f"Options: {options}")
    
    # Poll vote
    elif msg.pollUpdateMessage:
        selected = msg.pollUpdateMessage.vote.selectedOptions
        print(f"Voted for: {selected}")
```

## Message Information

### Extracting Message Details

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    info = event.Info
    
    # Message ID
    message_id = info.ID
    
    # Sender information
    sender = info.MessageSource.Sender
    chat = info.MessageSource.Chat
    
    # Check if from group
    is_group = info.MessageSource.IsGroup
    
    # Check if from self
    is_from_me = info.MessageSource.IsFromMe
    
    # Timestamp
    timestamp = info.Timestamp
    
    # Push name (sender's display name)
    push_name = info.PushName
    
    print(f"Message from {push_name} ({sender.User})")
    print(f"Chat: {chat.User}")
    print(f"Group: {is_group}")
    print(f"Time: {timestamp}")
```

### Checking Message Context

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    msg = event.Message
    
    # Check if message has context (reply, mentions, etc.)
    if hasattr(msg, 'extendedTextMessage') and msg.extendedTextMessage.contextInfo:
        context = msg.extendedTextMessage.contextInfo
        
        # Quoted message (reply)
        if context.quotedMessage:
            quoted_text = context.quotedMessage.conversation
            print(f"Reply to: {quoted_text}")
        
        # Mentions
        if context.mentionedJID:
            mentions = context.mentionedJID
            print(f"Mentioned: {mentions}")
        
        # Forwarded message
        if context.isForwarded:
            print("This is a forwarded message")
```

## Downloading Media

### Download to File

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    msg = event.Message
    
    if msg.imageMessage:
        # Download directly to file
        client.download_any(msg, path="downloads/image.jpg")
        print("Image saved to downloads/image.jpg")
```

### Download to Memory

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    msg = event.Message
    
    if msg.videoMessage:
        # Download to bytes
        video_bytes = client.download_any(msg)
        
        # Process in memory
        print(f"Video size: {len(video_bytes)} bytes")
        
        # Save if needed
        with open("video.mp4", "wb") as f:
            f.write(video_bytes)
```

### Download with Progress

```python
from tqdm import tqdm

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    msg = event.Message
    
    if msg.documentMessage:
        file_size = msg.documentMessage.fileLength
        filename = msg.documentMessage.fileName
        
        print(f"Downloading {filename} ({file_size} bytes)...")
        
        # Download
        data = client.download_any(msg)
        
        # Save
        with open(f"downloads/{filename}", "wb") as f:
            f.write(data)
        
        print("Download complete!")
```

## Message Filtering

### Filter by Sender

```python
ADMIN_NUMBERS = ["1234567890", "0987654321"]

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    sender = event.Info.MessageSource.Sender.User
    
    # Only respond to admins
    if sender in ADMIN_NUMBERS:
        text = event.Message.conversation
        if text == "/admin":
            client.reply_message("Admin command received", event)
```

### Filter by Chat Type

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    is_group = event.Info.MessageSource.IsGroup
    
    if is_group:
        # Group message handling
        print("Message from group")
    else:
        # Private message handling
        print("Private message")
```

### Filter by Message Type

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    msg = event.Message
    
    # Only handle text messages
    if msg.conversation or msg.extendedTextMessage:
        text = msg.conversation or msg.extendedTextMessage.text
        process_text_message(text, event)
    
    # Only handle media
    elif any([msg.imageMessage, msg.videoMessage, msg.audioMessage]):
        process_media_message(msg, event)
```

## Command Handling

### Simple Command Parser

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    text = event.Message.conversation or ""
    
    if not text.startswith("/"):
        return
    
    # Parse command
    parts = text.split()
    command = parts[0][1:]  # Remove /
    args = parts[1:] if len(parts) > 1 else []
    
    # Handle commands
    if command == "help":
        help_text = """
Available commands:
/help - Show this help
/ping - Pong!
/echo <text> - Echo back text
        """
        client.reply_message(help_text, event)
    
    elif command == "ping":
        client.reply_message("Pong! 🏓", event)
    
    elif command == "echo":
        if args:
            client.reply_message(" ".join(args), event)
        else:
            client.reply_message("Usage: /echo <text>", event)
```

### Advanced Command System

```python
from typing import Callable, Dict

class CommandHandler:
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
    
    def command(self, name: str):
        def decorator(func: Callable):
            self.commands[name] = func
            return func
        return decorator
    
    def handle(self, client: NewClient, event: MessageEv):
        text = event.Message.conversation or ""
        
        if not text.startswith("/"):
            return
        
        parts = text.split()
        command = parts[0][1:]
        args = parts[1:]
        
        if command in self.commands:
            self.commands[command](client, event, args)

# Usage
handler = CommandHandler()

@handler.command("start")
def start_command(client: NewClient, event: MessageEv, args):
    client.reply_message("Welcome! Use /help for commands", event)

@handler.command("info")
def info_command(client: NewClient, event: MessageEv, args):
    sender = event.Info.PushName
    client.reply_message(f"Hello {sender}!", event)

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    handler.handle(client, event)
```

## Message Receipts

### Handle Read Receipts

```python
from neonize.events import ReceiptEv

@client.event(ReceiptEv)
def on_receipt(client: NewClient, event: ReceiptEv):
    receipt_type = event.Type
    message_ids = event.MessageIDs
    
    print(f"Receipt type: {receipt_type}")
    print(f"Message IDs: {message_ids}")
```

### Mark Messages as Read

```python
from neonize.utils.enum import ReceiptType

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    # Auto mark as read
    client.mark_read(
        [event.Info.ID],
        chat=event.Info.MessageSource.Chat,
        sender=event.Info.MessageSource.Sender,
        receipt=ReceiptType.READ
    )
```

## Best Practices

### 1. Error Handling

```python
@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    try:
        text = event.Message.conversation
        if text:
            process_message(text)
    except Exception as e:
        print(f"Error processing message: {e}")
        client.reply_message("Sorry, an error occurred", event)
```

### 2. Async Processing

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    # Process message in background
    executor.submit(process_message_async, client, event)

def process_message_async(client: NewClient, event: MessageEv):
    # Long-running task
    result = heavy_computation()
    client.reply_message(f"Result: {result}", event)
```

### 3. Rate Limiting

```python
from collections import defaultdict
import time

# Track last message time per user
last_message_time = defaultdict(float)
RATE_LIMIT = 2  # seconds

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    sender = event.Info.MessageSource.Sender.User
    current_time = time.time()
    
    # Check rate limit
    if current_time - last_message_time[sender] < RATE_LIMIT:
        return  # Ignore message
    
    last_message_time[sender] = current_time
    
    # Process message
    handle_message(client, event)
```

## Next Steps

- [Event System](event-system.md) - Learn about all events
- [Media Handling](media-handling.md) - Advanced media processing
- [Group Management](group-management.md) - Handle group messages
