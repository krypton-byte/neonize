# API Reference

Welcome to the Neonize API reference documentation. This section provides detailed information about all classes, methods, and utilities available in the Neonize library.

## Core Modules

### [Client](client.md)
The main synchronous client for interacting with WhatsApp.

- `NewClient` - Synchronous WhatsApp client
- Connection management
- Message sending/receiving
- Media handling
- Group operations

### [Async Client](async-client.md)
Asynchronous client for high-performance applications.

- `NewAClient` - Async WhatsApp client
- Async/await support
- Concurrent operations
- Event handling

### [Events](events.md)
Event system for handling WhatsApp events.

- `MessageEv` - Message events
- `ReceiptEv` - Read receipts
- `PresenceEv` - Online/offline status
- `GroupInfoEv` - Group updates
- And more...

### [Types](types.md)
Type definitions and data structures.

- JID types
- Message types
- Contact information
- Group metadata

### [Utils](utils.md)
Utility functions and helpers.

- `build_jid()` - JID construction
- `build_jid_from_number()` - JID from phone number
- Media utilities
- Encoding/decoding helpers

### [Exceptions](exceptions.md)
Exception classes for error handling.

- `SendMessageError`
- `DownloadMediaError`
- `ConnectionError`
- Custom exceptions

## Protocol Buffers

### [Proto Messages](proto.md)
WhatsApp protocol buffer definitions.

- Message structures
- Media messages
- Group messages
- Status messages

## Quick Reference

### Common Operations

```python
from neonize.client import NewClient
from neonize.utils import build_jid
from neonize.events import MessageEv

# Create client
client = NewClient("my_bot")

# Connect
client.connect()

# Send message
recipient = build_jid("1234567890")
client.send_message(recipient, "Hello!")

# Handle events
@client.event
def on_message(client: NewClient, event: MessageEv):
    print(f"Received: {event.Message.conversation}")
```

### Type Hints

```python
from typing import Optional
from neonize.client import NewClient
from neonize.events import MessageEv
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import Message

def send_text(
    client: NewClient,
    recipient: str,
    text: str,
    quote: Optional[Message] = None
) -> str:
    """Send a text message.
    
    Args:
        client: WhatsApp client
        recipient: Recipient JID
        text: Message text
        quote: Optional message to quote
        
    Returns:
        Message ID
    """
    if quote:
        response = client.reply_message(text, quote)
    else:
        response = client.send_message(recipient, text)
    
    return response.ID
```

## Module Index

| Module | Description |
|--------|-------------|
| `neonize.client` | Synchronous WhatsApp client |
| `neonize.aioze.client` | Asynchronous WhatsApp client |
| `neonize.events` | Event definitions and handlers |
| `neonize.types` | Type definitions |
| `neonize.utils` | Utility functions |
| `neonize.exc` | Exception classes |
| `neonize.proto` | Protocol buffer messages |
| `neonize.const` | Constants and enums |
| `neonize.download` | Media download utilities |
| `neonize.builder` | Message builder utilities |

## Class Hierarchy

```
NewClient
├── Connection Management
│   ├── connect()
│   ├── disconnect()
│   └── logout()
├── Message Operations
│   ├── send_message()
│   ├── reply_message()
│   ├── edit_message()
│   └── revoke_message()
├── Media Operations
│   ├── send_image()
│   ├── send_video()
│   ├── send_audio()
│   ├── send_document()
│   └── download_any()
├── Group Operations
│   ├── get_group_info()
│   ├── create_group()
│   ├── update_group_name()
│   └── add_participants()
└── Utility Methods
    ├── get_me()
    ├── is_on_whatsapp()
    ├── get_contact()
    └── mark_read()

NewAClient (inherits from NewClient)
└── Async versions of all methods
```

## Event Types

| Event | Trigger | Handler Signature |
|-------|---------|------------------|
| `MessageEv` | New message received | `(client, event: MessageEv)` |
| `ReceiptEv` | Message receipt | `(client, event: ReceiptEv)` |
| `PresenceEv` | User presence change | `(client, event: PresenceEv)` |
| `GroupInfoEv` | Group info update | `(client, event: GroupInfoEv)` |
| `PictureEv` | Profile picture change | `(client, event: PictureEv)` |
| `ConnectedEv` | Client connected | `(client, event: ConnectedEv)` |
| `PairStatusEv` | Pairing status change | `(client, event: PairStatusEv)` |
| `LoggedInEv` | Successfully logged in | `(client, event: LoggedInEv)` |

## Constants and Enums

### Message Types

```python
from neonize.const import MessageType

MessageType.TEXT
MessageType.IMAGE
MessageType.VIDEO
MessageType.AUDIO
MessageType.DOCUMENT
MessageType.STICKER
MessageType.CONTACT
MessageType.LOCATION
MessageType.POLL
```

### Receipt Types

```python
from neonize.utils.enum import ReceiptType

ReceiptType.READ
ReceiptType.PLAYED
ReceiptType.SENDER
```

### Vote Types

```python
from neonize.utils.enum import VoteType

VoteType.SINGLE  # Single choice poll
VoteType.MULTIPLE  # Multiple choice poll
```

## Advanced Topics

### Custom Event Handlers

```python
from neonize.events import MessageEv
from typing import Callable

def rate_limit(max_calls: int, period: float) -> Callable:
    """Decorator to rate limit event handlers."""
    import time
    from collections import deque
    
    calls = deque()
    
    def decorator(func: Callable) -> Callable:
        def wrapper(client, event: MessageEv):
            now = time.time()
            
            # Remove old calls
            while calls and calls[0] < now - period:
                calls.popleft()
            
            if len(calls) >= max_calls:
                return  # Rate limited
            
            calls.append(now)
            return func(client, event)
        
        return wrapper
    return decorator

# Usage
@client.event
@rate_limit(max_calls=5, period=60)
def on_message(client, event: MessageEv):
    # Handle message (max 5 per minute)
    pass
```

### Middleware Pattern

```python
from typing import List, Callable

class Middleware:
    def __init__(self):
        self.middlewares: List[Callable] = []
    
    def use(self, func: Callable):
        self.middlewares.append(func)
        return func
    
    def run(self, client, event):
        for middleware in self.middlewares:
            result = middleware(client, event)
            if result is False:
                return False  # Stop processing
        return True

# Usage
middleware = Middleware()

@middleware.use
def log_messages(client, event):
    print(f"Message from {event.Info.PushName}")
    return True  # Continue

@middleware.use
def filter_spam(client, event):
    text = event.Message.conversation or ""
    if "spam" in text.lower():
        return False  # Stop processing
    return True

@client.event
def on_message(client, event: MessageEv):
    if middleware.run(client, event):
        # Process message
        pass
```

## See Also

- [User Guide](../user-guide/index.md) - Learn how to use Neonize
- [Examples](../examples/index.md) - Code examples
- [GitHub Repository](https://github.com/krypton-byte/neonize) - Source code
