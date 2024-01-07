from __future__ import annotations
from enum import Enum
import magic
import typing


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
        magic_func = (
            magic.from_file if isinstance(fn_or_bytes, str) else magic.from_buffer
        )
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
    CHAT_PRESENCE_COMPOSING = 0
    CHAT_PRESENCE_PAUSED = 1


class ChatPresenceMedia(Enum):
    CHAT_PRESENCE_MEDIA_TEXT = 0
    CHAT_PRESENCE_MEDIA_AUDIO = 1


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    ERROR = 4

class ReceiptType(Enum):
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
    