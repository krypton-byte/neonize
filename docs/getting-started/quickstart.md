# Quick Start

This guide will help you create your first WhatsApp bot using Neonize in just a few minutes.

## Your First Bot

Let's create a simple bot that responds to messages:

### Step 1: Create a Python File

Create a new file called `bot.py`:

```python
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, event

# Initialize the client
client = NewClient("my_first_bot")

@client.event
def on_connected(client: NewClient, event: ConnectedEv):
    print("✅ Bot connected successfully!")
    print(f"📱 Logged in as: {event.device.User}")

@client.event
def on_message(client: NewClient, event: MessageEv):
    # Get message text
    text = event.Message.conversation or event.Message.extendedTextMessage.text
    
    # Respond to specific messages
    if text == "ping":
        client.reply_message("pong! 🏓", event)
    elif text == "hello":
        client.reply_message("Hello! 👋 How can I help you?", event)

# Connect and start the bot
client.connect()
event.wait()  # Keep the bot running
```

### Step 2: Run Your Bot

Execute your bot:

```bash
python bot.py
```

### Step 3: Authenticate

When you run the bot for the first time, it will display a QR code in your terminal:

1. Open WhatsApp on your phone
2. Go to **Settings** → **Linked Devices**
3. Tap **Link a Device**
4. Scan the QR code displayed in your terminal

!!! success "Connected!"
    Once authenticated, you'll see "✅ Bot connected successfully!" in your terminal.

### Step 4: Test Your Bot

Send a message to your bot:

- Send `ping` → Bot replies: `pong! 🏓`
- Send `hello` → Bot replies: `Hello! 👋 How can I help you?`

## Understanding the Code

Let's break down what each part does:

### 1. Import Required Modules

```python
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, event
```

- `NewClient` - Main client class for WhatsApp connection
- `MessageEv` - Event triggered when receiving messages
- `ConnectedEv` - Event triggered when bot connects successfully
- `event` - Threading event to keep the bot running

### 2. Create the Client

```python
client = NewClient("my_first_bot")
```

This creates a new client instance with the session name "my_first_bot". The session data will be stored in `my_first_bot.db`.

### 3. Event Handlers

```python
@client.event
def on_connected(client: NewClient, event: ConnectedEv):
    print("✅ Bot connected successfully!")
```

The `@client.event` decorator registers event handlers. Functions are automatically matched to events based on their parameter types.

### 4. Message Processing

```python
text = event.Message.conversation or event.Message.extendedTextMessage.text
```

Messages can be either simple text (`conversation`) or extended text messages. This line handles both cases.

### 5. Start the Bot

```python
client.connect()
event.wait()
```

- `connect()` - Establishes connection to WhatsApp
- `event.wait()` - Keeps the bot running indefinitely

## Async Version

Neonize also supports async/await syntax:

```python
import asyncio
from neonize.aioze.client import NewAClient
from neonize.aioze.events import MessageEv, ConnectedEv

async def main():
    client = NewAClient("async_bot")
    
    @client.event
    async def on_connected(client: NewAClient, event: ConnectedEv):
        print("✅ Async bot connected!")
    
    @client.event
    async def on_message(client: NewAClient, event: MessageEv):
        text = event.Message.conversation
        if text == "ping":
            await client.reply_message("pong! 🏓", event)
    
    await client.connect()

asyncio.run(main())
```

## Database Configuration

By default, Neonize uses SQLite. You can specify a custom database:

### SQLite (Default)

```python
client = NewClient("my_bot", database="./my_bot.db")
```

### PostgreSQL (Production)

```python
client = NewClient(
    "my_bot",
    database="postgresql://user:password@localhost:5432/whatsapp"
)
```

## Common Patterns

### Handling Different Message Types

```python
@client.event
def on_message(client: NewClient, event: MessageEv):
    msg = event.Message
    
    # Text message
    if msg.conversation:
        print(f"Text: {msg.conversation}")
    
    # Image with caption
    elif msg.imageMessage:
        print(f"Image: {msg.imageMessage.caption}")
    
    # Video with caption
    elif msg.videoMessage:
        print(f"Video: {msg.videoMessage.caption}")
    
    # Document
    elif msg.documentMessage:
        print(f"Document: {msg.documentMessage.fileName}")
```

### Sending Different Message Types

```python
from neonize.utils import build_jid

# Build JID from phone number
recipient = build_jid("1234567890")

# Send text
client.send_message(recipient, "Hello!")

# Send image
client.send_image(
    recipient,
    "path/to/image.jpg",
    caption="Check this out!"
)

# Send video
client.send_video(
    recipient,
    "path/to/video.mp4",
    caption="Amazing video"
)

# Send document
client.send_document(
    recipient,
    "path/to/document.pdf",
    filename="report.pdf"
)
```

### Replying to Messages

```python
@client.event
def on_message(client: NewClient, event: MessageEv):
    # Reply to the message
    client.reply_message("I received your message!", event)
    
    # Reply with link preview
    client.reply_message(
        "Check this out: https://github.com/krypton-byte/neonize",
        event,
        link_preview=True
    )
```

## Next Steps

Now that you have a working bot, explore more features:

- [Authentication Methods](authentication.md) - Learn about pairing codes
- [Event System](../user-guide/event-system.md) - Handle different events
- [Sending Messages](../user-guide/sending-messages.md) - Send various message types
- [Media Handling](../user-guide/media-handling.md) - Work with images, videos, and more
- [Examples](../examples/index.md) - Browse more code examples

!!! tip "Best Practices"
    - Use meaningful session names for different bots
    - Handle errors gracefully with try-except blocks
    - Use environment variables for sensitive configuration
    - Enable logging for debugging: `logging.basicConfig(level=logging.DEBUG)`

!!! warning "Rate Limiting"
    WhatsApp has rate limits to prevent spam. Avoid sending too many messages in a short time to prevent temporary bans.
