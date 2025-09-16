<div align="center">
<img src="assets/neonize.png" width="30%">

# 🚀 Neonize

### *WhatsApp Automation Made Simple for Python*

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://golang.org)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](LICENSE)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://whatsapp.com/)
[![Release](https://img.shields.io/github/v/release/krypton-byte/neonize?style=for-the-badge)](https://github.com/krypton-byte/neonize/releases)

*A powerful Python library built on top of [Whatsmeow](https://github.com/tulir/whatsmeow) - enabling seamless WhatsApp automation with enterprise-grade performance*

---

[Getting Started](#-getting-started) • [Features](#-features) • [Examples](#-examples) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

<img src="assets/20250607_2254_Futuristic WhatsApp Backend Visualization_simple_compose_01jx5hh659f7bvbqxc8gedz8r8.png" width="100%" alt="Neonize"/>

## ✨ What is Neonize?

**Neonize** is a cutting-edge Python library that transforms WhatsApp automation from complex to simple. Built on top of the robust [Whatsmeow](https://github.com/tulir/whatsmeow) Go library, it delivers enterprise-grade performance with Python's ease of use and developer-friendly API.

### 🎯 Why Choose Neonize?

- **🔥 High Performance** - Built with Go backend for maximum speed and efficiency
- **🐍 Python Native** - Seamless integration with your existing Python ecosystem
- **🛡️ Enterprise Ready** - Production-tested with robust error handling and reliability
- **⚡ Real-time** - Handle messages, media, and events in real-time with async support
- **🔧 Easy Integration** - Simple, intuitive API design for rapid development
- **📚 Well Documented** - Comprehensive documentation with practical examples

---

## 🌟 Features

### Core Messaging
- ✅ Send and receive text messages
- ✅ Handle media files (images, videos, documents, audio)
- ✅ Group management and operations
- ✅ Real-time message events
- ✅ Message receipts and status tracking

### Advanced Capabilities
- 🔐 End-to-end encryption support
- 🎯 Contact and user information retrieval
- 📞 Call event handling
- 🔔 Presence and typing indicators
- 📊 Polls and interactive messages
- 🚫 Blocklist management

### Developer Experience
- 🔄 Event-driven architecture
- 📊 Built-in logging and debugging
- 🗄️ SQLite and PostgreSQL database support
- ⚡ Both synchronous and asynchronous APIs
- 🧪 Comprehensive examples and documentation

## 💎 Sponsors

We are grateful to our sponsors who help make Neonize possible. Their support enables us to continue developing and maintaining this open-source project for the community.

<!-- sponsors --><a href="https://github.com/OwlFeedMe"><img src="https:&#x2F;&#x2F;github.com&#x2F;OwlFeedMe.png" width="60px" alt="User avatar: FeedMe" /></a><!-- sponsors -->

### 🤝 Become a Sponsor

Your sponsorship helps us:
- ⚡ Maintain and improve Neonize
- 🐛 Fix bugs and add new features
- 📚 Create better documentation
- 🔧 Provide community support
- 🚀 Keep the project free and open-source

**[Become a Sponsor →](https://github.com/sponsors/krypton-byte)**

*Thank you to all our sponsors for believing in Neonize and supporting open-source development! 🙏*

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Go 1.19+ (for building from source)

### Installation

```bash
pip install neonize
```

### Quick Start

```python
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, event

# Initialize client
client = NewClient("your_bot_name")

@client.event
def on_connected(client: NewClient, event: ConnectedEv):
    print("🎉 Bot connected successfully!")

@client.event  
def on_message(client: NewClient, event: MessageEv):
    if event.message.conversation == "hi":
        client.reply_message("Hello! 👋", event.message)

# Start the bot
client.connect()
event.wait()  # Keep running
```

### Async Version

```python
import asyncio
from neonize.aioze.client import NewAClient
from neonize.aioze.events import MessageEv, ConnectedEv

async def main():
    client = NewAClient("async_bot")
    
    @client.event
    async def on_message(client: NewAClient, event: MessageEv):
        if event.message.conversation == "ping":
            await client.reply_message("pong! 🏓", event.message)
    
    await client.connect()

asyncio.run(main())
```

## 💡 Examples

### 📱 Basic Client Setup

```python
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, event
import logging

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)

# Initialize the WhatsApp client
client = NewClient(
    name="my-whatsapp-bot",
    database="./neonize.db"
)

# Handle successful connection
@client.event
def on_connected(client: NewClient, event: ConnectedEv):
    print("🎉 Successfully connected to WhatsApp!")
    print(f"📱 Device: {event.device}")

# Start the client
client.connect()
event.wait()
```

### 💬 Sending Messages

```python
from neonize.utils import build_jid

# Send simple text message
jid = build_jid("1234567890")
client.send_message(jid, text="Hello from Neonize! 🚀")

# Send image with caption
with open("image.jpg", "rb") as f:
    image_data = f.read()

image_msg = client.build_image_message(
    image_data,
    caption="Check out this amazing image! 📸",
    mime_type="image/jpeg"
)
client.send_message(jid, message=image_msg)

# Send document file
with open("document.pdf", "rb") as f:
    doc_data = f.read()

doc_msg = client.build_document_message(
    doc_data,
    filename="document.pdf",
    caption="Here is the document you requested",
    mime_type="application/pdf"
)
client.send_message(jid, message=doc_msg)
```

### 🎭 Message Event Handling

```python
from neonize.events import MessageEv, ReceiptEv, PresenceEv
from datetime import datetime

# Handle incoming text messages
@client.event
def on_message(client: NewClient, event: MessageEv):
    message_text = event.message.conversation
    sender_jid = event.info.message_source.sender
    chat_jid = event.info.message_source.chat
    
    print(f"📨 Received from {sender_jid}: {message_text}")
    
    # Auto-reply functionality
    if message_text and message_text.lower() == "hello":
        client.send_message(chat_jid, text="Hello there! 👋")
    elif message_text and message_text.lower() == "help":
        help_text = """
🤖 *Bot Commands:*
• hello - Get a greeting
• help - Show this help message
• time - Get current time
• joke - Get a random joke
"""
        client.send_message(chat_jid, text=help_text)
    elif message_text and message_text.lower() == "time":
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client.send_message(chat_jid, text=f"🕐 Current time: {current_time}")

# Handle message receipts (delivery status)
@client.event
def on_receipt(client: NewClient, event: ReceiptEv):
    print(f"📧 Message {event.receipt.type}: {event.message_ids}")

# Handle typing indicators
@client.event
def on_presence(client: NewClient, event: PresenceEv):
    chat = event.message_source.chat
    participant = event.message_source.sender
    print(f"💬 {participant} is {event.presence} in {chat}")
```

### 👥 Group Management

```python
from neonize.utils import build_jid

# Create a new group
participants = [
    build_jid("1234567890"),
    build_jid("0987654321"),
]

group_info = client.create_group(
    "My Awesome Group 🚀",
    participants
)
print(f"🎉 Group created: {group_info.jid}")

# Get group information
group_info = client.get_group_info(group_jid)
print(f"📋 Group Name: {group_info.group_name}")
print(f"📝 Description: {group_info.group_desc}")
print(f"👥 Participants: {len(group_info.participants)}")

# Add participants to group
client.update_group_participants(
    group_jid,
    [user_jid],
    "add"
)

# Remove participants from group
client.update_group_participants(
    group_jid,
    [user_jid],
    "remove"
)

# Update group name
client.update_group_name(
    group_jid,
    "New Group Name 🎯"
)

# Update group description
client.update_group_description(
    group_jid,
    "This is our updated group description"
)
```

### 🔍 Contact & Profile Management

```python
# Get user profile information
profile = client.get_profile_picture(
    user_jid,
    full_resolution=True
)
print(f"👤 Profile picture URL: {profile.url}")
print(f"🆔 Profile ID: {profile.id}")

# Update your own status
client.set_presence("available")
print("✅ Status updated to available")

# Check if contacts are on WhatsApp
contacts = ["1234567890", "0987654321", "1122334455"]
registered_contacts = client.is_on_whatsapp(contacts)

for contact in registered_contacts:
    if contact.is_in:
        print(f"✅ {contact.jid} is on WhatsApp")
    else:
        print(f"❌ {contact.query} is not on WhatsApp")
```

### 📊 Polls & Interactive Messages

```python
from neonize.utils.enum import VoteType

# Create a poll
poll_msg = client.build_poll_vote_creation(
    "What's your favorite programming language?",
    ["Python 🐍", "Go 🚀", "JavaScript 💛", "Rust 🦀"],
    VoteType.SINGLE_SELECT
)
client.send_message(chat_jid, message=poll_msg)

# Handle poll responses
@client.event
def on_poll_vote(client: NewClient, event):
    voter = event.info.message_source.sender
    selected_options = event.message.poll_update_message.vote.selected_options
    print(f"📊 {voter} voted for: {selected_options}")
```

## 🏗️ Project Structure

```
neonize/
├── examples/
│   ├── async_basic.py
│   ├── basic.py
│   ├── multisession_async.py
│   ├── multisession.py
│   └── paircode.py
├── goneonize/
│   ├── build_python_proto.py
│   ├── chat_settings_store.go
│   ├── contact_store.go
│   ├── go.mod
│   ├── go.sum
│   ├── main.go
│   └── defproto/
├── neonize/
│   ├── __init__.py
│   ├── client.py
│   ├── events.py
│   ├── types.py
│   ├── aioze/          # Async client
│   ├── proto/          # Protocol buffers
│   └── utils/          # Helper utilities
├── docs/
│   ├── conf.py
│   ├── index.rst
│   └── getstarted.rst
└── tools/              # Build and development tools
```

## 📖 Documentation

### Core Classes

- **[`NewClient`](neonize/client.py)** - Main synchronous WhatsApp client
- **[`NewAClient`](neonize/aioze/client.py)** - Asynchronous WhatsApp client
- **[Event System](neonize/events.py)** - Event handling and types
- **[Protocol Buffers](neonize/proto/)** - WhatsApp message definitions
- **[Utilities](neonize/utils/)** - Helper functions and enums

### Event System

The event system in Neonize is built around decorators and type-safe events:

```python
# Synchronous event handling
@client.event
def on_message(client: NewClient, event: MessageEv):
    handle_message(event)

@client.event
def on_receipt(client: NewClient, event: ReceiptEv):
    handle_receipt(event)

# Asynchronous event handling
@async_client.event
async def on_message(client: NewAClient, event: MessageEv):
    await handle_message_async(event)
```

### Database Support

Neonize supports multiple database backends for storing session data:

```python
# SQLite (default)
client = NewClient("bot_name", database="./app.db")

# PostgreSQL (recommended for production)
client = NewClient("bot_name", database="postgres://user:pass@localhost/dbname")

# In-memory (for testing)
client = NewClient("bot_name", database=":memory:")
```

### Multi-Session Support

Handle multiple WhatsApp accounts simultaneously:

```python
from neonize.client import NewClient
import threading

# Create multiple clients
clients = []
for i in range(3):
    client = NewClient(f"bot_{i}", database=f"./bot_{i}.db")
    clients.append(client)

# Start all clients in separate threads
threads = []
for client in clients:
    thread = threading.Thread(target=client.connect)
    thread.start()
    threads.append(thread)

# Wait for all threads
for thread in threads:
    thread.join()
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/krypton-byte/neonize.git
cd neonize

# Install dependencies with Poetry
poetry install --with dev

# Or install with pip in development mode
pip install -e .

# Run the basic example
python examples/basic.py

# Run tests
python -m pytest

# Build documentation
cd docs && make html
```

### Code Standards

- Follow **PEP 8** for Python code style
- Use **type hints** for better code documentation
- Write **comprehensive tests** for new features
- Update **documentation** for API changes
- Ensure **backward compatibility** when possible

## 🗄️ Database Configuration

### SQLite (Default)

Perfect for development and small-scale deployments:

```python
client = NewClient("my_bot", database="./whatsapp.db")
```

### PostgreSQL (Production Recommended)

For high-performance and scalable applications:

```python
# Basic connection
client = NewClient("my_bot", database="postgres://username:password@localhost:5432/dbname")

# With SSL disabled
client = NewClient("my_bot", database="postgres://username:password@localhost:5432/dbname?sslmode=disable")

# With SSL required
client = NewClient("my_bot", database="postgres://username:password@localhost:5432/dbname?sslmode=require")
```

### Connection Pool Settings

For production applications, configure connection pooling:

```python
database_url = "postgres://user:pass@localhost:5432/neonize?pool_min_conns=5&pool_max_conns=20"
client = NewClient("production_bot", database=database_url)
```

## 🚀 Quick Integration

### With FastAPI

```python
from fastapi import FastAPI
from neonize.aioze.client import NewAClient
from neonize.aioze.events import MessageEv

app = FastAPI()
whatsapp_client = NewAClient("fastapi_bot")

@app.on_event("startup")
async def startup_event():
    await whatsapp_client.connect()

@whatsapp_client.event
async def on_message(client: NewAClient, event: MessageEv):
    # Handle WhatsApp messages in your FastAPI app
    if event.message.conversation == "/api_status":
        await client.reply_message("API is running! ✅", event.message)

@app.get("/send-message")
async def send_message(phone: str, message: str):
    jid = build_jid(phone)
    await whatsapp_client.send_message(jid, text=message)
    return {"status": "sent"}
```

### With Django

```python
# apps.py
from django.apps import AppConfig
from neonize.client import NewClient
import threading

class WhatsAppConfig(AppConfig):
    name = 'whatsapp_integration'
    
    def ready(self):
        self.whatsapp_client = NewClient("django_bot")
        thread = threading.Thread(target=self.whatsapp_client.connect)
        thread.daemon = True
        thread.start()
```

### With Flask

```python
from flask import Flask, request, jsonify
from neonize.client import NewClient
import threading

app = Flask(__name__)
whatsapp_client = NewClient("flask_bot")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    phone = data.get('phone')
    message = data.get('message')
    
    if phone and message:
        jid = build_jid(phone)
        whatsapp_client.send_message(jid, text=message)
        return jsonify({"status": "success"})
    
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    # Start WhatsApp client in background
    thread = threading.Thread(target=whatsapp_client.connect)
    thread.daemon = True
    thread.start()
    
    app.run(debug=True)
```

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Whatsmeow](https://github.com/tulir/whatsmeow)** - The powerful Go library that powers Neonize
- **[Thundra](https://github.com/krypton-byte/thundra)** - Companion library for easy bot creation
- **Python Community** - For the amazing ecosystem and support
- **Contributors** - All the developers who have contributed to this project

## 📞 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/krypton-byte/neonize/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/krypton-byte/neonize/discussions)
- 📚 **Documentation**: [Full Documentation](https://neonize.readthedocs.io/)
- 🔗 **Related Projects**: [Thundra Framework](https://github.com/krypton-byte/thundra)

## 🌟 Related Projects

- **[Thundra](https://github.com/krypton-byte/thundra)** - High-level bot framework built on Neonize
- **[Neonize Dart](https://github.com/krypton-byte/neonize-dart)** - Dart/Flutter wrapper for Neonize
- **[Whatsmeow](https://github.com/tulir/whatsmeow)** - Go WhatsApp Web API library

---

<div align="center">

**Made with ❤️ for the Python community**

*If this project helped you, please consider giving it a ⭐ on GitHub!*

</div>
