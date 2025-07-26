from __future__ import annotations

import asyncio
import ctypes
from asyncio import Event as IOEvent
from typing import TYPE_CHECKING, Awaitable, Callable, Coroutine, Dict, Type, TypeVar

import segno
from google.protobuf.message import Message

from ..events import EVENT_TO_INT, INT_TO_EVENT, UnsupportedEvent, log
from ..proto.Neonize_pb2 import QR as QREv
from ..proto.Neonize_pb2 import BlocklistChange as BlocklistChangeEv
from ..proto.Neonize_pb2 import BlocklistEvent as BlocklistEv
from ..proto.Neonize_pb2 import CallAccept as CallAcceptEv
from ..proto.Neonize_pb2 import CallOffer as CallOfferEv
from ..proto.Neonize_pb2 import CallOfferNotice as CallOfferNoticeEv
from ..proto.Neonize_pb2 import CallPreAccept as CallPreAcceptEv
from ..proto.Neonize_pb2 import CallRelayLatency as CallRelayLatencyEv
from ..proto.Neonize_pb2 import CallTerminate as CallTerminateEv
from ..proto.Neonize_pb2 import CallTransport as CallTransportEv
from ..proto.Neonize_pb2 import ChatPresence as ChatPresenceEv
from ..proto.Neonize_pb2 import ClientOutdated as ClientOutdatedEv
from ..proto.Neonize_pb2 import Connected as ConnectedEv
from ..proto.Neonize_pb2 import ConnectFailure as ConnectFailureEv
from ..proto.Neonize_pb2 import Disconnected as DisconnectedEv
from ..proto.Neonize_pb2 import GroupInfoEvent as GroupInfoEv
from ..proto.Neonize_pb2 import HistorySync as HistorySyncEv
from ..proto.Neonize_pb2 import IdentityChange as IdentityChangeEv
from ..proto.Neonize_pb2 import JoinedGroup as JoinedGroupEv
from ..proto.Neonize_pb2 import KeepAliveRestored as KeepAliveRestoredEv
from ..proto.Neonize_pb2 import KeepAliveTimeout as KeepAliveTimeoutEv
from ..proto.Neonize_pb2 import LoggedOut as LoggedOutEv
from ..proto.Neonize_pb2 import Message as MessageEv
from ..proto.Neonize_pb2 import NewsletterJoin as NewsletterJoinEv
from ..proto.Neonize_pb2 import NewsletterLeave as NewsletterLeaveEv
from ..proto.Neonize_pb2 import NewsletterLiveUpdate as NewsletterLiveUpdateEv
from ..proto.Neonize_pb2 import NewsLetterMessageMeta as NewsLetterMessageMetaEv
from ..proto.Neonize_pb2 import NewsletterMuteChange as NewsletterMuteChangeEv
from ..proto.Neonize_pb2 import OfflineSyncCompleted as OfflineSyncCompletedEv
from ..proto.Neonize_pb2 import OfflineSyncPreview as OfflineSyncPreviewEv
from ..proto.Neonize_pb2 import PairStatus as PairStatusEv
from ..proto.Neonize_pb2 import Picture as PictureEv
from ..proto.Neonize_pb2 import Presence as PresenceEv
from ..proto.Neonize_pb2 import Receipt as ReceiptEv
from ..proto.Neonize_pb2 import StreamError as StreamErrorEv
from ..proto.Neonize_pb2 import StreamReplaced as StreamReplacedEv
from ..proto.Neonize_pb2 import TemporaryBan as TemporaryBanEv
from ..proto.Neonize_pb2 import UnknownCallEvent as UnknownCallEventEv
from ..proto.Neonize_pb2 import privacySettingsEvent as PrivacySettingsEv

event_global_loop = asyncio.new_event_loop()

if TYPE_CHECKING:
    from .client import ClientFactory, NewAClient
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
        self.blocking_func = self.paircode(self.default_paircode_cb)
        self.list_func: Dict[
            int, Callable[[NewAClient, Message], Coroutine[None, None, None]]
        ] = {}
        self._qr = self.__onqr

    def execute(self, uuid: int, binary: int, size: int, code: int):
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
        # print("key", code, "uuid", uuid, "size", size)
        # print(f"Executing function for event code {ctypes.string_at(code, size)} with UUID {uuid}")
        message = INT_TO_EVENT[code].FromString(ctypes.string_at(binary, size))

        if code == 0:
            self.client.me = message
            return
        elif code == 3:
            self.client.connected = True
        # loop = asyncio.new_event_loop()
        # loop.run_until_complete(
        #     self.list_func[code](self.client, message)
        # )
        # loop.close()
        asyncio.run_coroutine_threadsafe(
            self.list_func[code](self.client, message), event_global_loop
        )

    async def __onqr(self, _: NewAClient, data_qr: bytes):
        """
        Handles QR code generation and display.

        :param _: The client instance (not used in the function).
        :type _: NewClient
        :param data_qr: The data to be encoded in the QR code.
        :type data_qr: bytes
        """
        segno.make_qr(data_qr).terminal(compact=True)

    def qr(self, f: Callable[[NewAClient, bytes], Coroutine[None, None, None]]):
        """
        Sets a callback function for handling QR code data.

        :param f: The callback function that takes a NewClient instance and QR code data in bytes.
        :type f: Callable[[NewClient, bytes], None]
        """
        self._qr = f

    @property
    def paircode(self):
        def paircodecb(
            f: Callable[[NewAClient, str, bool], Coroutine[None, None, None]],
        ):
            """
            A decorator that registers a callback function for handling pair code events.
            :param f: The callback function that takes a NewAClient instance, pair code as a string, and a boolean indicating if the connection is established.
            :type f: Callable[[NewAClient, str, bool], Coroutine[None, None, None]]
            :return: A function that wraps the callback function to handle pair code events.
            :rtype: Callable[[NewAClient, bytes, bool], Coroutine[None, None, None]]
            """

            def wrap_paircode(_, code, connected: bool):
                paircode = ctypes.string_at(code)
                asyncio.run_coroutine_threadsafe(
                    f(self.client, paircode.decode(), connected), event_global_loop
                ).result()

            self.blocking_func = wrap_paircode
            return self.blocking_func

        return paircodecb

    @staticmethod
    async def default_paircode_cb(
        client: NewAClient, data: str, connected: bool = True
    ):
        """
        A default callback function that handles the pair code event.
        This function is called when the pair code event occurs, and it blocks the execution until the event is processed.
        :param client: The client instance that triggered the event.
        :type client: NewAClient
        :param data: The pair code data as a string.
        :type data: str
        """
        if connected:
            log.info("Pair code successfully processed: %s", data)
        else:
            log.info("Pair code: %s", data)

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


# threading.Thread(
#    target=event_global_loop.run_forever,
#    daemon=True,
# ).start()
