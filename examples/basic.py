import sys, os

sys.path.insert(0, os.getcwd())
from PIL import Image
import time
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
from neonize.proto.Neonize_pb2 import Message
from neonize.utils import Jid2String, MediaType
from neonize.utils import ChatPresence, ChatPresenceMedia
import magic
import time


def onQr(client: NewClient, data_qr: bytes):
    print("qr", data_qr)


def onMessage(client: NewClient, message: Message):
    client.send_message(message.Info.MessageSource.Chat, "hai gess")
    


client = NewClient("krypton.so", messageCallback=onMessage, qrCallback=onQr)
client.connect()
