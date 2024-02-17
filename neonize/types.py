from typing import NewType, TypeVar

from neonize.proto.def_pb2 import (
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
    Message,
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
from neonize.proto.def_pb2 import (
    ImageMessage,
    Conversation,
    VideoMessage,
    DocumentMessage,
    ExtendedTextMessage,
    AudioMessage,
    StickerMessage,
)

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
    Conversation,
    ExtendedTextMessage,
    str,
)
