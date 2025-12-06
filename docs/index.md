# Neonize Documentation

<div align="center">
  <h1>🚀 Neonize</h1>
  <p><strong>WhatsApp Automation Made Simple for Python</strong></p>
  
  <a href="https://github.com/krypton-byte/neonize">
    <img src="https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="https://pypi.org/project/neonize/">
    <img src="https://img.shields.io/pypi/v/neonize?style=for-the-badge&logo=pypi" alt="PyPI">
  </a>
  <a href="https://github.com/krypton-byte/neonize/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge" alt="License">
  </a>
</div>

---

## What is Neonize?

**Neonize** is a powerful Python library that transforms WhatsApp automation from complex to simple. Built on top of the robust [Whatsmeow](https://github.com/tulir/whatsmeow) Go library, it delivers enterprise-grade performance with Python's ease of use and developer-friendly API.

## ✨ Key Features

### Core Messaging
- ✅ **Send and receive** text messages
- ✅ **Handle media files** (images, videos, documents, audio)
- ✅ **Group management** and operations
- ✅ **Real-time message events**
- ✅ **Message receipts** and status tracking

### Advanced Capabilities
- 🔐 **End-to-end encryption** support
- 🎯 **Contact and user information** retrieval
- 📞 **Call event handling**
- 🔔 **Presence and typing indicators**
- 📊 **Polls and interactive messages**
- 🚫 **Blocklist management**
- 📢 **Newsletter/Channel support**

### Developer Experience
- 🔄 **Event-driven architecture**
- 📊 **Built-in logging** and debugging
- 🗄️ **SQLite and PostgreSQL** database support
- ⚡ Both **synchronous and asynchronous** APIs
- 🧪 **Comprehensive examples** and documentation

## Why Choose Neonize?

| Feature | Description |
|---------|-------------|
| 🔥 **High Performance** | Built with Go backend for maximum speed and efficiency |
| 🐍 **Python Native** | Seamless integration with your existing Python ecosystem |
| 🛡️ **Enterprise Ready** | Production-tested with robust error handling and reliability |
| ⚡ **Real-time** | Handle messages, media, and events in real-time with async support |
| 🔧 **Easy Integration** | Simple, intuitive API design for rapid development |
| 📚 **Well Documented** | Comprehensive documentation with practical examples |

## Quick Example

```python
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, event

# Initialize client
client = NewClient("my_bot")

@client.event
def on_connected(client: NewClient, event: ConnectedEv):
    print("🎉 Bot connected successfully!")

@client.event  
def on_message(client: NewClient, event: MessageEv):
    if event.message.conversation == "hi":
        client.reply_message("Hello! 👋", event.message)

# Start the bot
client.connect()
event.wait()
```

## What's Next?

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } **Getting Started**

    ---

    Install Neonize and create your first WhatsApp bot in minutes

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-book-open-variant:{ .lg .middle } **User Guide**

    ---

    Learn how to use Neonize features with detailed guides and examples

    [:octicons-arrow-right-24: User Guide](user-guide/index.md)

-   :material-code-braces:{ .lg .middle } **API Reference**

    ---

    Explore the complete API documentation with all available methods

    [:octicons-arrow-right-24: API Reference](api-reference/index.md)

-   :material-lightning-bolt:{ .lg .middle } **Examples**

    ---

    Browse practical examples for common use cases

    [:octicons-arrow-right-24: Examples](examples/index.md)

</div>

## Community and Support

- 📧 **Issues**: [GitHub Issues](https://github.com/krypton-byte/neonize/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/krypton-byte/neonize/discussions)
- 🌟 **Star us on GitHub**: Show your support by starring the repository

## License

Neonize is licensed under the **Apache License 2.0**. See the [LICENSE](https://github.com/krypton-byte/neonize/blob/main/LICENSE) file for details.

---

<div align="center">
  <p><strong>Made with ❤️ for the Python community</strong></p>
  <p><em>If this project helps you, please consider giving it a ⭐ on GitHub!</em></p>
</div>
