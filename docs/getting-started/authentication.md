# Authentication

WhatsApp multidevice supports two linking methods. Both produce the same
result: a persistent session stored in your SQLite database.

## Method 1: QR Code (default)

Calling `client.connect()` with an empty session store prints a QR code to
the terminal. Scan it from the phone:

```python
from neonize.client import NewClient

client = NewClient("session.db")
client.connect()
```

### Custom QR handling

Pass `qrCallback` to render the QR yourself — for example in a web UI. The
callback receives the client and the raw PNG bytes of the QR image.

```python
from neonize.client import NewClient

def on_qr(client: NewClient, qr_png: bytes) -> None:
    # qr_png is a PNG-encoded QR image; serve it, save it, or print it.
    with open("qr.png", "wb") as f:
        f.write(qr_png)

client = NewClient("session.db")
client.connect()
```

!!! note "QR rotation"
    WhatsApp rotates QR codes periodically while pairing is pending. The
    callback fires again for each refresh until the code is scanned or it
    times out.

## Method 2: Phone-Number Link Code

`PairPhone` returns an 8-character code that you enter on the phone instead
of scanning anything. Useful for headless servers where showing a QR is
inconvenient.

```python
from neonize.client import NewClient
from neonize.utils.enum import ClientType
from neonize.proto.waCommon_pb2 import ClientName

client = NewClient("session.db")

code: str = client.PairPhone(
    "628123456789",          # phone number in international format, no + or spaces
    show_push_notification=True,
    client_name=ClientName.LINUX,
)
print(f"Enter this code on your phone: {code}")
```

Then on the phone: **Settings > Linked Devices > Link a Device > Link with
phone number instead**, and type the code.

## Reconnecting

Nothing special is required — construct the client with the same database
file and connect:

```python
client = NewClient("session.db")   # loads the stored session
client.connect()                   # no QR, straight to ConnectedEv
```

To resume a specific session when the database holds several, pass its JID:

```python
from neonize.utils import build_jid

client = NewClient("session.db", jid=build_jid("628123456789"))
```

## Multi-Device Sessions

One SQLite file can hold multiple linked devices, each identified by a UUID.

```python
work = NewClient("session.db", uuid="work-bot")
home = NewClient("session.db", uuid="home-bot")
```

See [Sessions and Storage](../core-concepts/sessions-and-storage.md) and the
[multi-session example](../examples/multi-session.md).

## Logging Out

`logout()` unlinks the device and clears the stored session. The next
connect will require pairing again.

```python
client.logout()
```

!!! warning "Irreversible"
    After logout the session cannot be recovered — pair again via QR or link
    code.
