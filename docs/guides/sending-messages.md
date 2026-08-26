# Sending Messages

All send methods accept a `JID` destination and return a `SendResponse`
containing the message ID and send timestamp.

## Text

Pass a phone number string directly — it is auto-wrapped into a JID:

```python
client.send_message("628123456789", "Hello from Neonize")
```

Or build a JID explicitly when you need a non-default server (e.g. groups):

```python
from neonize.utils import build_jid

group = build_jid("120363001234567890", "g.us")
client.send_message(group, "Hello group")
```

`send_message` also accepts a raw protobuf `Message`, which every
`build_*_message` method produces — this is how you compose advanced payloads.

### Link previews

```python
client.send_message(
    chat, "Check out https://github.com/krypton-byte/neonize", link_preview=True
)
```

### Mentions

Pass a string containing `@<number>` mentions and supply the same numbers in
`ghost_mentions`; set `mentions_are_lids=True` when the chat uses LID
identifiers (common inside groups).

```python
client.send_message(
    group_chat,
    "Ping @628123456789, please review.",
    ghost_mentions="628123456789",
)
```

## Replies

`reply_message` quotes an existing message. Pass the received `MessageEv`
payload:

```python
@client.event(MessageEv)
def on_message(client: NewClient, ev: MessageEv) -> None:
    if ev.Message.conversation == "hi":
        client.reply_message("Hello!", ev.Message)
```

Options include `to=` (override destination), `reply_privately=True`
(answer in DM instead of the group), and `link_preview`.

## Media

```python
client.send_image(chat, "photo.jpg", caption="Sunset")
client.send_video(chat, "clip.mp4", caption="Look")
client.send_audio(chat, "voice.ogg", ptt=True)          # push-to-talk
client.send_document(chat, "report.pdf", filename="Q3-report.pdf")
client.send_sticker(chat, "meme.png", name="Bot", packname="MyPack")
```

Every media method accepts local paths, bytes, or URLs — see
[Media Handling](media-handling.md).

Albums send several images/videos as one gallery message:

```python
client.send_album(chat, ["a.jpg", "b.jpg", "c.jpg"], caption="Holiday")
```

## Contacts and Location

```python
client.send_contact(chat, contact_name="Support", contact_number="628123456789")
```

## Editing and Revoking

```python
resp = client.send_message(chat, "Typo hre")
client.edit_message(chat, resp.ID, Message(conversation="Typo here"))

# Unsend for everyone:
client.revoke_message(chat, sender=bot_jid, message_id=resp.ID)
```

`build_revoke` returns the revoke as a `Message` instead of sending it
directly — useful when composing it into other payloads.

## Reactions

```python
from neonize.client import NewClient

msg = client.send_message(chat, "React to me")
client.send_message(chat, client.build_reaction(chat, bot_jid, msg.ID, reaction="👍"))
```

An empty `reaction=""` removes an existing reaction.

## Pinning Messages

```python
client.pin_message(chat, sender_jid, message_id, seconds=604800)  # 7 days
```

`seconds=0` unpins.

## Interactive Messages

For buttons, list pickers and catalog messages use
`neonize.ext.interactive_message` builders with
`send_interactive_message(to, interactive_message)` — see
[Interactive Messages and Polls](interactive-messages-and-polls.md).

## Delivery Semantics

- Methods block until WhatsApp acknowledges the message (sync client).
- A raised `SendMessageError` means the send failed; nothing was silently
  dropped.
- Incoming acknowledgements arrive later as `ReceiptEv`.
