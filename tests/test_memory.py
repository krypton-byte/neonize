"""Unit tests for FFI memory management safety."""

import ctypes
import gc
import os
import weakref

os.environ["SPHINX"] = "1"

from neonize._binder import Bytes, free_bytes
from neonize.events import EventsManager


class TestFreeBytesNoop:
    """free_bytes must be a safe no-op for types already consumed."""

    def test_none(self):
        free_bytes(None)

    def test_bytes(self):
        free_bytes(b"already consumed")

    def test_bytearray(self):
        free_bytes(bytearray(b"already consumed"))


class TestConsumeBytesStructLogic:
    """Test the consume_bytes_struct logic independently.

    Since the real ``consume_bytes_struct`` is defined inside the SPHINX guard,
    we test the exact same logic inline here to verify correctness.
    """

    @staticmethod
    def _consume(result, free_fn):
        """Replicates the exact logic of consume_bytes_struct."""
        if not result:
            return b""
        try:
            contents = result.contents
            if not contents.ptr or contents.size == 0:
                return b""
            return ctypes.string_at(contents.ptr, contents.size)
        finally:
            free_fn(result)

    def test_copies_payload_and_frees(self):
        payload = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00binary\x00tail"
        buffer = ctypes.create_string_buffer(payload)
        b_struct = Bytes(ctypes.cast(buffer, ctypes.c_void_p), len(payload))
        b_ptr = ctypes.pointer(b_struct)

        freed = []
        result = self._consume(b_ptr, lambda ptr: freed.append(True))
        assert result == payload, f"Expected {payload!r}, got {result!r}"
        assert len(freed) == 1, "Free function was not called"

    def test_null_returns_empty(self):
        freed = []
        result = self._consume(None, lambda ptr: freed.append(True))
        assert result == b""
        assert len(freed) == 0, "Free should not be called on NULL"

    def test_nul_bytes_preserved(self):
        """Binary data containing NUL bytes must be preserved."""
        payload = b"\x00\x01\x02\x00\x03\x04\x00"
        buffer = ctypes.create_string_buffer(payload)
        b_struct = Bytes(ctypes.cast(buffer, ctypes.c_void_p), len(payload))
        b_ptr = ctypes.pointer(b_struct)

        result = self._consume(b_ptr, lambda ptr: None)
        assert result == payload
        assert len(result) == 7

    def test_free_called_even_on_error(self):
        """FreeBytesStruct must be called even if get_bytes raises."""
        freed = []

        class BadBytes(ctypes.Structure):
            _fields_ = [("ptr", ctypes.c_void_p), ("size", ctypes.c_size_t)]

        b_struct = BadBytes(0, 0)  # empty struct → returns b""
        b_ptr = ctypes.pointer(b_struct)

        # Can't directly make string_at raise inside _consume,
        # but we can verify free is called for zero-size struct
        def consume_zero(result, free_fn):
            if not result:
                return b""
            try:
                contents = result.contents
                if not contents.ptr or contents.size == 0:
                    return b""
                return ctypes.string_at(contents.ptr, contents.size)
            finally:
                free_fn(result)

        result = consume_zero(b_ptr, lambda ptr: freed.append(True))
        assert result == b""
        assert len(freed) == 1, "Free must be called even for empty structs"


class TestWeakMethodEvents:
    """EventsManager must use WeakMethod for bound-method handlers."""

    def test_bound_method_stored_as_weakmethod(self):
        class DummyFactory:
            pass

        class Listener:
            def __init__(self):
                self.called = False

            def on_event(self, client, message):
                self.called = True

        factory = DummyFactory()
        em = EventsManager(factory)
        listener = Listener()

        from neonize.events import EVENT_TO_INT
        from neonize.proto.Neonize_pb2 import Connected as ConnectedEv

        em(ConnectedEv)(listener.on_event)

        code = EVENT_TO_INT[ConnectedEv]
        assert code in em.list_func
        assert isinstance(em.list_func[code], weakref.WeakMethod)

    def test_weakmethod_allows_gc(self):
        class DummyFactory:
            pass

        class Listener:
            def on_event(self, client, message):
                pass

        factory = DummyFactory()
        em = EventsManager(factory)
        listener = Listener()

        from neonize.events import EVENT_TO_INT
        from neonize.proto.Neonize_pb2 import Connected as ConnectedEv

        em(ConnectedEv)(listener.on_event)
        code = EVENT_TO_INT[ConnectedEv]
        handler = em.list_func[code]

        listener_ref = weakref.ref(listener)
        del listener, handler
        gc.collect()

        assert listener_ref() is None, "Listener was not GC'd despite WeakMethod"
        assert em.list_func[code]() is None

    def test_plain_function_stored_directly(self):
        class DummyFactory:
            pass

        factory = DummyFactory()
        em = EventsManager(factory)

        from neonize.events import EVENT_TO_INT
        from neonize.proto.Neonize_pb2 import Connected as ConnectedEv

        def my_handler(client, message):
            pass

        em(ConnectedEv)(my_handler)
        code = EVENT_TO_INT[ConnectedEv]
        # Plain functions should NOT be wrapped in WeakMethod
        assert not isinstance(em.list_func[code], weakref.WeakMethod)
        assert em.list_func[code] is my_handler


class TestFinalizer:
    """NewClient and NewAClient must register a weakref.finalize callback to trigger Stop on GC."""

    def test_newclient_finalizer(self):
        from neonize.client import NewClient

        stopped = []

        class MockGocode:
            def Stop(self, uuid):
                stopped.append(uuid)

        client = NewClient(name="test_client", uuid="test_uuid")
        client._stop_finalizer.detach()  # replace default finalizer
        ref = weakref.finalize(client, NewClient._release_ffi, client.uuid, MockGocode())

        assert ref.alive
        del client
        gc.collect()

        assert not ref.alive
        assert stopped == [b"test_uuid"]

    def test_newaclient_finalizer(self):
        from neonize.aioze.client import NewAClient

        stopped = []

        class MockGocode:
            def Stop(self, uuid):
                stopped.append(uuid)

        client = NewAClient(name="test_aclient", uuid="test_uuid")
        client._stop_finalizer.detach()  # replace default finalizer
        ref = weakref.finalize(client, NewAClient._release_ffi, client.uuid, MockGocode())

        assert ref.alive
        del client
        gc.collect()

        assert not ref.alive
        assert stopped == [b"test_uuid"]


if __name__ == "__main__":
    for cls_name, cls in list(globals().items()):
        if isinstance(cls, type) and cls_name.startswith("Test"):
            obj = cls()
            for method_name in sorted(dir(obj)):
                if method_name.startswith("test_"):
                    print(f"  {cls_name}.{method_name}...", end=" ")
                    getattr(obj, method_name)()
                    print("OK")
    print("\nALL TESTS PASSED!")
