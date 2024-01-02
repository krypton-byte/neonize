from __future__ import annotations
from enum import Enum
import io
import magic
import typing
import requests


class MediaType(Enum):
    MediaImage = 1
    MediaVideo = 2
    MediaAudio = 3
    MediaDocument = 4
    MediaHistory = 5
    MediaAppState = 6
    MediaLinkThumbnail = 7

    @classmethod
    def from_magic(cls, fn_or_bytes: typing.Union[str, bytes]) -> MediaType:
        magic_func = (
            magic.from_file if isinstance(fn_or_bytes, str) else magic.from_buffer
        )
        mime = magic_func(fn_or_bytes, mime=True).split('/')[0]
        match mime:
            case 'image':
                return cls.MediaImage
            case 'video':
                return cls.MediaVideo
            case 'audio':
                return cls.MediaAudio
            case _:
                return cls.MediaDocument


class ChatPresence(Enum):
    CHAT_PRESENCE_COMPOSING = 0
    CHAT_PRESENCE_PAUSED = 1

class ChatPresenceMedia(Enum):
    CHAT_PRESENCE_MEDIA_TEXT = 0
    CHAT_PRESENCE_MEDIA_AUDIO = 1

def Jid2String(jid: JID) -> str:
    if jid.RawAgent > 0:
        return '%s.%s:%d@%s' % (jid.User, jid.RawAgent, jid.Device, jid.Server)
    elif jid.Device > 0:
        return '%s:%d@%s' % (jid.User, jid.Device, jid.Server)
    elif len(jid.User) > 0:
        return '%s@%s' % (jid.User, jid.Server)
    return jid.Server


def get_bytes_from_name_or_url(args: typing.Union[str, bytes]) -> bytes:
    if isinstance(args, str):
        if args.startswith('http'):
            return requests.get(args).content
        else:
            with open(args, 'rb') as file:
                return file.read()
    else:
        return args


def write_from_bytesio_or_filename(fn_or_bytesio: io.BytesIO | str, data: bytes):
    if isinstance(fn_or_bytesio, io.BytesIO):
        fn_or_bytesio.write(data)
    else:
        with open(fn_or_bytesio, 'wb') as file:
            file.write(data)
