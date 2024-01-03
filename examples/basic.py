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
from neonize.proto.Neonize_pb2 import MessageSource
from neonize.utils import Jid2String, MediaType
from neonize.utils import ChatPresence, ChatPresenceMedia
import magic


def onQr(client: NewClient, data_qr: bytes):
    print("qr", data_qr)


def onMessage(client: NewClient, from_: MessageSource, message: Message):
    text = message.extendedTextMessage and message.extendedTextMessage.text
    if text == "sticker":
        client.send_sticker(
            from_.Chat,
            "/home/krypton-byte/Downloads/WhatsApp Image 2023-12-30 at 6.54.03 AM.jpeg",
            quoted=message,
            from_=from_
        )
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
        response=client.send_message(
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
        print("response", response)
    elif text == "image":
        img = open(
            "/home/krypton-byte/Pictures/Screenshots/Screenshot_2023-12-26-00-31-03_1920x1080.png",
            "rb",
        ).read()
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
    elif text == "video":
        video = open(
            "/home/krypton-byte/Downloads/WhatsApp Video 2024-01-01 at 5.48.49 PM.mp4",
            "rb",
        ).read()
        up = client.upload(video)
        client.send_message(
            from_.Chat,
            Message(
                videoMessage=VideoMessage(
                    url=up.url,
                    caption="this is caption",
                    directPath=up.DirectPath,
                    fileEncSha256=up.FileEncSHA256,
                    fileLength=up.FileLength,
                    fileSha256=up.FileSHA256,
                    mediaKey=up.MediaKey,
                    mimetype=magic.from_buffer(video, mime=True),
                    viewOnce=True,
                )
            ),
        )
    elif text == "setgrupname":
        client.set_group_name(from_.Chat, "Hehe")
    elif text == "info":
        client.send_message(from_.Chat, Message(
            conversation=client.get_group_info(from_.Chat).__str__()
        ))
    elif text == "setgrupp":
        client.set_group_photo(
            from_.Chat, "/home/krypton-byte/Pictures/wallpapers/wallpaper_4.jpg"
        )
    elif text == "keluar":
        print('data',client.leave_group(
            from_.Chat
        ))
    elif text == "getinvite":
        client.send_message(
            from_.Chat,
            Message(conversation=client.get_group_invite_link(from_.Chat).__str__())
        )
    elif text == "join":
        return_ = client.join_group_with_link(".......")
        if not return_.Error:
            jid=client.send_message(return_.Jid, "text message")
    elif text == "presence":
        return_ = client.send_chat_presence(from_.Chat, ChatPresence.CHAT_PRESENCE_COMPOSING, ChatPresenceMedia.CHAT_PRESENCE_MEDIA_TEXT)
        time.sleep(2)
        client.send_chat_presence(from_.Chat, ChatPresence.CHAT_PRESENCE_PAUSED, ChatPresenceMedia.CHAT_PRESENCE_MEDIA_TEXT)
    elif text == "delete":
        client.build_revoke(
            from_.Chat,
            from_.Sender,
            from_.ID
        )
client = NewClient("krypton.so", messageCallback=onMessage, qrCallback=onQr)
client.connect()
