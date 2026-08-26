# Basic Bot

A complete synchronous bot exercising most of the client surface: text
commands, media sends, stickers, reactions, polls, chat settings and
newsletter operations.

The source below is embedded directly from
[`examples/basic.py`](https://github.com/krypton-byte/neonize/blob/master/examples/basic.py)
in this repository, so it always matches the released code.

## Running

```bash
python examples/basic.py
```

Pair with the printed QR code, then send any of the commands handled in the
`match text:` block (for example `ping`, `_image`, `_sticker`, `poll_vote`).

## Source

```python
--8<-- "examples/basic.py"
```

## Highlights

| Command | Demonstrates |
| --- | --- |
| `ping` | `reply_message` |
| `_test_link_preview` | Link previews in `send_message` |
| `_sticker_exif` | Stickers with pack metadata |
| `viewonce` | View-once images |
| `read` | Batch mark-read with receipts |
| `poll_vote` | Poll creation with `VoteType.SINGLE` |
| `send_react` | Reactions via `build_reaction` |
| `edit_message` | Progressive message editing |
| `put_*` | Persistent chat settings (`ChatSettingsStore`) |
| `button` | Raw interactive protobuf payloads |

## Related Pages

- [Sending Messages](../guides/sending-messages.md)
- [Media Handling](../guides/media-handling.md)
- [Interactive Messages and Polls](../guides/interactive-messages-and-polls.md)
