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
from neonize.proto.Neonize_pb2 import Message as MessageResponse, MessageInfo, JID, PairStatus
from neonize.utils import Jid2String, MediaType
from neonize.utils import ChatPresence, ChatPresenceMedia
from neonize.utils import LogLevel
import magic
import time


def onQr(client: NewClient, data_qr: bytes):
    print(data_qr)

client = NewClient("krypton.so", qrCallback=onQr)

@client.event(MessageResponse)
def onMessage(client: NewClient, message: MessageResponse):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    match text:
        case "ping":
            client.send_message(chat, "pong")
        case "sticker":
            client.send_sticker(chat, "/home/krypton-byte/Downloads/5b231c4cdac4c254142ff.png")
        case "debug":
            client.send_message(chat, message.__str__())
        case "viewonce":
            upload = client.upload(open("/home/krypton-byte/Downloads/5b231c4cdac4c254142ff.png", "rb").read())
            client.send_message(
                chat,
                Message(
                    imageMessage=ImageMessage(
                        url=upload.url,
                        caption="CAPTION",
                        directPath=upload.DirectPath,
                        fileEncSha256=upload.FileEncSHA256,
                        fileLength=upload.FileLength,
                        fileSha256=upload.FileSHA256,
                        jpegThumbnail=open("/home/krypton-byte/Downloads/5b231c4cdac4c254142ff.png","rb").read(),
                        mediaKey=upload.MediaKey,
                        mimetype=magic.from_file("/home/krypton-byte/Downloads/5b231c4cdac4c254142ff.png", mime=True),
                        thumbnailDirectPath=upload.DirectPath,
                        thumbnailEncSha256=upload.FileEncSHA256,
                        thumbnailSha256=upload.FileSHA256,
                        viewOnce=True
                    )
                )
            )

@client.event(PairStatus)
def PairStatusMessage(client: NewClient, message: PairStatus):
    print(client, message)

client.connect(log_level=LogLevel.INFO)
