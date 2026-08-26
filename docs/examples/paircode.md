# Pairing by Phone Number

Pair a device without scanning a QR code. `PairPhone` returns an
8-character code that you type into the linked-device dialog on the phone.

```python
from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv
from neonize.proto.waCommon_pb2 import ClientName

client = NewClient("session.db")

@client.event(ConnectedEv)
def on_connected(client: NewClient, _: ConnectedEv) -> None:
    print("Connected")

if __name__ == "__main__":
    code = client.PairPhone(
        "628123456789",                  # international format, digits only
        show_push_notification=True,
        client_name=ClientName.LINUX,
    )
    print(f"Enter this code in WhatsApp: {code}")
    client.connect()                     # completes pairing with the code
```

## Steps

1. Run the script.
2. On the phone open **Settings > Linked Devices > Link a Device**.
3. Choose **Link with phone number instead**.
4. Type the printed code.

The session is stored like any QR pairing; subsequent runs connect without
prompting.

## Notes

- `show_push_notification=True` raises a notification on the target phone.
- The code expires after a short window; rerun to get a fresh one.
- The same flow exists on the async client:
  `await client.PairPhone(...)`.
