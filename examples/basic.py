import sys, os

sys.path.insert(0, os.getcwd())
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
from neonize.proto.Neonize_pb2 import Message, MessageInfo
from neonize.utils import Jid2String, MediaType
from neonize.utils import ChatPresence, ChatPresenceMedia
import magic
import time


def onQr(client: NewClient, data_qr: bytes):
    print("qr", data_qr)


def onMessage(client: NewClient, message: Message):
    match message.Message.extendedTextMessage.text:
        case "test":
            client.send_message(message.Info.MessageSource.Chat, client.get_contact_qr_link())
        case "request":
            client.send_message(message.Info.MessageSource.Chat, client.get_group_request_participants(message.Info.MessageSource.Chat).__str__())
        case "list_groups":
            client.send_message(message.Info.MessageSource.Chat, client.get_joined_groups().__str__())
        case "get_linked":
            client.send_message(message.Info.MessageSource.Chat, client.get_linked_group_participants(message.Info.MessageSource.Chat).__str__())
        case "newsletter":
            client.send_message(message.Info.MessageSource.Chat, client.get_newsletter_info(message.Info.MessageSource.Chat).__str__())
        case "newsletter_link":
            client.send_message(message.Info.MessageSource.Chat, client.get_newsletter_info_with_invite('https://whatsapp.com/channel/0029Va7gIOyBKfi4aw2cYy24').__str__())
client = NewClient("krypton.so", messageCallback=onMessage, qrCallback=onQr)
client.connect()
