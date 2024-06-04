from typing import NewType, TypeVar

from .proto.waE2E.WAWebProtobufsE2E_pb2 import (
    AudioMessage,
    ButtonsMessage,
    ContactsArrayMessage,
    DocumentMessage,
    EventMessage,
    ExtendedTextMessage,
    GroupInviteMessage,
    ImageMessage,
    ListMessage,
    ListResponseMessage,
    LiveLocationMessage,
    MessageHistoryBundle,
    PollCreationMessage,
    ProductMessage,
    StickerMessage,
    VideoMessage,
)

MessageServerID = NewType("MessageServerID", int)
MessageWithContextInfo = TypeVar(
    "MessageWithContextInfo",
    ImageMessage,
    ContactsArrayMessage,
    ExtendedTextMessage,
    DocumentMessage,
    AudioMessage,
    VideoMessage,
    LiveLocationMessage,
    StickerMessage,
    GroupInviteMessage,
    GroupInviteMessage,
    ProductMessage,
    ListMessage,
    ListMessage,
    ListResponseMessage,
    ButtonsMessage,
    ButtonsMessage,
    PollCreationMessage,
    MessageHistoryBundle,
    EventMessage,
    ContactsArrayMessage,
)

MediaMessageType = TypeVar(
    "MediaMessageType",
    ImageMessage,
    AudioMessage,
    VideoMessage,
    StickerMessage,
    DocumentMessage,
)

from typing import TypeVar

MediaMessageType = TypeVar(
    "MediaMessageType",
    ImageMessage,
    AudioMessage,
    VideoMessage,
    StickerMessage,
    DocumentMessage,
)

TextMessageType = TypeVar(
    "TextMessageType",
    ExtendedTextMessage,
    str,
)
