from ..proto.waE2E.WAWebProtobufsE2E_pb2 import (
    Message,
    ImageMessage,
    DocumentMessage,
    ExtendedTextMessage,
    VideoMessage,
    PollUpdateMessage,
)
from ..proto import Neonize_pb2 as neonize_proto
from ..types import MediaMessageType, TextMessageType


def get_message_type(message: Message) -> MediaMessageType | TextMessageType:
    """
    Determines the type of message.

    :param message: The message object.
    :type message: Message
    :raises IndexError: If the message type cannot be determined.
    :return: The type of the message.
    :rtype: MediaMessageType | TextMessageType
    """
    for field_name, v in message.ListFields():
        if field_name.name.endswith("Message"):
            return v
        elif field_name.name == "conversation":
            return v
    raise IndexError()


def extract_text(message: Message):
    """
    Extracts text content from a message.

    :param message: The message object.
    :type message: Message
    :return: The extracted text content.
    :rtype: str
    """
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


def get_poll_update_message(message: neonize_proto.Message) -> PollUpdateMessage | None:
    """
    Extracts pollUpdateMessage from event Message
    :param message: The message object.
    :type message: neonize_proto.Message
    :return: The extracted poll update message.
    :rtype: PollUpdateMessage
    """
    msg = message.Message
    if msg.pollUpdateMessage.ListFields():
        pollUpdateMessage: PollUpdateMessage = msg.pollUpdateMessage
        return pollUpdateMessage
