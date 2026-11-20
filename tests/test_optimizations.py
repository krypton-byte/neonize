"""Unit tests verifying low-level optimizations, bug fixes, and safety guards."""

import os


def test_aspect_ratio_method_preserves_ratio():
    from neonize.utils.calc import AspectRatioMethod

    assert AspectRatioMethod(1920, 1080, 512) == (512, 288)
    assert AspectRatioMethod(1080, 1920, 512) == (288, 512)
    assert AspectRatioMethod(512, 512, 512) == (512, 512)


def test_jid_to_non_ad_direct_copy():
    from neonize.proto.Neonize_pb2 import JID
    from neonize.utils.jid import JIDToNonAD

    orig = JID(
        User="628123456789",
        RawAgent=2,
        Device=15,
        Integrator=1,
        Server="s.whatsapp.net",
        IsEmpty=False,
    )
    non_ad = JIDToNonAD(orig)
    assert non_ad.User == "628123456789"
    assert non_ad.Server == "s.whatsapp.net"
    assert non_ad.Integrator == 1
    assert non_ad.RawAgent == 0
    assert non_ad.Device == 0
    assert orig.Device == 15


def test_generate_streaming_sidecar_memoryview():
    from neonize.utils.calc import generate_streaming_sidecar

    iv = b"\x01" * 16
    mac_key = b"\x02" * 32
    ciphertext = b"\x03" * (70 * 1024)
    sidecar = generate_streaming_sidecar(ciphertext, iv, mac_key)
    assert len(sidecar) == 20  # 2 chunks * 10 bytes


def test_temporary_file_secure_lifecycle():
    from neonize.utils.iofile import TemporaryFile

    with TemporaryFile(prefix="neonize_test_", touch=True) as tf:
        assert tf.path.exists()
        path = tf.path
    assert not path.exists()

    # Does not raise if already removed
    with TemporaryFile(prefix="neonize_test_", touch=False) as tf2:
        assert not tf2.path.exists()


def test_aioze_gocode_caches_attribute_wrappers():
    from neonize.aioze.client import GoCode, async_gocode

    if os.environ.get("SPHINX"):
        # Verify GoCode caches when underlying gocode resolves an attribute
        wrapper = GoCode()
        assert wrapper.execute_sync_function is GoCode.execute_sync_function
        return

    fn1 = async_gocode.GenerateMessageID
    fn2 = async_gocode.GenerateMessageID
    assert fn1 is fn2


def test_cgo_nil_client_does_not_crash(tmp_path):
    import pytest

    if os.environ.get("SPHINX"):
        pytest.skip("Skipping live CGO test in SPHINX mock mode")

    from neonize._binder import gocode
    from neonize.proto.Neonize_pb2 import JID, GetUserInfoReturnFunction

    fake_uuid = b"non-existent-uuid-0000"
    # Should return None/empty or clean error instead of segfaulting on nil client
    assert gocode.IsConnected(fake_uuid) is False
    assert gocode.IsLoggedIn(fake_uuid) is False
    assert gocode.GenerateMessageID(fake_uuid) == b""
    gocode.Disconnect(fake_uuid)
    gocode.SetForceActiveDeliveryReceipts(fake_uuid, True)

    jid_bytes = JID(
        User="123456", RawAgent=0, Device=0, Integrator=0, Server="s.whatsapp.net"
    ).SerializeToString()
    raw = gocode.GetUserInfo(fake_uuid, jid_bytes, len(jid_bytes))
    res = GetUserInfoReturnFunction.FromString(raw)
    assert "client not found" in res.Error
