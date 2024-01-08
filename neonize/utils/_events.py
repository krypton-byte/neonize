from __future__ import annotations
import logging
from .._binder import func_callback_bytes
from ..proto import Neonize_pb2 as neonize
import ctypes
import time
import inspect
from typing import TypeVar, Type, Callable, TYPE_CHECKING, Dict, Any, Union
from google.protobuf.message import Message

# from google._upb._message import Message as MessageUpb
from abc import abstractmethod, ABC
from threading import Event as EventThread

log = logging.getLogger(__name__)
if TYPE_CHECKING:
    from ..client import NewClient
EventType = TypeVar("EventType", bound=Message)

EVENT_TO_INT: Dict[Type[Message], int] = {
    neonize.PairStatus: 1,
    neonize.KeepAliveTimeout: 3,
    neonize.LoggedOut: 4,
    neonize.TemporaryBan: 5,
    neonize.ConnectFailure: 6,
    neonize.StreamError: 8,
    neonize.HistorySync: 10,
    neonize.NewsletterMetadata: 13,
    neonize.Message: 14,
    neonize.Receipt: 15,
    neonize.ChatPresence: 16,
    neonize.Presence: 17,
    neonize.JoinedGroup: 18,
    neonize.Picture: 19,
    neonize.IdentityChange: 20,
    neonize.PrivacySettings: 21,
    neonize.OfflineSyncPreview: 22,
    neonize.OfflineSyncCompleted: 23,
    neonize.BlocklistEvent: 26,
    neonize.BlocklistChange: 27,
    neonize.NewsletterJoin: 28,
    neonize.NewsletterLeave: 29,
    neonize.NewsletterMuteChange: 30,
    neonize.NewsletterLiveUpdate: 31,
}
INT_TO_EVENT: Dict[int, Type[Message]] = {code: ev for ev, code in EVENT_TO_INT.items()}

event = EventThread()


class Event:
    def __init__(self, client: NewClient):
        self.client = client
        self.blocking_func = self.default_blocking
        self.list_func: Dict[int, Callable[[int, int], None]] = {}

    def execute(self, binary: int, size: int, code: int):
        self.list_func[code](binary, size)

    def wrap(self, f: Callable[[NewClient, EventType], None], event: Type[EventType]):
        def serialization(binary: int, size: int):
            f(self.client, event.FromString(ctypes.string_at(binary, size)))

        return serialization

    @property
    def blocking(self):
        def block(f: Callable[[NewClient], None]):
            self.blocking_func = lambda _: f(self.client)
            return self.blocking_func

        return block

    @classmethod
    def default_blocking(cls, x):
        log.debug("blocking function called")
        event.wait()
        log.debug("function unblocked")

    def __call__(
        self, event: Type[EventType]
    ) -> Callable[[Callable[[NewClient, EventType], None]], None]:
        def callback(func: Callable[[NewClient, EventType], None]) -> None:
            wrapped_func = self.wrap(func, event)
            self.list_func.update({EVENT_TO_INT[event]: wrapped_func})

        return callback
