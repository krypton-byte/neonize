# JID and Addressing

Every participant in WhatsApp — users, groups, channels, the status
broadcast — is addressed by a **JID** (Jabber ID). In Neonize, `JID` is a
protobuf message (`neonize.proto.Neonize_pb2.JID`) with three fields:

| Field | Description | Example |
| --- | --- | --- |
| `User` | Local part: phone number digits or group/channel id | `"628123456789"`, `"120363021212345678"` |
| `Server` | Domain that scopes the user part | `"s.whatsapp.net"`, `"g.us"`, `"newsletter"` |
| `Agent` / `Device` | Specific linked device of a user (rarely needed) | `0`, `1` |

## Common Server Values

| Server | Meaning |
| --- | --- |
| `s.whatsapp.net` | Individual user (phone number) |
| `g.us` | Group chat |
| `newsletter` | Channel (newsletter) |
| `broadcast` | Status broadcast and broadcast lists |
| `lid` | Layered identity — an alternate per-chat identity for privacy |

## Building JIDs

```python
from neonize.utils import build_jid

user = build_jid("628123456789")                          # s.whatsapp.net by default
group = build_jid("120363021212345678", server="g.us")    # group
channel = build_jid("12349999", server="newsletter")      # channel
```

Most APIs accept a `JID`. To extract a plain phone number back out:

```python
phone = jid.User                       # "628123456789"
```

## Phone Numbers vs LIDs

WhatsApp increasingly uses **LIDs** (layered IDs): within a given chat, a
participant may be identified by an opaque id under the `lid` server instead
of their phone-number JID. Neonize provides conversions:

```python
lid = client.get_lid_from_pn(user_jid)   # phone JID -> LID
pn = client.get_pn_from_lid(lid)         # LID -> phone JID
```

!!! tip "When this matters"
    Some operations (mentions, poll votes, receipts inside certain groups)
    must use whichever identifier the incoming event carried. When a message
    arrives, prefer `event.Info.MessageSource.Sender` as-is rather than
    reconstructing a JID from the raw phone number.

## Extracting JIDs from Events

Never build addresses from strings when you can copy them from the event:

```python
chat = ev.Info.MessageSource.Chat       # where to reply
sender = ev.Info.MessageSource.Sender   # who actually sent it
```

In groups `Chat` is the group JID while `Sender` is the member's JID; in
direct chats both are the same user.

## Device Metadata

For advanced flows (e.g. sender-key distribution), `get_user_devices`
returns all linked devices of a user:

```python
devices = client.get_user_devices(user_jid)
```

See [API Reference: Sync Client](../api-reference/client.md) for the full
signature.
