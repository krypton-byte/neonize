# Utilities

`neonize.utils` bundles JID helpers, protocol enums, media tooling and
logging.

## JID Helpers

::: neonize.utils.build_jid
    options:
      members: false

::: neonize.utils.Jid2String
    options:
      members: false

::: neonize.utils.JIDToNonAD
    options:
      members: false

```python
from neonize.utils import build_jid, Jid2String

jid = build_jid("628123456789")            # -> JID(User="628123456789", Server="s.whatsapp.net")
text = Jid2String(jid)
```

## Message Helpers

::: neonize.utils.message.extract_text
    options:
      members: false

::: neonize.utils.message.get_message_type
    options:
      members: false

```python
from neonize import extract_text
from neonize.utils import get_message_type

text = extract_text(ev.Message)     # "" if no text field
msg_type = get_message_type(ev.Message)  # e.g. ImageMessage, str for conversation
```

## Media Helpers

::: neonize.utils.get_bytes_from_name_or_url
    options:
      members: false

::: neonize.utils.save_file_to_temp_directory
    options:
      members: false

::: neonize.utils.ffmpeg.check_ffmpeg_available
    options:
      members: false

::: neonize.utils.FFmpeg
    options:
      members: false

## Enums (`neonize.utils.enum`)

The protocol enumerations used across client methods:

| Enum | Values (typical) | Used by |
| --- | --- | --- |
| `ReceiptType` | `DELIVERED`, `READ`, `PLAYED` | `mark_read` |
| `Presence` | `AVAILABLE`, `UNAVAILABLE` | `send_presence` |
| `ChatPresence` / `ChatPresenceMedia` | `COMPOSING`, `PAUSED`; `TEXT`, `AUDIO` | `send_chat_presence` |
| `VoteType` | single/multiple selectable count | Polls |
| `MediaType` | Photo, Video, Audio, Document | `upload` |
| `BlocklistAction` | block/unblock | `update_blocklist` |
| `ClientName` / `ClientType` | platform branding | `PairPhone` |
| `ParticipantChange` / `ParticipantRequestChange` | add/remove/promote/demote | Group participants |

```python
from neonize.utils.enum import ReceiptType, Presence, VoteType
```

## Number Parsing

Phone-number helpers are re-exported from the
[`phonenumbers`](https://pypi.org/project/phonenumbers/) library and
available directly on `neonize.utils`:

```python
from neonize.utils import format_number, parse, PhoneNumberFormat

number = parse("+62 812-3456-789")
print(format_number(number, PhoneNumberFormat.E164))
```

Link validation for WhatsApp URLs:

::: neonize.utils.validate_link
    options:
      members: false

## Logging

Two loggers are provided:

| Logger | Name | Covers |
| --- | --- | --- |
| Python side | `neonize` (via `neonize.utils.log`) | Binder, dispatcher, stores |
| Go core | `neonize.utils.log_whatsmeow` | whatsmeow protocol logs relayed over FFI |

```python
import logging
from neonize.utils import log

log.setLevel(logging.DEBUG)   # verbose protocol output
```

## Platform Detection

::: neonize.utils.platform
    options:
      members: false

Resolves the bundled shared-library filename for the running OS/arch pair;
raises the underlying `UnsupportedPlatform` error when no binary matches.
