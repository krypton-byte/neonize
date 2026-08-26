# Async Bot

The asyncio equivalent of the basic bot: identical command surface, but
every client call is awaited and handlers are coroutines.

Source embedded from
[`examples/async_basic.py`](https://github.com/krypton-byte/neonize/blob/master/examples/async_basic.py).

```bash
python examples/async_basic.py
```

```python
--8<-- "examples/async_basic.py"
```

## Notes

- Handlers registered with `@client.event` must be `async def`.
- The event loop runs the WhatsApp dispatch; blocking work belongs in
  `asyncio.to_thread` — see [Async Best Practices](../async/best-practices.md).
- For several sessions in one process, prefer
  [ClientFactory](../async/index.md#multi-session-with-clientfactory).
