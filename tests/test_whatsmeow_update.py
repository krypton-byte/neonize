from neonize.aioze.events import RotateADVSecretEv as AioRotateADVSecretEv
from neonize.events import EVENT_TO_INT, INT_TO_EVENT, RotateADVSecretEv
from neonize.proto.Neonize_pb2 import JID, MessageDebugTimings, RotateADVSecret, SendResponse


def test_send_response_has_sender_and_chat():
    sender = JID(
        User="1234567890",
        RawAgent=0,
        Device=0,
        Integrator=0,
        Server="s.whatsapp.net",
    )
    chat = JID(
        User="9876543210",
        RawAgent=0,
        Device=0,
        Integrator=0,
        Server="s.whatsapp.net",
    )
    timings = MessageDebugTimings(
        Queue=0,
        Marshal=0,
        GetParticipants=0,
        GetDevices=0,
        GroupEncrypt=0,
        PeerEncrypt=0,
        Send=0,
        Resp=0,
        Retry=0,
    )
    resp = SendResponse(
        Timestamp=1700000000,
        ID="ABCDEF123456",
        ServerID=12345,
        DebugTimings=timings,
        Sender=sender,
        Chat=chat,
    )
    serialized = resp.SerializeToString()
    deserialized = SendResponse.FromString(serialized)

    assert deserialized.ID == "ABCDEF123456"
    assert deserialized.Sender.User == "1234567890"
    assert deserialized.Chat.User == "9876543210"


def test_rotate_adv_secret_event():
    assert EVENT_TO_INT[RotateADVSecretEv] == 45
    assert INT_TO_EVENT[45] is RotateADVSecretEv
    assert AioRotateADVSecretEv is RotateADVSecretEv

    rot = RotateADVSecret(OldSecret="old_sec_key", NewSecret="new_sec_key")
    data = rot.SerializeToString()
    parsed = RotateADVSecret.FromString(data)
    assert parsed.OldSecret == "old_sec_key"
    assert parsed.NewSecret == "new_sec_key"


def test_pair_phone_without_connect_raises_clean_error(tmp_path):
    import os

    import pytest

    if os.environ.get("SPHINX"):
        pytest.skip("Skipping live CGO call in SPHINX mock mode")

    from neonize.client import NewClient
    from neonize.exc import PairPhoneError

    db_path = str(tmp_path / "session.db")
    c = NewClient(db_path)
    with pytest.raises(PairPhoneError, match="client is nil"):
        c.PairPhone("1234567890", True)
