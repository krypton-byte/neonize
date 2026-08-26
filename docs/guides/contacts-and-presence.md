# Contacts and Presence

## Checking Registration

Before messaging a number, verify it is on WhatsApp:

```python
from neonize.utils import build_jid

results = client.is_on_whatsapp([build_jid("628123456789")])
if results[0].IsIn:
    ...
```

Raises `IsOnWhatsAppError` when the check fails at protocol level.

## User Info

```python
info = client.get_user_info(user_jid)   # business profile, status, picture metadata
```

Raises `GetUserInfoError` on failure.

## Profile Pictures

```python
pic = client.get_profile_picture(chat)          # URL of the current picture
```

Picture changes arrive as `PictureEv`.

## Local Contact Store

The `ContactStore` persists contacts in SQLite:

```python
all_contacts = client.contact.get_all_contacts()
```

## Presence

### Your presence

```python
from neonize.utils.enum import Presence

client.send_presence(Presence.AVAILABLE)    # online
client.send_presence(Presence.UNAVAILABLE)  # offline
```

### Per-chat typing indicators

```python
from neonize.utils.enum import ChatPresence, ChatPresenceMedia

client.send_chat_presence(chat, ChatPresence.COMPOSING, ChatPresenceMedia.TEXT)
client.send_chat_presence(chat, ChatPresence.PAUSED, ChatPresenceMedia.TEXT)
```

Incoming indicators arrive as `ChatPresenceEv`.

### Subscribing to a contact's presence

```python
client.subscribe_presence(user_jid)
```

After subscribing, presence updates for that user arrive as `PresenceEv`.

## Privacy Settings

```python
settings = client.get_privacy_settings()     # current values
```

Change one value:

```python
from neonize.proto.waAdv.WAAdv_pb2 import PrivacySettingType
from neonize.utils.enum import ...           # value enums per setting

client.set_privacy_setting(PrivacySettingType.LAST_SEEN, value)
```

Changes (including ones made from the phone) arrive as `PrivacySettingsEv`.

Status-privacy readers:

```python
for entry in client.get_status_privacy():
    print(entry)
```

## Blocking

```python
blocklist = client.get_blocklist()

from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import BlocklistAction

client.update_blocklist(user_jid, BlocklistAction.BLOCK)
client.update_blocklist(user_jid, BlocklistAction.UNBLOCK)
```

Blocklist changes arrive as `BlocklistEv` / `BlocklistChangeEv`.

## Own Profile

```python
me = client.get_me()
client.set_profile_name("My Bot")
client.set_profile_photo("avatar.png")
client.set_status_message("Building with Neonize")
```

## Business Links

```python
target = client.resolve_business_message_link("https://wa.me/c/...")
qr_target = client.resolve_contact_qr_link("ABCD-1234")
link = client.get_contact_qr_link()      # generate your own QR link
```

## Calls

Reject an incoming call so it rings neither side:

```python
from neonize.events import CallOfferEv

@client.event(CallOfferEv)
def on_call(client: NewClient, ev: CallOfferEv) -> None:
    client.reject_call(ev.Call.From, ev.Info.ID)
```
