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
from neonize.utils.enum import MediaType

resp = client.upload_newsletter(media_bytes, MediaType.MediaImage)
```

## Publishing a Channel Story

A Channel Story is a temporary status shown around the Channel profile for up
to 24 hours. It uses a separate native WhatsApp status transport; it is not a
regular feed post sent with `send_message` and it is not a personal
`status@broadcast`. WhatsApp only accepts it when the account and Channel have
the required status-producer permission and feature rollout.

Text Story:

```python
from neonize.utils.enum import MediaType

status = client.send_newsletter_status(
    "123456789@newsletter",
    "Thanks for following our Channel!",
)
print(status.ID, status.ServerID)  # ServerID may be 0 if the echo is delayed.
```

Image, video, or audio Story:

```python
status = client.send_newsletter_status(
    "123456789@newsletter",
    media="story.jpg",  # local path, URL, or bytes
    media_type=MediaType.MediaImage,
    caption="A short update for followers",
)
```

Use `await client.send_newsletter_status(...)` with `NewAClient`. Channel
Stories require a goneonize shared library built with the Story transport; an
older binary reports that the feature is unavailable.

!!! note "One-way traffic"
    Channels do not support replies from followers. Bots interact by
    following, reading, reacting and mirroring content — not by sending
    chat messages into them.
