# Async Client (`NewAClient`)

The asyncio mirror of the sync client. Every method listed in
[Sync Client](client.md) exists here as a coroutine with the same name,
parameters and return values — `await` it instead of calling it.

```python
from neonize.aioze.client import NewAClient

client = NewAClient("session.db")
await client.connect()
```

## JID Helper

The async client uses the same `_ensure_jid` helper as the sync client.
Phone-number strings passed to `send_message` are auto-wrapped:

::: neonize.aioze.client._ensure_jid

## Constructor

::: neonize.aioze.client.NewAClient
    options:
      members:
        - __init__
        - connect
        - connect_with_proxy
        - disconnect
        - stop
        - idle
        - logout

!!! note "Method reference"
    To keep this page and the sync page from drifting apart, per-method
    signatures are documented once in [Sync Client](client.md). The async
    client adds no parameters; it only changes call semantics to coroutines.

## ClientFactory

Manages multiple `NewAClient` sessions over one SQLite database, with
factory-wide event dispatch.

```python
from neonize.aioze.client import ClientFactory

factory = ClientFactory("sessions.db")
```

::: neonize.aioze.client.ClientFactory
    options:
      members:
        - __init__
        - new_client
        - get_all_devices
        - event
        - idle_all
        - stop

## Example: Factory in Production

See the complete runnable version in
[examples/multi-session](../examples/multi-session.md).
