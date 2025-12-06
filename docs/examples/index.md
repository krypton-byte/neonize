# Examples

Practical examples demonstrating Neonize features and common use cases.

## Available Examples

### Getting Started

- **[Basic Bot](basic-bot.md)** - Simple bot responding to messages
- **[Async Bot](async-bot.md)** - Asynchronous version of the basic bot

### Advanced Examples

- **[Multi-Session](multi-session.md)** - Managing multiple WhatsApp accounts
- **[Media Bot](media-bot.md)** - Handling images, videos, and documents
- **[Group Bot](group-bot.md)** - Managing groups and group messages

## Quick Examples

### Echo Bot

A simple bot that echoes back all messages:

```python
from neonize.client import NewClient
from neonize.events import MessageEv, event

client = NewClient("echo_bot")

@client.event
def on_message(client: NewClient, event: MessageEv):
    text = event.Message.conversation
    if text:
        client.reply_message(f"You said: {text}", event)

client.connect()
event.wait()
```

### Command Bot

Bot with command handling:

```python
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, event

client = NewClient("command_bot")

@client.event
def on_connected(client: NewClient, event: ConnectedEv):
    print(f"✅ Bot connected as {event.device.User}")

@client.event
def on_message(client: NewClient, event: MessageEv):
    text = event.Message.conversation or ""
    
    if text.startswith("/"):
        command = text.split()[0][1:]  # Remove /
        
        if command == "help":
            help_text = """
Available commands:
/help - Show this help
/ping - Pong!
/time - Current time
/info - Bot information
            """
            client.reply_message(help_text, event)
        
        elif command == "ping":
            client.reply_message("Pong! 🏓", event)
        
        elif command == "time":
            from datetime import datetime
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client.reply_message(f"🕐 {now}", event)
        
        elif command == "info":
            info = f"Bot: Neonize Command Bot\nVersion: 1.0"
            client.reply_message(info, event)

client.connect()
event.wait()
```

### Auto-Reply Bot

Bot with auto-reply functionality:

```python
from neonize.client import NewClient
from neonize.events import MessageEv, event

client = NewClient("auto_reply_bot")

# Auto-reply rules
AUTO_REPLIES = {
    "hello": "Hello! How can I help you?",
    "hi": "Hi there! 👋",
    "thanks": "You're welcome!",
    "bye": "Goodbye! Have a great day! 👋",
}

@client.event
def on_message(client: NewClient, event: MessageEv):
    text = (event.Message.conversation or "").lower().strip()
    
    # Check if message matches any auto-reply rule
    if text in AUTO_REPLIES:
        client.reply_message(AUTO_REPLIES[text], event)

client.connect()
event.wait()
```

## More Examples

For complete, runnable examples, check the examples in the repository:

- [examples/basic.py](https://github.com/krypton-byte/neonize/blob/main/examples/basic.py)
- [examples/async_basic.py](https://github.com/krypton-byte/neonize/blob/main/examples/async_basic.py)
- [examples/multisession.py](https://github.com/krypton-byte/neonize/blob/main/examples/multisession.py)

## Need More Examples?

- Check the [User Guide](../user-guide/index.md) for feature-specific examples
- Visit [GitHub Discussions](https://github.com/krypton-byte/neonize/discussions) to share your examples
- Browse the [API Reference](../api-reference/index.md) for method examples
