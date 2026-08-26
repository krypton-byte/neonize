# Client Configuration

## Constructor Options

```python
from neonize.client import NewClient

client = NewClient(
    "session.db",          # SQLite session path
    jid=None,              # resume a specific stored session
    props=None,            # DeviceProps protobuf (device branding)
    uuid=None,             # session key when several share one database
    new_device=False,      # force pairing a fresh device for this uuid
)
```

## Connecting Through a Proxy

Route the WhatsApp WebSocket through an HTTP/SOCKS proxy:

```python
from neonize.utils import ProxySettings   # configure per your deployment

client.connect_with_proxy(proxy_settings)
```

A proxy can also be changed at runtime with `set_proxy_address`, and the
current address read back:

```python
client.set_proxy_address("socks5://127.0.0.1:1080")
```

## Disappearing Messages

Set the default timer applied to new chats, or per chat:

```python
from datetime import timedelta

client.set_default_disappearing_timer(timedelta(days=7))  # account default
client.set_disappearing_timer(chat_jid, timedelta(hours=24))  # one chat
```

`timedelta(0)` disables the timer. Raises `SetDisappearingTimerError` /
`SetDefaultDisappearingTimerError`.

## Delivery Receipts

Force delivery receipts even while offline syncing:

```python
client.set_force_activate_delivery_receipts(True)
```

Useful for bots that must not miss message acknowledgement windows.

## Passive Mode

Suppress outgoing presence and receipt traffic (useful for archive-only
listeners):

```python
client.set_passive(True)
```

## Stopping

| Method | Behavior |
| --- | --- |
| `disconnect()` | Drop the connection; session stays valid |
| `stop()` | Disconnect and stop background workers |
| `logout()` | Unlink the device and clear the session |

For the async client, prefer `await client.stop()` or the shared
`ClientFactory.stop()` — see [Async Best Practices](../async/best-practices.md).

## Message Retry Control

When a message cannot be decrypted, Neonize participates in WhatsApp's
retry protocol. Override the handler to customize behavior:

```python
custom = client.get_message_for_retry(msg_bytes, source)   # inspect/replace payload
```

## Runtime Introspection

```python
me = client.get_me()               # own JID and profile info
version = client.generate_message_id()  # helper for custom flows
```
