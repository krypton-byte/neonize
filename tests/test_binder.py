import ctypes
import os

os.environ["SPHINX"] = "1"

from neonize._binder import Bytes


def test_bytes_get_bytes_preserves_nul_bytes():
    payload = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00binary\x00tail"
    buffer = ctypes.create_string_buffer(payload)
    data = Bytes(ctypes.cast(buffer, ctypes.c_void_p), len(payload))

    assert data.get_bytes() == payload
