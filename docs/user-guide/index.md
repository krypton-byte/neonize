# User Guide

Welcome to the comprehensive Neonize user guide. This section covers all the features and capabilities of Neonize in detail.

## What You'll Learn

This guide is organized into the following sections:

### Core Functionality

- **[Client Configuration](client-configuration.md)** - Learn how to configure and customize your WhatsApp client
- **[Sending Messages](sending-messages.md)** - Send text, media, and interactive messages
- **[Receiving Messages](receiving-messages.md)** - Handle incoming messages and media
- **[Event System](event-system.md)** - Work with Neonize's event-driven architecture

### Media and Content

- **[Media Handling](media-handling.md)** - Send and receive images, videos, audio, and documents
- **[Advanced Features](advanced-features.md)** - Polls, reactions, stickers, and more

### WhatsApp Features

- **[Group Management](group-management.md)** - Create and manage WhatsApp groups
- **[Contact Management](contact-management.md)** - Manage contacts and user information
- **[Newsletter/Channel](newsletter.md)** - Work with WhatsApp newsletters and channels

## Quick Navigation

<div class="grid cards" markdown>

-   :material-cog:{ .lg .middle } **Configuration**

    ---

    Set up databases, logging, and client properties

    [:octicons-arrow-right-24: Client Configuration](client-configuration.md)

-   :material-message-text:{ .lg .middle } **Messaging**

    ---

    Send and receive all types of messages

    [:octicons-arrow-right-24: Sending Messages](sending-messages.md)

-   :material-lightning-bolt:{ .lg .middle } **Events**

    ---

    Handle real-time events from WhatsApp

    [:octicons-arrow-right-24: Event System](event-system.md)

-   :material-account-group:{ .lg .middle } **Groups**

    ---

    Create and manage WhatsApp groups

    [:octicons-arrow-right-24: Group Management](group-management.md)

</div>

## Prerequisites

Before diving into this guide, make sure you have:

- ✅ Installed Neonize ([Installation Guide](../getting-started/installation.md))
- ✅ Completed the Quick Start ([Quick Start](../getting-started/quickstart.md))
- ✅ Successfully authenticated ([Authentication](../getting-started/authentication.md))

## Code Examples

Throughout this guide, you'll find practical code examples. All examples assume you have a basic client setup:

```python
from neonize.client import NewClient
from neonize.events import event

client = NewClient("my_bot")
client.connect()
event.wait()
```

For async examples:

```python
import asyncio
from neonize.aioze.client import NewAClient

client = NewAClient("async_bot")

# register event handlers on client.event here...

async def main():
    await client.connect()  # captures the running event loop
    await client.idle()     # keeps the bot alive

asyncio.run(main())  # ✅ standard entry point
```

## Best Practices

Throughout this guide, we'll highlight best practices with special callouts:

!!! tip "Performance Tip"
    Use async clients for high-throughput applications

!!! warning "Important"
    Be aware of WhatsApp rate limits to avoid temporary bans

!!! info "Information"
    Additional context and helpful information

!!! example "Example"
    Practical code examples demonstrating concepts

## Getting Help

If you need help while following this guide:

- 📚 Check the [API Reference](../api-reference/index.md) for detailed method documentation
- 💡 Browse [Examples](../examples/index.md) for complete working code
- ❓ Visit the [FAQ](../faq.md) for common questions
- 🐛 Report issues on [GitHub](https://github.com/krypton-byte/neonize/issues)

## Next Steps

Ready to dive in? Start with:

1. [Client Configuration](client-configuration.md) - Set up your client properly
2. [Event System](event-system.md) - Understand event handling
3. [Sending Messages](sending-messages.md) - Start sending messages

Let's get started! 🚀
