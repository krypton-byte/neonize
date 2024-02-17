from ..proto.def_pb2 import (
    Message,
    ImageMessage,
    DocumentMessage,
    ExtendedTextMessage,
    VideoMessage,
)
from ..types import MediaMessageType, TextMessageType


def get_message_type(message: Message) -> MediaMessageType | TextMessageType:
    for field_name, v in message.ListFields():
        if field_name.name.endswith("Message"):
            return v
        elif field_name.name == "conversation":
            return v
    raise IndexError()


def extract_text(message: Message):
    if message.imageMessage.ListFields():
        imageMessage: ImageMessage = message.imageMessage
        return imageMessage.caption
    elif message.extendedTextMessage.ListFields():
        extendedTextMessage: ExtendedTextMessage = message.extendedTextMessage
        return extendedTextMessage.text
    elif message.videoMessage.ListFields():
        videoMessage: VideoMessage = message.videoMessage
        return videoMessage.caption
    elif message.documentMessage.ListFields():
        documentMessage: DocumentMessage = message.documentMessage
        return documentMessage.caption
    elif message.conversation:
        return message.conversation
    return ""
