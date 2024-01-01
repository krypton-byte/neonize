import sys, os

sys.path.insert(0, os.getcwd())
from PIL import Image
import base64
from io import BytesIO
from neonize.client import NewClient
from neonize.proto.def_pb2 import (
    Message,
    ImageMessage,
    ContextInfo,
    ExtendedTextMessage,
    StickerMessage,
    Chat
)
from neonize.proto.Neonize_pb2 import MessageSource
from neonize.utils import Jid2String, MediaType
import magic


def onQr(client: NewClient, data_qr: bytes):
    print("qr", data_qr)


def onMessage(client: NewClient, from_: MessageSource, message: Message):
    text = message.extendedTextMessage and message.extendedTextMessage.text
    if text == "sticker":
        client.send_sticker(from_.Chat, 'stickx.webp')
        # gg = open("stickx.webp","rb").read()
        # resp = client.upload(gg, media_type=MediaType.MediaImage)
        # client.send_message(
        #     from_.Chat,
        #     Message(
        #         stickerMessage=StickerMessage(
        #             url=resp.url,
        #             directPath=resp.DirectPath,
        #             fileEncSha256=resp.FileEncSHA256,
        #             fileLength=resp.FileLength,
        #             fileSha256=resp.FileSHA256,
        #             mediaKey=resp.MediaKey,
        #             mimetype=magic.from_buffer(gg, mime=True),
        #         )
        #     ),
        # )
        # print(Message(
        #         stickerMessage=StickerMessage(
        #             url=resp.url,
        #             directPath=resp.DirectPath,
        #             fileEncSha256=resp.FileEncSHA256,
        #             fileLength=resp.FileLength,
        #             fileSha256=resp.FileSHA256,
        #             mediaKey=resp.MediaKey,
        #             mimetype=magic.from_buffer(gg, mime=True),
        #         )
        #     ))
    if text == "ping":
        client.send_message(
            from_.Chat,
            Message(
                extendedTextMessage=ExtendedTextMessage(
                    contextInfo=ContextInfo(
                        stanzaId=from_.ID,
                        participant=Jid2String(from_.Sender),
                        quotedMessage=message,
                    ),
                    text="Pong!!",
                )
            ),
        )
    elif text == "image":
        img = open("/home/krypton-byte/Pictures/Screenshots/Screenshot_2023-12-26-00-31-03_1920x1080.png", "rb").read()
        resp = client.upload(img, media_type=MediaType.MediaImage)
        # pil: Image.Image = Image.open(BytesIO(img))
        # thumbnail = client.upload(img, media_type=MediaType.MediaLinkThumbnail)
        # print('thumbnail: ', thumbnail)
        client.send_message(
            from_.Chat,
            Message(
                imageMessage=ImageMessage(
                    url=resp.url,
                    thumbnailDirectPath=resp.DirectPath,
                    thumbnailEncSha256=resp.FileEncSHA256,
                    thumbnailSha256=resp.FileSHA256,
                    fileEncSha256=resp.FileEncSHA256,
                    mimetype=magic.from_buffer(img, mime=True),
                    caption="python",
                    fileLength=img.__len__(),
                    directPath=resp.DirectPath,
                    fileSha256=resp.FileSHA256,
                    jpegThumbnail=img,
                    mediaKey=resp.MediaKey,
                    contextInfo=ContextInfo(
                        stanzaId=from_.ID,
                        participant=Jid2String(from_.Sender),
                        quotedMessage=message,
                    ),
                ),
            ),
        )
    print(from_, message)


client = NewClient("krypton.so", messageCallback=onMessage, qrCallback=onQr)
client.connect()
