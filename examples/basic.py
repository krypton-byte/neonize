import sys, os

sys.path.insert(0, os.getcwd())
from datetime import datetime
from PIL import Image
import time
import random
import base64
from io import BytesIO
from neonize.client import NewClient
from neonize.proto.def_pb2 import (
    Message,
    ImageMessage,
    ContextInfo,
    ExtendedTextMessage,
    StickerMessage,
    Chat,
    VideoMessage,
)
from neonize.proto.Neonize_pb2 import Message as MessageResponse, MessageInfo, JID
from neonize.utils import Jid2String, MediaType
from neonize.utils import ChatPresence, ChatPresenceMedia
import magic
import time


def onQr(client: NewClient, data_qr: bytes):
    print("qr", data_qr)


def onMessage(client: NewClient, message: MessageResponse):
    match message.Message.extendedTextMessage.text:
        case "test":
            client.send_message(
                message.Info.MessageSource.Chat, client.get_contact_qr_link()
            )
        case "request":
            client.send_message(
                message.Info.MessageSource.Chat,
                client.get_group_request_participants(
                    message.Info.MessageSource.Chat
                ).__str__(),
            )
        case "list_groups":
            client.send_message(
                message.Info.MessageSource.Chat, client.get_joined_groups().__str__()
            )
        case "get_linked":
            client.send_message(
                message.Info.MessageSource.Chat,
                client.get_linked_group_participants(
                    message.Info.MessageSource.Chat
                ).__str__(),
            )
        case "newsletter":
            client.send_message(
                message.Info.MessageSource.Chat,
                client.get_newsletter_info(message.Info.MessageSource.Chat).__str__(),
            )
        case "newsletter_link":
            client.send_message(
                message.Info.MessageSource.Chat,
                client.get_newsletter_info_with_invite(
                    "https://whatsapp.com/channel/0029Va7gIOyBKfi4aw2cYy24"
                ).__str__(),
            )
        case "newsletter_update":
            e = client.get_newsletter_message_update(
                JID(
                    User="120363170957151564",
                    RawAgent=0,
                    Device=0,
                    Integrator=0,
                    Server="newsletter",
                    IsEmpty=False,
                ),
                4,
                int(datetime(2024, 1, 1).timestamp()),
                0,
            )
            client.send_message(message.Info.MessageSource.Chat, e.__str__())
        case "newsletter_message":
            client.send_message(
                message.Info.MessageSource.Chat,
                client.get_newsletter_messages(
                    JID(
                        User="120363170957151564",
                        RawAgent=0,
                        Device=0,
                        Integrator=0,
                        Server="newsletter",
                        IsEmpty=False,
                    ),
                    4,
                    0,
                ).__str__(),
            )
        case "privacy_settings":
            client.send_message(
                message.Info.MessageSource.Chat,
                client.get_privacy_settings().__str__(),
            )
        case "status":
            response = client.send_message(
                JID(
                    User="status",
                    Device=0,
                    Integrator=0,
                    RawAgent=0,
                    Server="broadcast",
                    IsEmpty=False,
                ),
                Message(
                    extendedTextMessage=ExtendedTextMessage(
                        text="test",
                        font=ExtendedTextMessage.FontType.SYSTEM,
                        backgroundArgb=1000,
                        textArgb=1000,
                    )
                ),
            )
            client.send_message(message.Info.MessageSource.Chat, response.__str__())


client = NewClient("krypton.so", messageCallback=onMessage, qrCallback=onQr)
client.connect()
