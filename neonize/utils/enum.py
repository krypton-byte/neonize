from __future__ import annotations
from enum import Enum
import magic
import typing
from ..proto.waE2E.WAWebProtobufsE2E_pb2 import (
    Message,
    ImageMessage,
    AudioMessage,
    VideoMessage,
    DocumentMessage,
)
from .message import get_message_type


class MediaTypeToMMS(Enum):
    MediaImage = "image"
    MediaAudio = "audio"
    MediaVideo = "video"
    MediaDocument = "document"
    MediaHistory = "md-msg-hist"
    MediaAppState = "md-app-state"
    MediaLinkThumbnail = "thumbnail-link"

    @classmethod
    def from_message(cls, message: Message):
        return {
            ImageMessage: cls.MediaImage,
            AudioMessage: cls.MediaAudio,
            VideoMessage: cls.MediaVideo,
            DocumentMessage: cls.MediaDocument,
        }[type(get_message_type(message))]

    @classmethod
    def from_mime(cls, mime: str):
        type_ = mime.split("/")[0]
        return {
            "audio": cls.MediaAudio,
            "video": cls.MediaVideo,
            "image": cls.MediaImage,
        }.get(type_, cls.MediaDocument)


class MediaType(Enum):
    MediaImage = 0
    MediaVideo = 1
    MediaAudio = 2
    MediaDocument = 3
    MediaHistory = 4
    MediaAppState = 5
    MediaLinkThumbnail = 6

    @classmethod
    def from_magic(cls, fn_or_bytes: typing.Union[str, bytes]) -> MediaType:
        """Returns the MediaType based on file magic bytes or file extension.

        :param fn_or_bytes: Either a file path (str) or binary data (bytes) for determining the MediaType.
        :type fn_or_bytes: typing.Union[str, bytes]
        :return: The determined MediaType.
        :rtype: MediaType
        """
        magic_func = magic.from_file if isinstance(fn_or_bytes, str) else magic.from_buffer
        mime = magic_func(fn_or_bytes, mime=True).split("/")[0]
        match mime:
            case "image":
                return cls.MediaImage
            case "video":
                return cls.MediaVideo
            case "audio":
                return cls.MediaAudio
            case _:
                return cls.MediaDocument


class ChatPresence(Enum):
    """
    Enum representing the presence status in a chat.

    Attributes:
        CHAT_PRESENCE_COMPOSING (int): Indicates that the user is currently composing a message.
        CHAT_PRESENCE_PAUSED (int): Indicates that the user has paused composing a message.
    """

    CHAT_PRESENCE_COMPOSING = 0
    CHAT_PRESENCE_PAUSED = 1


class ChatPresenceMedia(Enum):
    """
    Enum representing the type of media being used in a chat.

    Attributes:
        CHAT_PRESENCE_MEDIA_TEXT (int): Indicates that the chat media type is text.
        CHAT_PRESENCE_MEDIA_AUDIO (int): Indicates that the chat media type is audio.
    """

    CHAT_PRESENCE_MEDIA_TEXT = 0
    CHAT_PRESENCE_MEDIA_AUDIO = 1


class LogLevel(Enum):
    """
    Enum representing the different levels of logging.

    Attributes:
        NOTSET (int): Logging level not set, represented by -1.
        DEBUG (int): Debug level, represented by 0.
        INFO (int): Information level, represented by 1.
        WARN (int): Warning level, represented by 2.
        ERROR (int): Error level, represented by 3.
    """

    NOTSET = -1
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

    @property
    def level(self) -> bytes:
        """
        Returns the logging level name encoded as bytes.

        Returns:
            bytes: The name of the logging level encoded in bytes. If the level is NOTSET, returns an empty byte string.
        """
        if self is self.NOTSET:
            return b""
        return self.name.encode()

    @classmethod
    def from_logging(cls, level: int):
        """
        Converts a numeric logging level to a corresponding LogLevel enum member.

        Args:
            level (int): Numeric value representing the logging level.

        Returns:
            LogLevel: The corresponding LogLevel enum member.
        """
        match level:
            case 50:
                return cls.ERROR
            case 40:
                return cls.ERROR
            case 30:
                return cls.WARN
            case 20:
                return cls.INFO
            case 10:
                return cls.DEBUG
            case 0:
                return cls.NOTSET
        return cls.INFO

    def log_level(self) -> int:
        """
        Converts the LogLevel enum member to its corresponding numeric logging level.

        Returns:
            int: The numeric value representing the logging level.
        """
        return (self.value + 1) * 10


