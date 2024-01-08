import logging
import sys, os

from neonize.types import MessageServerID

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
from neonize.proto.Neonize_pb2 import (
    Message as MessageResponse,
    MessageInfo,
    JID,
    PairStatus,
)
from neonize.utils import Jid2String, MediaType
from neonize.utils import ChatPresence, ChatPresenceMedia
from neonize.utils import LogLevel, ReceiptType, log
import magic
import time
import segno
import signal
import sys
from neonize.utils import event


def interrupted(*args):
    event.set()


log.setLevel(logging.DEBUG)
signal.signal(signal.SIGINT, interrupted)


def onQr(_: NewClient, data_qr: bytes):
    segno.make_qr(data_qr).terminal(compact=True)


client = NewClient("krypton_pairphone.so", qrCallback=onQr)


@client.blocking
def testblock(client: NewClient):
    log.debug("Blocking Function!")
    event.wait()
    client.disconnect()
    log.debug("Blocking Function Quit!")


@client.event(MessageResponse)
def onMessage(client: NewClient, message: MessageResponse):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    match text:
        case "ping":
            client.reply_message(chat, "pong", message)
        case "_sticker":
            client.send_sticker(
                chat, "https://mystickermania.com/cdn/stickers/anime/spy-family-anya-smirk-512x512.png"
            )
        case "_image":
            client.send_image(
                chat,
                "https://download.samplelib.com/png/sample-boat-400x300.png",
                caption="Test",
                quoted=message,
            )
        case "_video":
            client.send_video(
                chat,
                "https://download.samplelib.com/mp4/sample-5s.mp4",
                caption="Test",
                quoted=message,
            )
        case "_audio":
            client.send_audio(
                chat,
                "https://download.samplelib.com/mp3/sample-12s.mp3",
                quoted=message,
            )
        case "_ptt":
            client.send_audio(
                chat,
                "https://download.samplelib.com/mp3/sample-12s.mp3",
                ptt=True,
                quoted=message,
            )
        case "_doc":
            client.send_document(
                chat,
                "https://download.samplelib.com/xls/sample-heavy-1.xls",
                caption="Test",
                filename="test.xls",
                quoted=message,
            )
        case "debug":
            client.send_message(chat, message.__str__())
        case "viewonce":
            client.send_image(
                chat,
                "https://pbs.twimg.com/media/GC3ywBMb0AAAEWO?format=jpg&name=medium",
                viewonce=True,
            )
        case "profile_pict":
            client.send_message(chat, client.get_profile_picture(chat).__str__())
        case "status_privacy":
            client.send_message(chat, client.get_status_privacy().__str__())
        case "read":
            client.send_message(
                chat,
                client.mark_read(
                    [message.Info.ID],
                    message.Info.MessageSource.Chat,
                    message.Info.MessageSource.Sender,
                    ReceiptType.READ,
                ).__str__(),
            )
        case "read_channel":
            metadata = client.get_newsletter_info_with_invite(
                "https://whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M"
            )
            err = client.follow_newsletter(metadata.ID)
            client.send_message(chat, "error: " + err)
            resp = client.newsletter_mark_viewed(metadata.ID, [MessageServerID(0)])
            client.send_message(chat, resp.__str__() + "\n" + metadata.__str__())
        case "keluar#09":
            client.logout()
        case "send_react_channel":
            metadata = client.get_newsletter_info_with_invite(
                "https://whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M"
            )
            data_msg = client.get_newsletter_messages(metadata.ID, 2, MessageServerID(0))
            client.send_message(chat, data_msg.__str__())
            for _ in data_msg:
                client.newsletter_send_reaction(
                    metadata.ID, MessageServerID(0), "🗿", "")
        case "subscribe_channel_updates":
            metadata = client.get_newsletter_info_with_invite(
                "https://whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M"
            )
            result = client.newsletter_subscribe_live_updates(metadata.ID)
            client.send_message(chat, result.__str__())
        case "mute_channel":
            metadata = client.get_newsletter_info_with_invite(
                "https://whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M"
            )
            client.send_message(
                chat, client.newsletter_toggle_mute(metadata.ID, False).__str__()
            )


@client.event(PairStatus)
def PairStatusMessage(client: NewClient, message: PairStatus):
    print(client, message)


client.PairPhone(
    "13372922220",
    True,
)
# print(log.level)
