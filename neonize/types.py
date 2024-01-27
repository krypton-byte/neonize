import typing
from neonize.proto.Neonize_pb2 import Contact

from neonize.proto.def_pb2 import AudioMessage, ButtonsMessage, ContactsArrayMessage, DocumentMessage, EventMessage, ExtendedTextMessage, GroupInviteMessage, ImageMessage, ListMessage, ListResponseMessage, LiveLocationMessage, Message, MessageHistoryBundle, PollCreationMessage, ProductMessage, SendPaymentMessage, StickerMessage, VideoMessage


MessageServerID = typing.NewType("MessageServerID", int)
MessageWithContextInfo = typing.TypeVar("MessageWithContextInfo",
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
)