import logging
import os
import signal
import sys
from datetime import timedelta
from neonize.client import NewClient
from neonize.events import (
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    event,
    ReceiptEv,
    CallOfferEv,
)
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import (
    Message,
    FutureProofMessage,
    InteractiveMessage,
    MessageContextInfo,
    DeviceListMetadata,
)
from neonize.types import MessageServerID
from neonize.utils import log
from neonize.utils.enum import ReceiptType

sys.path.insert(0, os.getcwd())


def interrupted(*_):
    event.set()


log.setLevel(logging.DEBUG)
signal.signal(signal.SIGINT, interrupted)


client = NewClient("db.sqlite3")


@client.event(ConnectedEv)
def on_connected(_: NewClient, __: ConnectedEv):
    log.info("⚡ Connected")


@client.event(ReceiptEv)
def on_receipt(_: NewClient, receipt: ReceiptEv):
    log.debug(receipt)


@client.event(CallOfferEv)
def on_call(_: NewClient, call: CallOfferEv):
    log.debug(call)


@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    handler(client, message)


def handler(client: NewClient, message: MessageEv):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    match text:
        case "ping":
            client.reply_message("pong", message)
        case "_test_link_preview":
            client.send_message(
                chat, "Test https://github.com/krypton-byte/neonize", link_preview=True
            )
        case "_sticker":
            client.send_sticker(
                chat,
                "https://mystickermania.com/cdn/stickers/anime/spy-family-anya-smirk-512x512.png",
            )
        case "_sticker_exif":
            client.send_sticker(
                chat,
                "https://mystickermania.com/cdn/stickers/anime/spy-family-anya-smirk-512x512.png",
                name="@Neonize",
                packname="2024",
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
                    message.Info.ID,
                    chat=message.Info.MessageSource.Chat,
                    sender=message.Info.MessageSource.Sender,
                    receipt=ReceiptType.READ,
                ).__str__(),
            )
        case "read_channel":
            metadata = client.get_newsletter_info_with_invite(
                "https://whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M"
            )
            err = client.follow_newsletter(metadata.ID)
            client.send_message(chat, "error: " + err.__str__())
            resp = client.newsletter_mark_viewed(metadata.ID, [MessageServerID(0)])
            client.send_message(chat, resp.__str__() + "\n" + metadata.__str__())
        case "logout":
            client.logout()
        case "send_react_channel":
            metadata = client.get_newsletter_info_with_invite(
                "https://whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M"
            )
            data_msg = client.get_newsletter_messages(
                metadata.ID, 2, MessageServerID(0)
            )
            client.send_message(chat, data_msg.__str__())
            for _ in data_msg:
                client.newsletter_send_reaction(
                    metadata.ID, MessageServerID(0), "🗿", ""
                )
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
        case "set_diseapearing":
            client.send_message(
                chat, client.set_default_disappearing_timer(timedelta(days=7)).__str__()
            )
        case "test_contacts":
            client.send_message(chat, client.contact.get_all_contacts().__str__())
        case "build_sticker":
            client.send_message(
                chat,
                client.build_sticker_message(
                    "https://mystickermania.com/cdn/stickers/anime/spy-family-anya-smirk-512x512.png",
                    message,
                    "2024",
                    "neonize",
                ),
            )
        case "build_video":
            client.send_message(
                chat,
                client.build_video_message(
                    "https://download.samplelib.com/mp4/sample-5s.mp4", "Test", message
                ),
            )
        case "build_image":
            client.send_message(
                chat,
                client.build_image_message(
                    "https://download.samplelib.com/png/sample-boat-400x300.png",
                    "Test",
                    message,
                ),
            )
        case "build_document":
            client.send_message(
                chat,
                client.build_document_message(
                    "https://download.samplelib.com/xls/sample-heavy-1.xls",
                    "Test",
                    "title",
                    "sample-heavy-1.xls",
                    quoted=message,
                ),
            )
        # ChatSettingsStore
        case "put_muted_until":
            client.chat_settings.put_muted_until(chat, timedelta(seconds=5))
        case "put_pinned_enable":
            client.chat_settings.put_pinned(chat, True)
        case "put_pinned_disable":
            client.chat_settings.put_pinned(chat, False)
        case "put_archived_enable":
            client.chat_settings.put_archived(chat, True)
        case "put_archived_disable":
            client.chat_settings.put_archived(chat, False)
        case "get_chat_settings":
            client.send_message(
                chat, client.chat_settings.get_chat_settings(chat).__str__()
            )
        case "button":
            client.send_message(
                message.Info.MessageSource.Chat,
                Message(
                    viewOnceMessage=FutureProofMessage(
                        message=Message(
                            messageContextInfo=MessageContextInfo(
                                deviceListMetadata=DeviceListMetadata(),
                                deviceListMetadataVersion=2,
                            ),
                            interactiveMessage=InteractiveMessage(
                                body=InteractiveMessage.Body(text="Body Message"),
                                footer=InteractiveMessage.Footer(text="@krypton-byte"),
                                header=InteractiveMessage.Header(
                                    title="Title Message",
                                    subtitle="Subtitle Message",
                                    hasMediaAttachment=False,
                                ),
                                nativeFlowMessage=InteractiveMessage.NativeFlowMessage(
                                    buttons=[
                                        InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                            name="single_select",
                                            buttonParamsJSON='{"title":"List Buttons","sections":[{"title":"title","highlight_label":"label","rows":[{"header":"header","title":"title","description":"description","id":"select 1"},{"header":"header","title":"title","description":"description","id":"select 2"}]}]}',
                                        ),
                                        InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                            name="quick_reply",
                                            buttonParamsJSON='{"display_text":"Quick URL","url":"https://www.google.com","merchant_url":"https://www.google.com"}',
                                        ),
                                        InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                            name="cta_call",
                                            buttonParamsJSON='{"display_text":"Quick Call","id":"message"}',
                                        ),
                                        InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                            name="cta_copy",
                                            buttonParamsJSON='{"display_text":"Quick Copy","id":"123456789","copy_code":"message"}',
                                        ),
                                        InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                            name="cta_remainder",
                                            buttonParamsJSON='{"display_text":"Reminder","id":"message"}',
                                        ),
                                        InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                            name="cta_cancel_remainder",
                                            buttonParamsJSON='{"display_text":"Cancel Reminder","id":"message"}',
                                        ),
                                        InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                            name="address_message",
                                            buttonParamsJSON='{"display_text":"Address","id":"message"}',
                                        ),
                                        InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                            name="send_location", buttonParamsJSON=""
                                        ),
                                    ]
                                ),
                            ),
                        )
                    )
                ),
            )


@client.event(PairStatusEv)
def PairStatusMessage(_: NewClient, message: PairStatusEv):
    log.info(f"logged as {message.ID.User}")


client.connect()
