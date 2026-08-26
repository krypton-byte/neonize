# Multi-Session

Run several WhatsApp accounts in one process over a single SQLite database
using the async `ClientFactory`.

Source embedded from
[`examples/multisession_async.py`](https://github.com/krypton-byte/neonize/blob/master/examples/multisession_async.py).

```bash
python examples/multisession_async.py
```

--8<-- "examples/multisession_async.py"

## Key Ideas

### Resume or create

```python
factory = ClientFactory("db.sqlite3")

for device in factory.get_all_devices():   # stored sessions
    factory.new_client(device.JID)

factory.new_client(uuid="extra-bot")       # fresh pairing slot
```

### One handler set for all clients

`@factory.event(...)` receives events from every managed client; the first
handler argument identifies which client fired it.

### Lifecycle

`await factory.idle_all()` connects everything and parks; SIGINT schedules
`await factory.stop()` for a clean shutdown.

The sync variant is available in
[`examples/multisession.py`](https://github.com/krypton-byte/neonize/blob/master/examples/multisession.py).
