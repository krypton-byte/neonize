# Types

Public type aliases and generics used across the client signatures.

::: neonize.types
    options:
      members:
        - MessageServerID
        - MessageWithContextInfo
        - MediaMessageType
        - TextMessageType

## MessageServerID

Server-assigned numeric identifier used by newsletters/channels. Wrap a
plain int:

```python
from neonize.types import MessageServerID

sid = MessageServerID(0)   # 0 means "from the beginning" in pagination
```

## Message Type Variables

| Type | Accepts |
| --- | --- |
| `MessageWithContextInfo` | Any protobuf message carrying context info (text, reactions, revocations, poll votes) |
| `MediaMessageType` | Image / video / audio / document / sticker message variants |
| `TextMessageType` | `conversation` and `extendedTextMessage` payloads |

These are used to type parameters such as `quoted:` in send methods — you
normally pass the whole `ev.Message` object.

## JID

`JID` is re-exported from the generated protocol module
(`neonize.proto.Neonize_pb2`). Construct via
[`build_jid`](utils.md#neonize.utils.build_jid) rather than manually.