class ReceiptType(Enum):
    """
    Enum representing different types of message receipts.

    Attributes:
        DELIVERED (bytes): Indicates that the message has been delivered.
        SENDER (bytes): Indicates that the message is from the sender.
        RETRY (bytes): Indicates a retry receipt.
        READ (bytes): Indicates that the message has been read.
        READ_SELF (bytes): Indicates that the message has been read by the sender themselves.
        PLAYED (bytes): Indicates that the message has been played (e.g., for audio messages).
        PLAYED_SELF (bytes): Indicates that the message has been played by the sender themselves.
        SERVER_ERROR (bytes): Indicates a server error receipt.
        INACTIVE (bytes): Indicates that the recipient is inactive.
        PEER_MSG (bytes): Indicates a peer message receipt.
        HISTORY_SYNC (str): Indicates that the message is part of a history sync.
    """

    DELIVERED = b""
    SENDER = b"sender"
    RETRY = b"RETRY"
    READ = b"read"
    READ_SELF = b"read-self"
    PLAYED = b"played"
    PLAYED_SELF = b"played-self"
    SERVER_ERROR = b"server-error"
    INACTIVE = b"inactive"
    PEER_MSG = b"peer_msg"
    HISTORY_SYNC = "hist_sync"


class ClientType(Enum):
    """
    Enumeration of client types.

    Attributes:
        UNKNOWN (int): Unknown client type.
        CHROME (int): Chrome browser.
        EDGE (int): Microsoft Edge browser.
        FIREFOX (int): Mozilla Firefox browser.
        IE (int): Internet Explorer browser.
        OPERA (int): Opera browser.
        SAFARI (int): Safari browser.
        ELECTRON (int): Electron framework.
        UWP (int): Universal Windows Platform.
        OTHER (int): Other client types.
    """

    UNKNOWN = 0
    CHROME = 1
    EDGE = 2
    FIREFOX = 3
    IE = 4
    OPERA = 5
    SAFARI = 6
    ELECTRON = 7
    UWP = 8
    OTHER = 9

    @property
    def name(self) -> str:
        """
        Returns the title-cased name of the client type.

        :return: The title-cased name.
        :rtype: str
        """
        return super().name.title()


class ClientName(Enum):
    """
    Enumeration of client names.

    Attributes:
        LINUX (str): Linux operating system.
        WINDOWS (str): Windows operating system.
        ANDROID (str): Android operating system.
    """

    LINUX = "linux"
    WINDOWS = "windows nt"
    ANDROID = "android"

    @property
    def name(self) -> str:
        """
        Returns the title-cased name of the client.

        :return: The title-cased name.
        :rtype: str
        """
        return super().name.title()


class PrivacySettingType(Enum):
    """
    Enumeration of privacy setting types.

    Attributes:
        GROUP_ADD (str): Group add privacy setting.
        LAST_SEEN (str): Last seen privacy setting.
        STATUS (str): Status privacy setting.
        PROFILE (str): Profile privacy setting.
        READ_RECEIPTS (str): Read receipts privacy setting.
        ONLINE (str): Online privacy setting.
        CALL_ADD (str): Call add privacy setting.
    """

    GROUP_ADD = "groupadd"
    LAST_SEEN = "last"
    STATUS = "status"
    PROFILE = "profile"
    READ_RECEIPTS = "readreceipts"
    ONLINE = "online"
    CALL_ADD = "calladd"


class PrivacySetting(Enum):
    """
    Enumeration of privacy settings.

    Attributes:
        UNDEFINED (str): Undefined privacy setting.
        ALL (str): All privacy setting.
        CONTACTS (str): Contacts privacy setting.
        CONTACTS_BLACKLIST (str): Contacts blacklist privacy setting.
        MATCH_LAST_SEEN (str): Match last seen privacy setting.
        KNOWN (str): Known privacy setting.
        NONE (str): None privacy setting.
    """

    UNDEFINED = ""
    ALL = "all"
    CONTACTS = "contacts"
    CONTACTS_BLACKLIST = "contacts_blacklist"
    MATCH_LAST_SEEN = "match_last_seen"
    KNOWN = "known"
    NONE = "none"


class BlocklistAction(Enum):
    """
    Enumeration of blocklist actions.

    Attributes:
        BLOCK (str): Block action.
        UNBLOCK (str): Unblock action.
    """

    BLOCK = "block"
    UNBLOCK = "unblock"


class ParticipantChange(Enum):
    """
    Enumeration of participant change actions.

    Attributes:
        ADD (str): Add participant action.
        REMOVE (str): Remove participant action.
        PROMOTE (str): Promote participant action.
        DEMOTE (str): Demote participant action.
    """

    ADD = "add"
    REMOVE = "remove"
    PROMOTE = "promote"
    DEMOTE = "demote"


class ParticipantRequestChange(Enum):
    """
    Enumeration of participant request change actions.

    Attributes:
        APPROVE (str): Approve participant request action.
        REJECT (str): Reject participant request action.
    """

    APPROVE = "approve"
    REJECT = "reject"


class Presence(Enum):
    AVAILABLE = b"available"
    UNAVAILABLE = b"unavailable"
