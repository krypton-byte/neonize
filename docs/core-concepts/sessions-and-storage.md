# Sessions and Storage

Neonize persists state in two places. Knowing which is which makes backup,
reset and multi-session setups straightforward.

## Session Database (SQLite)

The `name` argument of the client constructor is a SQLite path holding the
linked-device session: identity keys, registration data, and protocol state.

```python
client = NewClient("session.db")
```

- Created automatically on first run.
- Reused on every subsequent run — no re-pairing.
- One file can hold **multiple independent sessions**, keyed by UUID.

### Multiple sessions in one database

```python
support = NewClient("sessions.db", uuid="support-bot")
sales = NewClient("sessions.db", uuid="sales-bot")
```

Each client resumes only its own session. Without an explicit UUID, the
**first** stored session is resumed; pass `new_device=True` together with a
`uuid` to force pairing a brand-new device even when sessions already exist:

```python
extra = NewClient("sessions.db", uuid="third-bot", new_device=True)
```

## Python-Side Stores

Two stores live alongside the session, scoped per client UUID:

### ContactStore (`client.contact`)

Persistent contact records populated from your own code and from syncs.

```python
contacts = client.contact.get_all_contacts()
```

### ChatSettingsStore (`client.chat_settings`)

Per-chat settings that survive restarts: mute timers, pin and archive flags.

```python
from datetime import timedelta

client.chat_settings.put_muted_until(chat, timedelta(hours=1))
client.chat_settings.put_pinned(chat, True)
client.chat_settings.put_archived(chat, False)

settings = client.chat_settings.get_chat_settings(chat)
```

## Backup and Reset

| Task | How |
| --- | --- |
| Back up sessions | Stop the bot, copy the SQLite file while idle |
| Move to another machine | Copy the SQLite file — the session travels with it |
| Start over for one session | `client.logout()` then delete the file if no other sessions live there |
| Invalidate everything | Delete the SQLite file |

!!! warning "Session files are credentials"
    Anyone with the SQLite file can act as the linked device. Protect it
    like a private key; do not commit it to version control.

## What Lives Where

| Data | Location | Survives logout? |
| --- | --- | --- |
| Device keys / registration | Go core's SQLite store | No |
| Contact records | `ContactStore` | Yes (file remains) |
| Chat mute/pin/archive | `ChatSettingsStore` | Yes |
| Media cache | Not persisted by Neonize | n/a |
