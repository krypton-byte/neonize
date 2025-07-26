from __future__ import annotations

import ctypes
import logging
from threading import Event as EventThread
from typing import TYPE_CHECKING, Callable, Dict, Type, TypeVar

import segno
from google.protobuf.message import Message

from neonize.exc import UnsupportedEvent

from .proto.Neonize_pb2 import QR as QREv
from .proto.Neonize_pb2 import BlocklistChange as BlocklistChangeEv
from .proto.Neonize_pb2 import BlocklistEvent as BlocklistEv
from .proto.Neonize_pb2 import CallAccept as CallAcceptEv
from .proto.Neonize_pb2 import CallOffer as CallOfferEv
from .proto.Neonize_pb2 import CallOfferNotice as CallOfferNoticeEv
from .proto.Neonize_pb2 import CallPreAccept as CallPreAcceptEv
from .proto.Neonize_pb2 import CallRelayLatency as CallRelayLatencyEV
from .proto.Neonize_pb2 import CallTerminate as CallTerminateEv
from .proto.Neonize_pb2 import CallTransport as CallTransportEv
from .proto.Neonize_pb2 import ChatPresence as ChatPresenceEv
from .proto.Neonize_pb2 import ClientOutdated as ClientOutdatedEv
from .proto.Neonize_pb2 import Connected as ConnectedEv
from .proto.Neonize_pb2 import ConnectFailure as ConnectFailureEv
from .proto.Neonize_pb2 import Device
from .proto.Neonize_pb2 import Disconnected as DisconnectedEv
from .proto.Neonize_pb2 import GroupInfoEvent as GroupInfoEv
from .proto.Neonize_pb2 import HistorySync as HistorySyncEv
from .proto.Neonize_pb2 import IdentityChange as IdentityChangeEv
from .proto.Neonize_pb2 import JoinedGroup as JoinedGroupEv
from .proto.Neonize_pb2 import KeepAliveRestored as KeepAliveRestoredEv
from .proto.Neonize_pb2 import KeepAliveTimeout as KeepAliveTimeoutEv
from .proto.Neonize_pb2 import LoggedOut as LoggedOutEv
from .proto.Neonize_pb2 import Message as MessageEv
from .proto.Neonize_pb2 import NewsletterJoin as NewsletterJoinEv
from .proto.Neonize_pb2 import NewsletterLeave as NewsletterLeaveEv
from .proto.Neonize_pb2 import NewsletterLiveUpdate as NewsletterLiveUpdateEV
from .proto.Neonize_pb2 import NewsLetterMessageMeta as NewsLetterMessageMetaEv
from .proto.Neonize_pb2 import NewsletterMuteChange as NewsletterMuteChangeEv
from .proto.Neonize_pb2 import OfflineSyncCompleted as OfflineSyncCompletedEv
from .proto.Neonize_pb2 import OfflineSyncPreview as OfflineSyncPreviewEv
from .proto.Neonize_pb2 import PairStatus as PairStatusEv
from .proto.Neonize_pb2 import Picture as PictureEv
from .proto.Neonize_pb2 import Presence as PresenceEv
from .proto.Neonize_pb2 import Receipt as ReceiptEv
from .proto.Neonize_pb2 import StreamError as StreamErrorEv
from .proto.Neonize_pb2 import StreamReplaced as StreamReplacedEv
from .proto.Neonize_pb2 import TemporaryBan as TemporaryBanEv
from .proto.Neonize_pb2 import UndecryptableMessage as UndecryptableMessageEv
from .proto.Neonize_pb2 import UnknownCallEvent as UnknownCallEventEV
from .proto.Neonize_pb2 import privacySettingsEvent as PrivacySettingsEv

log = logging.getLogger(__name__)
if TYPE_CHECKING:
    from .client import ClientFactory, NewClient
EventType = TypeVar("EventType", bound=Message)
EVENT_TO_INT: Dict[Type[Message], int] = {
    Device: 0,
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
    ReceiptEv: 18,
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
    BlocklistChangeEv: 31,
    NewsletterJoinEv: 32,
    NewsletterLeaveEv: 33,
    NewsletterMuteChangeEv: 34,
    NewsletterLiveUpdateEV: 35,
    CallOfferEv: 36,
    CallAcceptEv: 37,
    CallPreAcceptEv: 38,
    CallTransportEv: 39,
    CallOfferNoticeEv: 40,
    CallRelayLatencyEV: 41,
    CallTerminateEv: 42,
    UnknownCallEventEV: 43,
    UndecryptableMessageEv: 44,
}
INT_TO_EVENT: Dict[int, Type[Message]] = {code: ev for ev, code in EVENT_TO_INT.items()}

