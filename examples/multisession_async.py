import asyncio
import logging
import os
import sys
from datetime import timedelta
from neonize.aioze.client import ClientFactory, NewAClient
from neonize.aioze.events import (
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    ReceiptEv,
    event,
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
import signal


sys.path.insert(0, os.getcwd())


def interrupted(*_):
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(ClientFactory.stop(), loop)


log.setLevel(logging.DEBUG)
signal.signal(signal.SIGINT, interrupted)


client_factory = ClientFactory("db.sqlite3")

# create clients from preconfigured sessions
sessions = client_factory.get_all_devices()
for device in sessions:
    client_factory.new_client(device.JID)
# if new_client jid parameter is not passed, it will create a new client

# or create a new client
# from uuid import uuid4
# client_factory.new_client(uuid=uuid4().hex[:5])


@client_factory.event(ConnectedEv)
async def on_connected(_: NewAClient, __: ConnectedEv):
    log.info("⚡ Connected")


@client_factory.event(ReceiptEv)
async def on_receipt(_: NewAClient, receipt: ReceiptEv):
    log.debug(receipt)


@client_factory.event(CallOfferEv)
async def on_call(_: NewAClient, call: CallOfferEv):
    log.debug(call)


@client_factory.event(MessageEv)
async def on_message(client: NewAClient, message: MessageEv):
    await handler(client, message)


async def handler(client: NewAClient, message: MessageEv):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    match text:
        case "ping":
            await client.reply_message("pong", message)
        case "_test_link_preview":
            await client.send_message(
                chat, "Test https://github.com/krypton-byte/neonize", link_preview=True
            )
        case "stop_all":
            await client_factory.stop()
        case "_sticker":
            await client.send_sticker(
                chat,
                "https://mystickermania.com/cdn/stickers/anime/spy-family-anya-smirk-512x512.png",
            )
        case "_sticker_exif":
            await client.send_sticker(
                chat,
                "https://mystickermania.com/cdn/stickers/anime/spy-family-anya-smirk-512x512.png",
                name="@Neonize",
                packname="2024",
            )
        case "_image":
            await client.send_image(
                chat,
                "https://download.samplelib.com/png/sample-boat-400x300.png",
                caption="Test",
                quoted=message,
            )
        case "_video":
            await client.send_video(
                chat,
                "https://download.samplelib.com/mp4/sample-5s.mp4",
                caption="Test",
                quoted=message,
            )
        case "wait":
            await client.send_message(chat, "Waiting for 5 seconds...")
            await asyncio.sleep(5)
            await client.send_message(chat, "Done waiting!")
        case "shutdown":
            event.set()
        case "_audio":
            await client.send_audio(
                chat,
                "https://download.samplelib.com/mp3/sample-12s.mp3",
                quoted=message,
            )
        case "_ptt":
            await client.send_audio(
                chat,
                "https://download.samplelib.com/mp3/sample-12s.mp3",
                ptt=True,
                quoted=message,
            )
        case "_doc":
            await client.send_document(
                chat,
                "https://download.samplelib.com/xls/sample-heavy-1.xls",
                caption="Test",
                filename="test.xls",
                quoted=message,
            )
        case "debug":
            await client.send_message(chat, message.__str__())
        case "viewonce":
            await client.send_image(
                chat,
                "https://pbs.twimg.com/media/GC3ywBMb0AAAEWO?format=jpg&name=medium",
                viewonce=True,
            )
        case "profile_pict":
            await client.send_message(chat, (await client.get_profile_picture(chat)).__str__())
        case "status_privacy":
            await client.send_message(chat, (await client.get_status_privacy()).__str__())
        case "read":
            await client.send_message(
                chat,
                (
                    await client.mark_read(
                        message.Info.ID,
                        chat=message.Info.MessageSource.Chat,
                        sender=message.Info.MessageSource.Sender,
                        receipt=ReceiptType.READ,
                    )
                ).__str__(),
            )
        case "read_channel":
            metadata = await client.get_newsletter_info_with_invite(
                "https://whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M"
            )
            err = await client.follow_newsletter(metadata.ID)
            await client.send_message(chat, "error: " + err.__str__())
            resp = await client.newsletter_mark_viewed(metadata.ID, [MessageServerID(0)])
            await client.send_message(chat, resp.__str__() + "\n" + metadata.__str__())
        case "logout":
            await client.logout()
        case "send_react_channel":
            metadata = await client.get_newsletter_info_with_invite(
                "https://whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M"
            )
            data_msg = await client.get_newsletter_messages(metadata.ID, 2, MessageServerID(0))
            await client.send_message(chat, data_msg.__str__())
            for _ in data_msg:
                await client.newsletter_send_reaction(metadata.ID, MessageServerID(0), "🗿", "")
        case "subscribe_channel_updates":
            metadata = await client.get_newsletter_info_with_invite(
                "https://whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M"
            )
            result = await client.newsletter_subscribe_live_updates(metadata.ID)
            await client.send_message(chat, result.__str__())
        case "mute_channel":
            metadata = await client.get_newsletter_info_with_invite(
                "https://whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M"
            )
            await client.send_message(
                chat,
                (await client.newsletter_toggle_mute(metadata.ID, False)).__str__(),
            )
        case "set_diseapearing":
            await client.send_message(
                chat,
                (await client.set_default_disappearing_timer(timedelta(days=7))).__str__(),
            )
        case "test_contacts":
            await client.send_message(chat, (await client.contact.get_all_contacts()).__str__())
        case "build_sticker":
            await client.send_message(
                chat,
                await client.build_sticker_message(
                    "https://mystickermania.com/cdn/stickers/anime/spy-family-anya-smirk-512x512.png",
                    message,
                    "2024",
                    "neonize",
                ),
            )
        case "build_video":
            await client.send_message(
                chat,
                await client.build_video_message(
                    "https://download.samplelib.com/mp4/sample-5s.mp4", "Test", message
                ),
            )
        case "build_image":
            await client.send_message(
                chat,
                await client.build_image_message(
                    "https://download.samplelib.com/png/sample-boat-400x300.png",
                    "Test",
                    message,
                ),
            )
        case "build_document":
            await client.send_message(
                chat,
                await client.build_document_message(
                    "https://download.samplelib.com/xls/sample-heavy-1.xls",
                    "Test",
                    "title",
                    "sample-heavy-1.xls",
                    quoted=message,
                ),
            )
        # ChatSettingsStore
        case "put_muted_until":
            await client.chat_settings.put_muted_until(chat, timedelta(seconds=5))
        case "put_pinned_enable":
            await client.chat_settings.put_pinned(chat, True)
        case "put_pinned_disable":
            await client.chat_settings.put_pinned(chat, False)
        case "put_archived_enable":
            await client.chat_settings.put_archived(chat, True)
        case "put_archived_disable":
            await client.chat_settings.put_archived(chat, False)
        case "get_chat_settings":
            await client.send_message(
                chat, (await client.chat_settings.get_chat_settings(chat)).__str__()
            )
        case "button":
            await client.send_message(
                message.Info.MessageSource.Chat,
                Message(
                    viewOnceMessage=FutureProofMessage(
                        message=Message(
                            messageContextInfo=MessageContextInfo(
                                deviceListMetadata=DeviceListMetadata(),
                                deviceListMetadataVersion=2,
                            ),
                            interactiveMessage=InteractiveMessage(
                                body=InteractiveMessage.Body(
                                    text="Body Message"),
                                footer=InteractiveMessage.Footer(
                                    text="@krypton-byte"),
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


@client_factory.event(PairStatusEv)
async def PairStatusMessage(_: NewAClient, message: PairStatusEv):
    log.info(f"logged as {message.ID.User}")


async def run_factory():
    await client_factory.run()
    # Do something else
    await client_factory.idle_all()


if __name__ == "__main__":
    # all created clients will be automatically logged in and receive all
    # events
    client_factory.loop.run_until_complete(run_factory())
