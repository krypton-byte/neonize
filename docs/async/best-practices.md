# Async Best Practices

## Never Block the Loop

Every `await client.*` call is non-blocking, but your own code may not be.
Common offenders inside handlers:

| Blocking call | Replace with |
| --- | --- |
| `time.sleep()` | `await asyncio.sleep()` |
| `requests.get()` | `aiohttp` / `httpx.AsyncClient` |
| Heavy CPU work | `asyncio.to_thread(...)` or an executor |
| Sync SQLite writes | keep them short, or offload |

## One Event Loop

The Go core starts its own background thread; Neonize bridges callbacks
into the loop running at connect time. Do not create multiple event loops
in one process for the same factory.

```python
# Correct: single entry point
if __name__ == "__main__":
    asyncio.run(main())
```

## Graceful Shutdown

Install a signal handler that schedules `stop()` on the loop instead of
killing the process mid-write:

```python
import asyncio, signal

def interrupted(*_):
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(factory.stop(), loop)

signal.signal(signal.SIGINT, interrupted)
```

This lets pending sends finish and the SQLite store close cleanly.

## Backpressure

WhatsApp can deliver bursts (history sync after reconnect). If handlers do
slow I/O per message, queue internally instead of processing inline:

```python
queue: asyncio.Queue[MessageEv] = asyncio.Queue(maxsize=1000)

@client.event(MessageEv)
async def on_message(client, ev):
    queue.put_nowait(ev)

async def worker():
    while True:
        ev = await queue.get()
        await process(ev)
```

## Session Hygiene

- One UUID per logical bot; never reuse a UUID across processes running in
  parallel (the session will be taken over — you will see
  `StreamReplacedEv`).
- Copy the database file only while clients are stopped.

## Testing Bots

Inject events by calling handlers directly with constructed payloads — no
network required:

```python
import asyncio
from neonize.aioze.events import MessageEv

def fake_event(text: str) -> MessageEv:
    ...  # build a minimal Message protobuf

asyncio.run(on_message(client, fake_event("ping")))
```

## Checklist

- [ ] All WhatsApp calls awaited; blocking helpers wrapped
- [ ] Signal handler calls `factory.stop()`
- [ ] Per-client state keyed by UUID
- [ ] Burst handling via internal queues where needed
- [ ] Database backups taken while stopped
