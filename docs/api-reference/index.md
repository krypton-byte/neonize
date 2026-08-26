# API Reference Overview

Neonize ships two mirrored clients plus shared event, error and utility
modules. This section documents every public symbol; signatures are
extracted from the source at build time, so they always match the release.

## Modules

| Module | Contents |
| --- | --- |
| `neonize.client` | `NewClient` — synchronous client, `ClientFactory` for multi-session sync use |
| `neonize.aioze.client` | `NewAClient`, `ClientFactory` — asyncio mirror with identical methods |
| `neonize.events` / `neonize.aioze.events` | Typed event classes and the dispatcher |
| `neonize.types` | Public type aliases (`MessageServerID`, message type variables) |
| `neonize.exc` | Exception hierarchy (one class per failed operation) |
| `neonize.utils` | JID helpers, enums, FFmpeg wrapper, logging, platform detection |
| `neonize.ext.interactive_message` | Builders for buttons, lists and carousels |

## Conventions

- Destinations are `JID` protobuf objects (see
  [JID and Addressing](../core-concepts/jid-and-addressing.md)).
- Send methods return `SendResponse`; failures raise a specific exception
  from `neonize.exc`.
- Media inputs accept local paths, bytes or URLs unless stated otherwise.
- Every method's docstring lists parameters, return types and raised
  exceptions in Sphinx reST format — mkdocstrings renders them inline below.

## Pages

1. [Sync Client](client.md) — full `NewClient` reference
2. [Async Client](async-client.md) — `NewAClient` and `ClientFactory`
3. [Events](events.md) — all event types
4. [Types](types.md) — aliases and helper types
5. [Exceptions](exceptions.md) — error hierarchy
6. [Utilities](utils.md) — enums, JID helpers, media utilities