event = EventThread()


class EventsManager:
    def __init__(self, client_factory: ClientFactory):
        self.client_factory = client_factory
        self.list_func: Dict[int, Callable[[NewClient, Message], None]] = {}

    def __call__(
        self, event: Type[EventType]
    ) -> Callable[[Callable[[NewClient, EventType], None]], None]:
        """
        Registers a callback function for a specific event type.

        :param event: The type of event to register the callback for.
        :type event: Type[EventType]
        :return: A decorator that registers the callback function.
        :rtype: Callablae[[Callable[[NewClient, EventType], None]], None]
        """

        def callback(func: Callable[[NewClient, EventType], None]) -> None:
            self.list_func.update({EVENT_TO_INT[event]: func})

        return callback


class Event:
    def __init__(self, client: NewClient):
        """
        Initializes the Event class with a client of type NewClient.
        Also sets up a default blocking function and an empty dictionary for list functions.

        :param client: An instance of the NewClient class
        :type client: NewClient
        """
        self.client = client
        self.paircode_cb = self.paircode(self.default_paircode_cb)
        self.list_func: Dict[int, Callable[[NewClient, Message], None]] = {}
        self._qr = self.__onqr

    def execute(
        self, uuid: int, binary: int, size: int, code: int
    ):  # Demands Attention
        """Executes a function from the list of functions based on the given code.

        :param binary: The binary data to be processed by the function.
        :type binary: int
        :param size: The size of the binary data.
        :type size: int
        :param code: The index of the function to be executed from the list of functions.
        :type code: int
        """
        if code not in INT_TO_EVENT:
            raise UnsupportedEvent()
        message = INT_TO_EVENT[code].FromString(ctypes.string_at(binary, size))
        if code == 0:
            self.client.me = message
            return
        elif code == 3:
            self.client.connected = True
        self.list_func[code](self.client, message)

    def __onqr(self, _: NewClient, data_qr: bytes):
        """
        Handles QR code generation and display.

        :param _: The client instance (not used in the function).
        :type _: NewClient
        :param data_qr: The data to be encoded in the QR code.
        :type data_qr: bytes
        """
        segno.make_qr(data_qr).terminal(compact=True)

    def qr(self, f: Callable[[NewClient, bytes], None]):
        """
        Sets a callback function for handling QR code data.

        :param f: The callback function that takes a NewClient instance and QR code data in bytes.
        :type f: Callable[[NewClient, bytes], None]
        """
        self._qr = f

    @property
    def paircode(self):
        def paircodecb(f: Callable[[NewClient, str, bool], None]):
            """
            Sets a callback function for handling pair codes.
            :param f: The callback function that takes a NewClient instance and pair code as a string.
            :type f: Callable[[NewClient, str], None]
            """

            def wrap_paircode_cb(code, connected):
                """
                Wraps the pair code callback function to include the client instance.
                :param code: The pair code as a string.
                :type code: str
                :param connected: A boolean indicating if the client is connected.
                :type connected: bool
                """
                paircode = ctypes.string_at(code)
                if self.paircode_cb:
                    f(self.client, paircode.decode(), connected)

            self.paircode_cb = wrap_paircode_cb
            return self.paircode_cb

        return paircodecb

    @staticmethod
    def default_paircode_cb(client: NewClient, data: str, connected: bool):
        if connected:
            log.info("authtenticated with pair code: %s", data)
        else:
            log.info("Pair code: %s", data)

    def __call__(
        self, event: Type[EventType]
    ) -> Callable[[Callable[[NewClient, EventType], None]], None]:
        """
        Registers a callback function for a specific event type.

        :param event: The type of event to register the callback for.
        :type event: Type[EventType]
        :return: A decorator that registers the callback function.
        :rtype: Callable[[Callable[[NewClient, EventType], None]], None]
        """

        def callback(func: Callable[[NewClient, EventType], None]) -> None:
            self.list_func.update({EVENT_TO_INT[event]: func})

        return callback
