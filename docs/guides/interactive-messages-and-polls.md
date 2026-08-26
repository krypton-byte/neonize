# Interactive Messages and Polls

## Polls

### Creating a poll

```python
from neonize.utils.enum import VoteType

msg = client.build_poll_vote_creation(
    "Lunch?",                     # poll question
    ["Pizza", "Burger", "Sushi"], # options (2-12)
    VoteType.SINGLE,              # or VoteType.MULTIPLE
)
client.send_message(chat, msg)
```

Raises `BuildPollVoteCreationError` for invalid configurations.

### Voting in a poll

```python
# Given a received poll message:
vote = client.build_poll_vote(poll_message_info, ["Pizza"])
client.send_message(chat, vote)
```

`build_poll_vote` encrypts the selection with the poll's message secret.

### Reading incoming votes

Poll votes arrive as `MessageEv` with a `pollVoteMessage` payload; decrypt
the selected options with:

```python
selected = client.decrypt_poll_vote(original_poll_msg, vote_msg)
```

## Reactions

```python
reaction = client.build_reaction(chat, sender_jid, message_id, reaction="👍")
client.send_message(chat, reaction)
```

## Interactive Buttons

The `neonize.ext.interactive_message` module provides typed builders that
produce `CustomInteractiveMessage` payloads accepted by
`send_interactive_message`.

### Quick replies and URL buttons

```python
from neonize.ext.interactive_message import (
    ButtonMessage,
    ReplyButton,
    UrlButton,
)

message = ButtonMessage(
    title="Daily Report",
    body="Choose an action",
    footer="Neonize bot",
    buttons=[
        ReplyButton(display_text="Send report"),
        UrlButton(display_text="Dashboard", url="https://example.com"),
    ],
)
client.send_interactive_message(chat, message)
```

Available button types: `ReplyButton`, `UrlButton`, `CallButton`,
`CopyButton`, `LocationButton`, `AddressButton`, `ReminderButton`,
`CancelReminderButton`.

### List selection

```python
from neonize.ext.interactive_message import (
    ButtonMessage, Row, Section, SelectionButton,
)

message = ButtonMessage(
    title="Settings",
    body="Pick an option",
    buttons=[
        SelectionButton(
            title="Options",
            sections=[
                Section(
                    title="General",
                    rows=[
                        Row(title="Language", description="Change language"),
                        Row(title="Theme", description="Light or dark"),
                    ],
                )
            ],
        )
    ],
)
client.send_interactive_message(chat, message)
```

### Carousel

`CarouselMessage` lays out cards with images — see the module reference via
[API Utilities](../api-reference/utils.md) or the source at
`neonize/ext/interactive_message/`.

## Raw Protocol Access

For flows the builders do not cover yet, compose the protobuf directly and
send it as a plain message:

```python
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import (
    FutureProofMessage, InteractiveMessage, Message, MessageContextInfo,
)

payload = Message(
    viewOnceMessage=FutureProofMessage(
        message=Message(
            interactiveMessage=InteractiveMessage(
                body=InteractiveMessage.Body(text="Body"),
                footer=InteractiveMessage.Footer(text="Footer"),
                nativeFlowMessage=InteractiveMessage.NativeFlowMessage(
                    buttons=[
                        InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                            name="quick_reply",
                            buttonParamsJSON='{"display_text":"Tap","id":"1"}',
                        )
                    ]
                ),
            )
        )
    )
)
client.send_message(chat, payload)
```

!!! note "Fragility"
    Raw interactive payloads depend on undocumented WhatsApp internals.
    Prefer the ext builders; fall back to raw protobuf only when needed.
