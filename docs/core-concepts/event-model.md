# Event Model

All WhatsApp activity reaches your code as events. Events are typed classes
in `neonize.events` (sync) and `neonize.aioze.events` (async); the sets are
identical.

## Registering Handlers

```python
from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv

client = NewClient("session.db")

@client.event(ConnectedEv)
def on_connected(client: NewClient, event: ConnectedEv) -> None:
    ...

@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv) -> None:
    ...
```

Rules:

- One event type can have multiple handlers; they run in registration order.
- Handlers receive `(client, event)`.
- A handler raising an exception does not stop other handlers.

## Anatomy of MessageEv

The event you will handle most:

| Member | Type | Description |
| --- | --- | --- |
| `event.Message` | `Message` (protobuf) | Full message payload. Text lives in `.conversation` or `.extendedTextMessage.text`; media in dedicated fields |
| `event.Info.ID` | `str` | Message identifier — needed for replies, reactions, edits, mark-read |
| `event.Info.MessageSource.Chat` | `JID` | Chat where the message appeared (a user, group, or channel) |
| `event.Info.MessageSource.Sender` | `JID` | Actual sender — differs from `Chat` inside groups and channels |
| `event.Info.Timestamp` | `int` | Unix timestamp |

```python
@client.event(MessageEv)
def on_message(client: NewClient, ev: MessageEv) -> None:
    chat = ev.Info.MessageSource.Chat
    sender = ev.Info.MessageSource.Sender
    text = ev.Message.conversation or ev.Message.extendedTextMessage.text
```

## Event Catalog

### Connection lifecycle

| Event | Fired when |
| --- | --- |
| `QREv` | A pairing QR was generated or refreshed |
| `PairStatusEv` | Device pairing completed (contains the paired JID) |
| `ConnectedEv` | Session is live after connect |
| `DisconnectedEv` | Connection dropped |
| `StreamReplacedEv` | The session was taken over by another device |
| `KeepAliveTimeoutEv` / `KeepAliveRestoredEv` | Keepalive failures and recovery |
| `ClientOutdatedEv` | Protocol version too old for the server |
| `LoggedOutEv` | Device was unlinked remotely |

### Messaging

| Event | Fired when |
| --- | --- |
| `MessageEv` | Any new message |
| `UndecryptableMessageEv` | Message arrived that this client cannot decrypt |
| `ReceiptEv` | Delivery/read receipts for previously sent messages |
| `ChatPresenceEv` | Typing indicators (`composing` / `paused`) |
| `IdentityChangeEv` | A contact's safety-number identity changed |

### Groups

| Event | Fired when |
| --- | --- |
| `GroupInfoEv` | Group metadata changed (name, topic, photo, settings) |
| `JoinedGroupEv` | This account was added to a group (carries `Sender`/`SenderPN`: who added the bot) |
| `PictureEv` | A profile or group picture changed |

### Newsletters / channels

| Event | Fired when |
| --- | --- |
| `NewsletterJoinEv` / `NewsletterLeaveEv` | Channel membership changes |
| `NewsletterMuteChangeEv` | Channel mute state changed |
| `NewsLetterMessageMetaEv` | Channel message metadata updates (views, reactions) |

### Calls

| Event | Fired when |
| --- | --- |
| `CallOfferEv` | Incoming call offer (respond with `reject_call`) |
| `CallAcceptEv`, `CallPreAcceptEv`, `CallOfferNoticeEv`, `CallTerminateEv`, `CallTransportEv` | Call negotiation lifecycle |

### Privacy, sync and errors

| Event | Fired when |
| --- | --- |
| `PrivacySettingsEv` | A privacy setting of this account changed |
| `BlocklistEv` / `BlocklistChangeEv` | Blocklist updated |
| `HistorySyncEv` | History sync batch arrived |
| `OfflineSyncPreviewEv` / `OfflineSyncCompletedEv` | Offline message replay progress |
| `ConnectFailureEv`, `StreamErrorEv`, `TemporaryBanEv` | Failure conditions requiring attention |

## Dispatch Internals

The dispatcher is built from the Go core's callbacks: each native callback
converts raw protobuf bytes into typed Python objects and fans them out to
registered handlers. Custom events can be dispatched manually by
instantiating `neonize.events.event` subclasses — see
`neonize.events.Event` in the [API reference](../api-reference/events.md).
