from __future__ import annotations
import ctypes
import asyncio
import segno
from ..events import EVENT_TO_INT, INT_TO_EVENT, UnsupportedEvent, log
from ..proto.Neonize_pb2 import (
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
    Receipt as ReceiptEv,
    ChatPresence as ChatPresenceEv,
    Presence as PresenceEv,
    JoinedGroup as JoinedGroupEv,
    GroupInfoEvent as GroupInfoEv,
    Picture as PictureEv,
    IdentityChange as IdentityChangeEv,
    privacySettingsEvent as PrivacySettingsEv,
    OfflineSyncPreview as OfflineSyncPreviewEv,
    OfflineSyncCompleted as OfflineSyncCompletedEv,
    BlocklistEvent as BlocklistEv,
    BlocklistChange as BlocklistChangeEv,
    NewsletterJoin as NewsletterJoinEv,
    NewsletterLeave as NewsletterLeaveEv,
    NewsletterMuteChange as NewsletterMuteChangeEv,
    NewsletterLiveUpdate as NewsletterLiveUpdateEv,
    CallOffer as CallOfferEv,
    CallAccept as CallAcceptEv,
    CallPreAccept as CallPreAcceptEv,
    CallTransport as CallTransportEv,
    CallOfferNotice as CallOfferNoticeEv,
    CallRelayLatency as CallRelayLatencyEv,
    CallTerminate as CallTerminateEv,
    UnknownCallEvent as UnknownCallEventEv,
)

from google.protobuf.message import Message
from typing import Awaitable, Dict, Callable, Type, TypeVar, TYPE_CHECKING
from asyncio import Event as IOEvent

if TYPE_CHECKING:
    from .client import NewAClient, ClientFactory
EventType = TypeVar("EventType", bound=Message)
event = IOEvent()
__all__ = [
    "QREv",
    "PairStatusEv",
    "ConnectedEv",
    "KeepAliveTimeoutEv",
    "KeepAliveRestoredEv",
    "LoggedOutEv",
    "StreamReplacedEv",
    "TemporaryBanEv",
    "ConnectFailureEv",
    "ClientOutdatedEv",
    "StreamErrorEv",
    "DisconnectedEv",
    "HistorySyncEv",
    "NewsLetterMessageMetaEv",
    "MessageEv",
    "ReceiptEv",
    "ChatPresenceEv",
    "PresenceEv",
    "JoinedGroupEv",
    "GroupInfoEv",
    "PictureEv",
    "IdentityChangeEv",
    "PrivacySettingsEv",
    "OfflineSyncPreviewEv",
    "OfflineSyncCompletedEv",
    "BlocklistEv",
    "BlocklistChangeEv",
    "NewsletterJoinEv",
    "NewsletterLeaveEv",
    "NewsletterMuteChangeEv",
    "NewsletterLiveUpdateEv",
    "CallOfferEv",
    "CallAcceptEv",
    "CallPreAcceptEv",
    "CallTransportEv",
    "CallOfferNoticeEv",
    "CallRelayLatencyEv",
    "CallTerminateEv",
    "UnknownCallEventEv",
]


class Event:
    def __init__(self, client: NewAClient):
        """
        Initializes the Event class with a client of type NewClient.
        Also sets up a default blocking function and an empty dictionary for list functions.

        :param client: An instance of the NewClient class
        :type client: NewClient
        """
        self.client = client
        self.blocking_func = self.blocking(self.default_blocking)
        self.list_func: Dict[int, Callable[[NewAClient, Message], Awaitable[None]]] = {}
        self._qr = self.__onqr

    def execute(self, binary: int, size: int, code: int):
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
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.list_func[code](self.client, message))
        loop.close()

    async def __onqr(self, _: NewAClient, data_qr: bytes):
        """
        Handles QR code generation and display.

        :param _: The client instance (not used in the function).
        :type _: NewClient
        :param data_qr: The data to be encoded in the QR code.
        :type data_qr: bytes
        """
        segno.make_qr(data_qr).terminal(compact=True)

    def qr(self, f: Callable[[NewAClient, bytes], Awaitable[None]]):
        """
        Sets a callback function for handling QR code data.

        :param f: The callback function that takes a NewClient instance and QR code data in bytes.
        :type f: Callable[[NewClient, bytes], None]
        """
        self._qr = f

    @property
    def blocking(self):
        def block(f: Callable[[NewAClient], Awaitable[None]]):
            """This method assigns a blocking function to process a new client and prevents the process from ending.

            :param f: A function that takes a new client as an argument and returns nothing.
            :type f: Callable[[NewClient], None]
            """

            def wrap_blocking(_):
                loop = asyncio.new_event_loop()
                loop.run_until_complete(f(self.client))
                loop.close()

            self.blocking_func = wrap_blocking
            return self.blocking_func

        return block

    @classmethod
    async def default_blocking(cls, _):
        log.debug("🚧 The blocking function has been called.")
        await event.wait()
        log.debug("🚦 The function has been unblocked.")

    def __call__(
        self, event: Type[EventType]
    ) -> Callable[[Callable[[NewAClient, EventType], Awaitable[None]]], None]:
        """
        Registers a callback function for a specific event type.

        :param event: The type of event to register the callback for.
        :type event: Type[EventType]
        :return: A decorator that registers the callback function.
        :rtype: Callable[[Callable[[NewClient, EventType], None]], None]
        """

        def callback(func: Callable[[NewAClient, EventType], Awaitable[None]]) -> None:
            self.list_func.update({EVENT_TO_INT[event]: func})

        return callback


class EventsManager:
    def __init__(self, client_factory: ClientFactory):
        self.client_factory = client_factory
        self.list_func: Dict[int, Callable[[NewAClient, Message], Awaitable[None]]] = {}

    def __call__(
        self, event: Type[EventType]
    ) -> Callable[[Callable[[NewAClient, EventType], Awaitable[None]]], None]:
        """
        Registers a callback function for a specific event type.

        :param event: The type of event to register the callback for.
        :type event: Type[EventType]
        :return: A decorator that registers the callback function.
        :rtype: Callable[[Callable[[NewClient, EventType], None]], None]
        """

        def callback(func: Callable[[NewAClient, EventType], Awaitable[None]]) -> None:
            self.list_func.update({EVENT_TO_INT[event]: func})

        return callback
