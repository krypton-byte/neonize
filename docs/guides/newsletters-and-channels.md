# Newsletters and Channels

Channels (newsletters) are one-to-many broadcasts. Their JIDs use the
`newsletter` server.

## Creating a Channel

```python
meta = client.create_newsletter(
    "My Channel",
    "Daily updates about automation",
    "cover.png",          # local path, bytes or URL
)
print(meta.ID)            # newsletter JID for later use
```

Raises `CreateNewsletterError` on failure.

## Resolving Channels

```python
from neonize.proto.Neonize_pb2 import NewsletterJID

# From an invite link (https://whatsapp.com/channel/<id>):
meta = client.get_newsletter_info_with_invite("https://whatsapp.com/channel/0029Va...")

# From a known JID:
meta = client.get_newsletter_info(newsletter_jid)

print(meta.ThreadMeta.MessageCount)   # message volume
```

Both raise `GetNewsletterInfoError` / `GetNewsletterInfoWithInviteError`
respectively when the channel cannot be resolved.

## Following and Unfollowing

```python
client.follow_newsletter(meta.ID)
client.unfollow_newsletter(meta.ID)
```

Membership changes also arrive as `NewsletterJoinEv` / `NewsletterLeaveEv`.

## Reading Messages

```python
from neonize.types import MessageServerID

messages = client.get_newsletter_messages(meta.ID, 10, MessageServerID(0))
for m in messages:
    print(m.Key.ID)
```

`MessageServerID(0)` means "from the beginning"; otherwise pass the server
ID of the oldest message you already have. Metadata updates arrive as
`NewsLetterMessageMetaEv`.

## Reacting

Channel reactions are keyed by server ID, not message ID:

```python
client.newsletter_send_reaction(meta.ID, MessageServerID(12345), "👍", "")
```

An empty reaction string removes it.

## Muting and Live Updates

```python
client.newsletter_toggle_mute(meta.ID, True)     # mute

# Subscribe to live message updates for this channel:
resp = client.newsletter_subscribe_live_updates(meta.ID)
```

New channel messages then arrive through the normal event stream.

Marking messages as viewed (affects read stats on other clients):

```python
client.newsletter_mark_viewed(meta.ID, [MessageServerID(12345)])
```

## Uploading to a Channel

```python
resp = client.upload_newsletter(media_bytes, MediaType.Photo, newsletter_jid)
```

!!! note "One-way traffic"
    Channels do not support replies from followers. Bots interact by
    following, reading, reacting and mirroring content — not by sending
    chat messages into them.
