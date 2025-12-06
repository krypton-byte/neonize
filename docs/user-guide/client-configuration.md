# Client Configuration

Learn how to configure and customize your Neonize WhatsApp client for optimal performance.

## Basic Configuration

### Creating a Client

```python
from neonize.client import NewClient

# Basic client with default settings
client = NewClient("my_bot")

# Client with custom database
client = NewClient("my_bot", database="./sessions/bot.db")
```

## Database Configuration

### SQLite (Default)

Perfect for development and small-scale applications:

```python
from neonize.client import NewClient

# Default SQLite database
client = NewClient("bot_name")

# Custom path
client = NewClient("bot_name", database="./data/whatsapp.db")

# In-memory (for testing)
client = NewClient("bot_name", database=":memory:")
```

### PostgreSQL (Production)

Recommended for production environments:

```python
from neonize.client import NewClient

# PostgreSQL connection
client = NewClient(
    "production_bot",
    database="postgresql://username:password@localhost:5432/whatsapp"
)

# With SSL
client = NewClient(
    "production_bot",
    database="postgresql://user:pass@host:5432/db?sslmode=require"
)

# Connection pooling
database_url = "postgresql://user:pass@host:5432/db?pool_min_conns=5&pool_max_conns=20"
client = NewClient("bot", database=database_url)
```

## Device Properties

Customize how your bot appears in WhatsApp:

```python
from neonize.client import NewClient
from neonize.proto.waCompanionReg.WAWebProtobufsCompanionReg_pb2 import DeviceProps

# Custom device properties
device_props = DeviceProps(
    os="My Custom Bot",
    version=DeviceProps.AppVersion(
        primary=1,
        secondary=0,
        tertiary=0,
    ),
    platformType=DeviceProps.PlatformType.CHROME,
    requireFullSync=False,
)

client = NewClient("my_bot", props=device_props)
```

## Logging Configuration

### Enable Debug Logging

```python
import logging

# Set logging level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from neonize.client import NewClient

client = NewClient("debug_bot")
```

### Custom Logger

```python
import logging

# Create custom logger
logger = logging.getLogger('neonize')
logger.setLevel(logging.INFO)

# Add file handler
fh = logging.FileHandler('whatsapp.log')
fh.setLevel(logging.INFO)

# Add console handler
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add handlers
logger.addHandler(fh)
logger.addHandler(ch)
```

## Client Methods

### Connection Management

```python
from neonize.client import NewClient

client = NewClient("my_bot")

# Connect to WhatsApp
client.connect()

# Check connection status
if client.is_connected:
    print("Connected!")

# Check login status
if client.is_logged_in:
    print("Logged in!")

# Disconnect
client.logout()
```

### Getting Client Information

```python
# Get your own JID
me = client.get_me()
print(f"My JID: {me.JID.User}")

# Get device information
print(f"Device: {me}")
```

## Environment Variables

Use environment variables for sensitive configuration:

```python
import os
from neonize.client import NewClient

# Database URL from environment
DATABASE_URL = os.getenv("WHATSAPP_DB_URL", "sqlite:///./bot.db")

# Bot name from environment
BOT_NAME = os.getenv("BOT_NAME", "default_bot")

client = NewClient(BOT_NAME, database=DATABASE_URL)
```

### Example .env File

```bash
# .env
WHATSAPP_DB_URL=postgresql://user:pass@localhost:5432/whatsapp
BOT_NAME=production_bot
LOG_LEVEL=INFO
```

### Using python-dotenv

```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from neonize.client import NewClient

client = NewClient(
    os.getenv("BOT_NAME"),
    database=os.getenv("WHATSAPP_DB_URL")
)
```

## Configuration Best Practices

### 1. Separate Configurations by Environment

```python
import os
from neonize.client import NewClient

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    DATABASE = os.getenv("PRODUCTION_DB_URL")
    LOG_LEVEL = "WARNING"
elif ENVIRONMENT == "staging":
    DATABASE = os.getenv("STAGING_DB_URL")
    LOG_LEVEL = "INFO"
else:
    DATABASE = "./dev.db"
    LOG_LEVEL = "DEBUG"

client = NewClient("bot", database=DATABASE)
```

### 2. Use Configuration Classes

```python
from dataclasses import dataclass
from neonize.client import NewClient

@dataclass
class Config:
    bot_name: str = "my_bot"
    database_url: str = "./bot.db"
    log_level: str = "INFO"
    max_retries: int = 3

config = Config()
client = NewClient(config.bot_name, database=config.database_url)
```

### 3. Validate Configuration

```python
import os
from neonize.client import NewClient

def validate_config():
    """Validate required configuration."""
    required_vars = ["BOT_NAME", "DATABASE_URL"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"Missing required config: {', '.join(missing)}")

validate_config()

client = NewClient(
    os.getenv("BOT_NAME"),
    database=os.getenv("DATABASE_URL")
)
```

## Performance Tuning

### Connection Pooling (PostgreSQL)

```python
# Optimize PostgreSQL connection pool
database_url = (
    "postgresql://user:pass@host:5432/db"
    "?pool_min_conns=10"
    "&pool_max_conns=50"
    "&pool_timeout=30"
)

client = NewClient("bot", database=database_url)
```

### SQLite Optimization

```python
# For SQLite, use WAL mode for better concurrency
# This is handled automatically by Neonize
client = NewClient("bot", database="./bot.db")
```

## Next Steps

- [Sending Messages](sending-messages.md) - Learn to send messages
- [Event System](event-system.md) - Handle events
- [Media Handling](media-handling.md) - Work with media files
