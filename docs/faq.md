# FAQ

## Installation and Startup

### ImportError: dynamic module does not define module init

You are importing the bundled Go shared library as a Python module. It is
not a Python extension — import `neonize` normally; the binder loads the
binary itself.

### UnsupportedPlatform at import

No prebuilt binary matches your OS/architecture pair. Check the platform
table on the [home page](index.md#platform-support) or build from source —
see [Building from Source](development/building.md).

### FFmpeg errors when sending stickers

Install FFmpeg (see [Installation](getting-started/installation.md#install-ffmpeg)).
Text-only bots do not need it.

## Authentication

### The QR code does not appear

The QR prints only when the session database has no stored device. If you
expect a fresh pairing, use `new_device=True` with a `uuid`, or delete the
database file.

### Can I run two bots with one database?

Yes — give each a distinct `uuid`. See
[Sessions and Storage](core-concepts/sessions-and-storage.md).

### My bot disconnects and shows StreamReplacedEv

Another process (or machine) resumed the same session and took it over.
Never run two processes against one UUID simultaneously.

## Messaging

### Why does my handler not fire for group messages?

Check filters: status broadcasts arrive under the `broadcast` server, and
your own outgoing messages echo back as `MessageEv` too. Filter both early.

### How do I get the sender's phone number in a group?

Use `ev.Info.MessageSource.Sender.User`. In some chats WhatsApp provides a
LID instead — convert with `get_pn_from_lid` when needed.

### Mentions do not highlight anyone

Provide `ghost_mentions=` with the same numbers written as `@<number>` in
the text, and set `mentions_are_lids=True` in LID chats.

## Media

### download_any returns bytes but I want a file

Pass a destination path:
`client.download_any(ev.Message, "downloads/file.jpg")`.

### Upload fails for large files

WhatsApp caps media sizes (roughly 16 MB images/audio, 100 MB video).
Oversized payloads raise `UploadError`.

## Operations

### How often should I expect reconnects?

whatsmeow reconnects automatically. Watch `KeepAliveTimeoutEv` /
`KeepAliveRestoredEv` for transient outages and `DisconnectedEv` for longer
drops.

### Is Neonize safe to run behind Docker?

Yes. Persist the SQLite file in a volume, keep the container single-process
per session set, and install FFmpeg in the image if media features are
used. See [Sessions and Storage](core-concepts/sessions-and-storage.md).

### Where are the docs for method X?

[API Reference](api-reference/index.md) renders every public signature from
source. If something looks missing there, it is private by design.
