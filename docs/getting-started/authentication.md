# Authentication

Learn how to authenticate your WhatsApp account with Neonize using different methods.

## Authentication Methods

Neonize supports two primary authentication methods:

1. **QR Code Authentication** - Scan QR code with your phone
2. **Pairing Code Authentication** - Enter a pairing code on your phone

## QR Code Authentication

This is the default and simplest authentication method.

### Basic QR Code Login

```python
from neonize.client import NewClient
from neonize.events import ConnectedEv, event

client = NewClient("my_bot")

@client.event
def on_connected(client: NewClient, event: ConnectedEv):
    print("✅ Successfully authenticated!")

client.connect()
event.wait()
```

When you run this code:

1. A QR code will be displayed in your terminal
2. Open WhatsApp on your phone
3. Go to **Settings** → **Linked Devices**
4. Tap **Link a Device**
5. Scan the displayed QR code

### Custom QR Code Handler

You can customize how the QR code is displayed:

```python
import segno
from neonize.client import NewClient
from neonize.events import event

client = NewClient("my_bot")

# Custom QR code handler
@client.qr
def on_qr_code(client: NewClient, qr_data: bytes):
    print("📱 Scan this QR code with your WhatsApp:")
    # Display QR code in terminal
    segno.make_qr(qr_data).terminal(compact=True)
    
    # Or save to file
    segno.make_qr(qr_data).save("qr_code.png", scale=10)
    print("QR code saved to qr_code.png")

client.connect()
event.wait()
```

### QR Code for Web Applications

For web applications, you can generate a QR code image:

```python
import base64
from io import BytesIO
import segno

@client.qr
def on_qr_code(client: NewClient, qr_data: bytes):
    # Create QR code image
    buffer = BytesIO()
    segno.make_qr(qr_data).save(buffer, kind='png', scale=10)
    
    # Convert to base64 for embedding in HTML
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Now you can send this to your web frontend
    print(f"data:image/png;base64,{qr_base64}")
```

## Pairing Code Authentication

Pairing codes provide an alternative authentication method without QR codes.

### Basic Pairing Code

```python
from neonize.client import NewClient
from neonize.events import PairStatusEv, event

client = NewClient("my_bot")

@client.event
def on_pair_status(client: NewClient, event: PairStatusEv):
    if event.ID.User:
        print(f"✅ Logged in as: {event.ID.User}")

# Request pairing code for your phone number
pairing_code = client.pair_phone(
    "1234567890",  # Your phone number (without + or country code)
    show_push_notification=True
)

print(f"🔑 Your pairing code: {pairing_code}")
print("Enter this code in WhatsApp → Linked Devices → Link with phone number")

client.connect()
event.wait()
```

### Pairing Code with Custom Callback

```python
from neonize.client import NewClient
from neonize.events import event

client = NewClient("my_bot")

@client.paircode
def on_pair_code(client: NewClient, code: str, connected: bool):
    if not connected:
        print(f"🔑 Your pairing code: {code}")
        print("Enter this code in WhatsApp:")
        print("1. Open WhatsApp on your phone")
        print("2. Go to Settings → Linked Devices")
        print("3. Tap 'Link a Device'")
        print("4. Choose 'Link with phone number'")
        print(f"5. Enter: {code}")
    else:
        print("✅ Device successfully paired!")

# Request pairing code
client.pair_phone("1234567890", show_push_notification=True)
client.connect()
event.wait()
```

### International Phone Numbers

For international numbers, include the country code:

```python
# US number
client.pair_phone("1234567890")  # Country code 1 is implied

# UK number
client.pair_phone("447123456789")  # Include country code

# India number
client.pair_phone("919876543210")  # Include country code
```

## Session Management

### Understanding Sessions

When you authenticate, Neonize stores session data in a database file. This allows you to reconnect without re-authenticating.

```python
# Session stored in my_bot.db (SQLite)
client = NewClient("my_bot")

# Custom database path
client = NewClient("my_bot", database="./sessions/my_bot.db")

# PostgreSQL database
client = NewClient(
    "my_bot",
    database="postgresql://user:pass@localhost/whatsapp"
)
```

### Multiple Sessions

You can manage multiple WhatsApp accounts:

```python
# Bot 1
client1 = NewClient("bot_1", database="./sessions/bot1.db")

# Bot 2
client2 = NewClient("bot_2", database="./sessions/bot2.db")

# Each maintains its own session
```

### Logout and Re-authentication

To logout and clear the session:

```python
from neonize.client import NewClient

client = NewClient("my_bot")

# Logout (clears session)
client.logout()

# Next time you connect, you'll need to authenticate again
```

## Device Information

Customize how your bot appears in WhatsApp:

```python
from neonize.client import NewClient
from neonize.proto.waCompanionReg.WAWebProtobufsCompanionReg_pb2 import DeviceProps
from neonize.utils.enum import ClientType

# Create custom device properties
device_props = DeviceProps(
    os="Neonize Bot",
    version=DeviceProps.AppVersion(
        primary=0,
        secondary=1,
        tertiary=0,
    ),
    platformType=DeviceProps.PlatformType.CHROME,
    requireFullSync=False,
)

client = NewClient("my_bot", props=device_props)
```

## Security Best Practices

### Protecting Session Data

1. **Never commit session files to version control**

```gitignore
# .gitignore
*.db
sessions/
```

2. **Use environment variables for sensitive data**

```python
import os

DATABASE_URL = os.getenv("WHATSAPP_DB_URL", "./bot.db")
client = NewClient("bot", database=DATABASE_URL)
```

3. **Secure file permissions**

```bash
# Linux/macOS
chmod 600 bot.db
```

### Production Deployment

For production environments:

```python
import os
from neonize.client import NewClient

# Use PostgreSQL for production
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:pass@localhost:5432/whatsapp"
)

client = NewClient("production_bot", database=DATABASE_URL)
```

## Troubleshooting Authentication

### QR Code Not Displaying

If the QR code doesn't display in your terminal:

```python
import segno

@client.qr
def on_qr_code(client: NewClient, qr_data: bytes):
    # Save to file instead
    segno.make_qr(qr_data).save("qr_code.png", scale=10)
    print("QR code saved to qr_code.png - scan with WhatsApp")
```

### Pairing Code Not Working

Common issues:

1. **Wrong phone number format** - Remove spaces, dashes, and the + symbol
2. **Code expired** - Pairing codes expire after a few minutes
3. **Already linked** - Unlink old devices first

```python
# Correct format
client.pair_phone("1234567890")  # ✅

# Incorrect formats
client.pair_phone("+1 234-567-890")  # ❌
client.pair_phone("(123) 456-7890")  # ❌
```

### Connection Issues

If you can't connect:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

client = NewClient("my_bot")
client.connect()
```

### Session Corrupted

If your session is corrupted:

```python
import os

# Delete the session file
if os.path.exists("my_bot.db"):
    os.remove("my_bot.db")

# Re-authenticate
client = NewClient("my_bot")
client.connect()
```

## Next Steps

Now that you understand authentication, learn more about:

- [Event System](../user-guide/event-system.md) - Handle WhatsApp events
- [Sending Messages](../user-guide/sending-messages.md) - Send messages and media
- [Client Configuration](../user-guide/client-configuration.md) - Advanced client setup

!!! info "Session Persistence"
    Once authenticated, your session persists across restarts. You only need to authenticate once per session/device.

!!! warning "Account Security"
    - Never share your session database file
    - Use strong passwords for PostgreSQL databases
    - Regularly monitor linked devices in WhatsApp settings
