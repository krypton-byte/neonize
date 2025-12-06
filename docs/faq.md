# Frequently Asked Questions

Common questions and answers about Neonize.

## General Questions

### What is Neonize?

Neonize is a Python library for WhatsApp automation built on top of the Whatsmeow Go library. It provides a simple, Python-native API for interacting with WhatsApp Web.

### Is Neonize free?

Yes, Neonize is completely free and open-source under the Apache 2.0 license.

### What Python versions are supported?

Neonize requires Python 3.10 or higher.

## Installation & Setup

### How do I install Neonize?

```bash
pip install neonize
```

See the [Installation Guide](getting-started/installation.md) for more details.

### Do I need to install Go?

No, pre-built binaries are included with the package. You don't need to install Go unless you're building from source.

### Why do I get "ModuleNotFoundError: No module named 'neonize'"?

Make sure you've installed Neonize in the correct Python environment:

```bash
pip list | grep neonize
```

## Authentication

### How do I authenticate with WhatsApp?

You can use either QR code or pairing code authentication. See the [Authentication Guide](getting-started/authentication.md).

### Can I use multiple WhatsApp accounts?

Yes, create separate client instances with different session names:

```python
bot1 = NewClient("account1")
bot2 = NewClient("account2")
```

### How long does my session last?

Sessions persist indefinitely unless you logout or WhatsApp revokes the session.

### My QR code won't scan, what should I do?

1. Make sure your terminal supports QR code display
2. Try saving the QR code to an image file
3. Check that your phone and computer have internet connection

## Usage & Features

### Can I send messages to unsaved numbers?

Yes, use the `build_jid` function:

```python
from neonize.utils import build_jid

recipient = build_jid("1234567890")
client.send_message(recipient, "Hello!")
```

### How do I send images/videos?

```python
client.send_image(jid, "path/to/image.jpg", caption="Caption")
client.send_video(jid, "path/to/video.mp4", caption="Caption")
```

See [Media Handling](user-guide/media-handling.md) for more details.

### Can I create WhatsApp groups?

Yes:

```python
group = client.create_group("Group Name", [jid1, jid2, jid3])
```

See [Group Management](user-guide/group-management.md).

### Does Neonize support WhatsApp Business features?

Neonize works with both regular WhatsApp and WhatsApp Business accounts.

## Performance & Limitations

### What are WhatsApp's rate limits?

WhatsApp has undocumented rate limits. To avoid bans:

- Don't send more than 20-30 messages per minute
- Implement delays between messages
- Don't spam users

### Can I use Neonize in production?

Yes, Neonize is production-ready. Use PostgreSQL for production databases:

```python
client = NewClient(
    "bot",
    database="postgresql://user:pass@localhost/db"
)
```

### How many messages can Neonize handle?

Neonize can handle thousands of messages per day. For high-volume applications, use the async client.

### Is Neonize faster than other libraries?

Yes, because it's built on the Go-based Whatsmeow library, Neonize is significantly faster than pure Python implementations.

## Errors & Troubleshooting

### I'm getting "SendMessageError", what should I do?

Common causes:

1. Invalid JID format
2. User blocked your number
3. Rate limiting

Enable debug logging to see details:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### The bot disconnects randomly

This is usually due to:

1. Poor internet connection
2. WhatsApp maintenance
3. Session issues

Implement reconnection logic:

```python
@client.event
def on_disconnected(client: NewClient, event: DisconnectedEv):
    print("Disconnected, attempting to reconnect...")
    client.connect()
```

### "Database is locked" error with SQLite

This occurs with concurrent access. Solutions:

1. Use PostgreSQL for multi-threaded applications
2. Enable WAL mode for SQLite
3. Use the async client

### FFmpeg errors when sending videos

Make sure FFmpeg is installed and in your PATH:

```bash
ffmpeg -version
```

## Database & Storage

### Can I use PostgreSQL instead of SQLite?

Yes, recommended for production:

```python
client = NewClient(
    "bot",
    database="postgresql://user:password@localhost:5432/whatsapp"
)
```

### Where is session data stored?

By default in `{session_name}.db` in the current directory. You can customize:

```python
client = NewClient("bot", database="./sessions/bot.db")
```

### How do I backup my session?

Simply backup the database file:

```bash
# SQLite
cp my_bot.db my_bot.db.backup

# PostgreSQL
pg_dump whatsapp > backup.sql
```

### Can I migrate from SQLite to PostgreSQL?

Yes, but you'll need to re-authenticate. Session data is not directly portable between database types.

## Development

### How do I contribute to Neonize?

See the [Contributing Guide](development/contributing.md).

### Where do I report bugs?

Open an issue on [GitHub](https://github.com/krypton-byte/neonize/issues).

### How do I request features?

Open a feature request on [GitHub Discussions](https://github.com/krypton-byte/neonize/discussions).

### Can I use Neonize commercially?

Yes, the Apache 2.0 license allows commercial use.

## WhatsApp Policies

### Is using Neonize against WhatsApp's Terms of Service?

WhatsApp's Terms of Service prohibit using unauthorized third-party clients. Use at your own risk and responsibility.

### Can my account get banned?

Possible if you:

- Send spam
- Violate WhatsApp's policies
- Exceed rate limits
- Use aggressive automation

To minimize risk:

- Follow WhatsApp's policies
- Implement rate limiting
- Don't spam users
- Use for personal/business communication only

### What happens if I get banned?

WhatsApp may temporarily or permanently ban your number. There's no guaranteed way to appeal.

## Comparison with Other Libraries

### Neonize vs other WhatsApp libraries?

| Feature | Neonize | Others |
|---------|---------|--------|
| Performance | ⚡ Very Fast (Go-based) | 🐌 Slower (Pure Python) |
| Async Support | ✅ Yes | ❌ Limited |
| Type Hints | ✅ Full | ⚠️ Partial |
| Documentation | ✅ Comprehensive | ⚠️ Varies |
| Protocol Buffers | ✅ Native | ❌ Manual |

### Should I migrate from library X?

Neonize offers:

- Better performance
- More features
- Active development
- Better documentation

Consider migrating if you need these benefits.

## Still Have Questions?

- 💬 Join [GitHub Discussions](https://github.com/krypton-byte/neonize/discussions)
- 🐛 Report bugs on [GitHub Issues](https://github.com/krypton-byte/neonize/issues)
- 📧 Check existing issues before creating new ones
