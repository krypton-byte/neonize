from __future__ import annotations
import logging

from neonize.exc import UnsupportedEvent
from .proto import Neonize_pb2 as neonize
import ctypes
from typing import TypeVar, Type, Callable, TYPE_CHECKING, Dict
from google.protobuf.message import Message

from threading import Event as EventThread
from .proto.Neonize_pb2 import (
    QR as QREv,
    PairStatus as PairStatusEv,
    Connected as ConnectedEv,
    KeepAliveTimeout as KeepAliveTimeoutEv,
    KeepAliveRestored as KeepAliveRestoredEv,
    LoggedOut as LoggedOutEv,
    StreamReplaced as StreamReplacedEv,
    TemporaryBan as TemporaryBanEv,
    ConnectFailure as ConnectFailureEv,
    ClientOutdated as ClientOutdatedEv,
    StreamError as StreamErrorEv,
    Disconnected as DisconnectedEv,
    HistorySync as HistorySyncEv,
    NewsLetterMessageMeta as NewsLetterMessageMetaEv,
    Message as MessageEv,
    Receipt as receiptEv,
    ChatPresence as ChatPresenceEv,
    Presence as PresenceEv,
    JoinedGroup as JoinedGroupEv,
    GroupInfoEvent as GroupInfoEv,
    Picture as PictureEv,
    IdentityChange as IdentityChangeEv,
    PrivacySettings as PrivacySettingsEv,
    OfflineSyncPreview as OfflineSyncPreviewEv,
    OfflineSyncCompleted as OfflineSyncCompletedEv,
    BlocklistEvent as BlocklistEv,
    BlocklistChange as BlocklistChangeEv,
    NewsletterJoin as NewsletterJoinEv,
    NewsletterLeave as NewsletterLeaveEv,
    NewsletterMuteChange as NewsletterMuteChangeEv,
    NewsletterLiveUpdate as NewsletterLiveUpdateEV


)
log = logging.getLogger(__name__)
if TYPE_CHECKING:
    from .client import NewClient
EventType = TypeVar("EventType", bound=Message)

EVENT_TO_INT: Dict[Type[Message], int] = {
    QREv: 1,
    PairStatusEv: 2,
    ConnectedEv: 3,
    KeepAliveTimeoutEv: 4,
    KeepAliveRestoredEv: 5,
    LoggedOutEv: 6,
    StreamReplacedEv: 7,
    TemporaryBanEv: 8,
    ConnectFailureEv: 9,
    ClientOutdatedEv: 10,
    StreamErrorEv: 11,
    DisconnectedEv: 12,
    HistorySyncEv: 13,
    NewsLetterMessageMetaEv: 16,
    MessageEv: 17,
    receiptEv: 18,
    ChatPresenceEv: 19,
    PresenceEv: 20,
    JoinedGroupEv: 21,
    GroupInfoEv: 22,
    PictureEv: 23,
    IdentityChangeEv: 24,
    PrivacySettingsEv: 25,
    OfflineSyncPreviewEv: 26,
    OfflineSyncCompletedEv: 27,
    BlocklistEv: 30,
    BlocklistChangeEv:31,
    NewsletterJoinEv: 32,
    NewsletterLeaveEv: 33,
    NewsletterMuteChangeEv: 34,
    NewsletterLiveUpdateEV: 35
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
        if event not in EVENT_TO_INT:
            raise UnsupportedEvent()
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
