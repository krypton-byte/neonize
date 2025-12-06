# Async Client

Working with Neonize's asynchronous client.

## Overview

The async client (`NewAClient`) provides full async/await support for high-performance applications.

## Quick Links

- [Getting Started](quickstart.md) - Start with async client
- [Event Handling](events.md) - Async event handlers
- [Best Practices](best-practices.md) - Async patterns and tips

## Basic Usage

```python
import asyncio
from neonize.aioze.client import NewAClient
from neonize.aioze.events import MessageEv, ConnectedEv

async def main():
    client = NewAClient("async_bot")
    
    @client.event
    async def on_connected(client: NewAClient, event: ConnectedEv):
        print("✅ Connected!")
    
    @client.event
    async def on_message(client: NewAClient, event: MessageEv):
        text = event.Message.conversation
        if text == "ping":
            await client.reply_message("pong!", event)
    
    await client.connect()

asyncio.run(main())
```

## When to Use Async

Use async client when you need:

- **High concurrency** - Handle many connections simultaneously
- **Non-blocking I/O** - Don't block on network operations
- **Integration** - Work with async frameworks (FastAPI, aiohttp)
- **Performance** - Maximum throughput

## Async vs Sync

| Feature | Async Client | Sync Client |
|---------|-------------|-------------|
| Performance | ⚡ Higher | 🐌 Lower |
| Concurrency | ✅ Excellent | ⚠️ Limited |
| Complexity | 🔴 Higher | 🟢 Lower |
| Best For | Production | Prototyping |

## Next Steps

Continue to:

- [Async Quick Start](quickstart.md) - Build your first async bot
- [Async Events](events.md) - Handle events asynchronously
- [Best Practices](best-practices.md) - Write efficient async code
