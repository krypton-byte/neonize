import asyncio
import logging
import os
import signal
import sys

from neonize.aioze.client import NewAClient
from neonize.aioze.events import ConnectedEv, MessageEv, PairStatusEv, event
from neonize.utils import log
from neonize.ext.interactive_message import (
    ButtonMessage,
    ButtonV2Message,
    CarouselMessage,
    AIRichMessage,
    Product,
    Reel,
    Post,
    Source,
)

sys.path.insert(0, os.getcwd())


def interrupted(*_):
    event.set()


log.setLevel(logging.DEBUG)
signal.signal(signal.SIGINT, interrupted)

client = NewAClient("db.sqlite3")


@client.event(ConnectedEv)
async def on_connected(_: NewAClient, __: ConnectedEv):
    log.info("Client connected to WhatsApp successfully.")


@client.event(MessageEv)
async def on_message(client: NewAClient, message: MessageEv):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    print(f"Received message: {text} from chat: {chat}")

    match text:
        case "_button":
            # Native flow button with image header
            msg = (
                ButtonMessage()
                .set_title("Welcome to Neonize")
                .set_subtitle("Interactive Messages")
                .set_body("Please select an action from the menu below.")
                .set_footer("Powered by Neonize Framework")
                .set_image("https://download.samplelib.com/png/sample-boat-400x300.png")
                .add_reply("Quick Reply Test", "reply_1")
                .add_url("Visit Google", "https://google.com")
                .add_copy("Copy License", "MIT License Content")
                .add_call("Call Support", "1234567890")
                .add_reminder("Set Reminder", "remind_1")
                .add_cancel_reminder("Cancel Reminder", "cancel_remind_1")
                .add_address("Address Info", "address_1")
                .add_location()
                .add_selection("More Options")
                .add_section("Main Menu", "Start Here")
                .add_row("Profile", "View your profile", "profile_id", "User")
                .add_row("Settings", "Change your preferences", "settings_id", "System")
            )
            msg = await msg.prepare_asend(client)
            await client.send_message(chat, msg)
            msg2 = (
                ButtonMessage()
                .set_title("Welcome to Neonize")
                .set_subtitle("Interactive Messages")
                .set_body("Please select an action from the menu below.")
                .set_footer("Powered by Neonize Framework")
                .set_image("https://download.samplelib.com/png/sample-boat-400x300.png")
                .add_selection("More Options")
                .add_section("Main Menu", "Start Here")
                .add_row("Profile", "View your profile", "profile_id", "User")
                .add_row("Settings", "Change your preferences", "settings_id", "System")
            )
            msg2 = await msg2.prepare_asend(client)
            await client.send_message(chat, msg2)

        case "_buttonv2":
            # Legacy buttons message with location header for thumbnail
            msg = (
                ButtonV2Message()
                .set_title("Legacy Support")
                .set_subtitle("ButtonV2 Example")
                .set_body("This uses the older button format.")
                .set_footer("Neonize Legacy")
                .set_thumbnail(
                    "https://mystickermania.com/cdn/stickers/anime/spy-family-anya-smirk-512x512.png"
                )
                .add_button("Acknowledge", "ack_1")
                .add_button("Cancel Action", "cancel_1")
            )
            msg = await msg.prepare_asend(client)
            await client.send_message(chat, msg)

        case "_carousel":
            # Horizontal scroll carousel with image and video cards
            card1 = (
                ButtonMessage()
                .set_title("Product One")
                .set_body("This is an image-based card.")
                .set_footer("Item 1")
                .set_image("https://download.samplelib.com/png/sample-boat-400x300.png")
                .add_reply("Select Item 1", "item_1")
            )

            card2 = (
                ButtonMessage()
                .set_title("Product Two")
                .set_body("This is a video-based card.")
                .set_footer("Item 2")
                .set_video("https://download.samplelib.com/mp4/sample-5s.mp4")
                .add_reply("Select Item 2", "item_2")
            )

            msg = (
                CarouselMessage()
                .set_body("Swipe through our catalog")
                .set_footer("End of catalog")
                .add_card(await card1.to_acard(client))
                .add_card(await card2.to_acard(client))
            )
            msg = await msg.prepare_asend(client)
            await client.send_message(chat, msg)

        case "_airich":
            # AI Rich response message with complex structures
            print("Preparing AI Rich Message...")
            table_data = [
                ["Name", "Version", "Status"],
                ["Neonize", "1.0", "Active"],
                ["Baileys", "6.5", "Ported"],
            ]

            msg = (
                AIRichMessage()
                .set_title("AI Assistant")
                .set_footer("Generated by Neonize Bot")
                # Showcasing markdown text with hyperlink, citation, and LaTeX rendering support
                .add_text(
                    "Hello! I am an AI assistant. I can show you [Neonize Github](https://github.com/krypton-byte/neonize) links, citations [](https://example.com), and even LaTeX formulas $2^2$ [E=mc^2|100|50|12.5|5.0]<https://upload.wikimedia.org/wikipedia/commons/2/2b/Math_formula.png>.",
                    latex=True,
                    hyperlink=True,
                    citation=True,
                )
                .add_code("python", "def hello_world():\n    print('Welcome to Neonize!')\n")
                .add_table(table_data)
                # Showcasing multiple images
                .add_image(
                    [
                        "https://download.samplelib.com/png/sample-boat-400x300.png",
                        "https://download.samplelib.com/png/sample-clouds-400x300.png",
                    ]
                )
                # Showcasing video with duration
                .add_video("https://download.samplelib.com/mp4/sample-5s.mp4", duration=5)
                # Showcasing multiple sources (renders as search results)
                .add_source(
                    [
                        Source(
                            display_name="Github",
                            url="https://github.com",
                            favicon_url="https://github.githubassets.com/favicons/favicon.png",
                        ),
                        Source(
                            display_name="Python",
                            url="https://python.org",
                            favicon_url="https://www.python.org/static/favicon.ico",
                        ),
                    ]
                )
                # Showcasing multiple products (renders as horizontal scroll cards)
                .add_product(
                    [
                        Product(
                            title="Neonize Pro",
                            brand="Neonize",
                            price="$99",
                            sale_price="$49",
                            icon_url="https://github.githubassets.com/favicons/favicon.png",
                            product_url="https://github.com/krypton-byte/neonize",
                            image_url="https://download.samplelib.com/png/sample-boat-400x300.png",
                        ),
                        Product(
                            title="Neonize Basic",
                            brand="Neonize",
                            price="$19",
                            sale_price="",
                            icon_url="https://github.githubassets.com/favicons/favicon.png",
                            product_url="https://github.com/krypton-byte/neonize",
                            image_url="https://download.samplelib.com/png/sample-clouds-400x300.png",
                        ),
                    ]
                )
                # Showcasing multiple reels
                .add_reels(
                    [
                        Reel(
                            username="dev_krypton",
                            video_url="https://download.samplelib.com/mp4/sample-5s.mp4",
                            thumbnail_url="https://download.samplelib.com/png/sample-boat-400x300.png",
                            profile_icon_url="https://github.githubassets.com/favicons/favicon.png",
                            reels_title="Neonize Update",
                            likes_count=120,
                            shares_count=15,
                            view_count=1500,
                            reel_source="IG",
                            is_verified=True,
                        ),
                        Reel(
                            username="python_dev",
                            video_url="https://download.samplelib.com/mp4/sample-5s.mp4",
                            thumbnail_url="https://download.samplelib.com/png/sample-clouds-400x300.png",
                            profile_icon_url="https://www.python.org/static/favicon.ico",
                            reels_title="Python Tip",
                            likes_count=50,
                            shares_count=5,
                            view_count=300,
                            reel_source="IG",
                            is_verified=False,
                        ),
                    ]
                )
                # Showcasing multiple posts
                .add_post(
                    [
                        Post(
                            title="Release v1.0",
                            subtitle="Out now!",
                            username="neonize_team",
                            profile_picture_url="https://github.githubassets.com/favicons/favicon.png",
                            is_verified=True,
                            thumbnail_url="https://download.samplelib.com/png/sample-boat-400x300.png",
                            post_caption="Huge update for WhatsApp bots.",
                            likes_count=500,
                            comments_count=42,
                            shares_count=10,
                            post_url="https://github.com/krypton-byte/neonize",
                            post_deeplink="https://github.com/krypton-byte/neonize",
                            source_app="INSTAGRAM",
                            footer_label="View Github",
                            footer_icon="https://github.githubassets.com/favicons/favicon.png",
                            orientation="LANDSCAPE",
                            post_type="VIDEO",
                        ),
                        Post(
                            title="Python WhatsApp",
                            subtitle="Tutorial",
                            username="py_guide",
                            profile_picture_url="https://www.python.org/static/favicon.ico",
                            is_verified=False,
                            thumbnail_url="https://download.samplelib.com/png/sample-clouds-400x300.png",
                            post_caption="Learn how to build bots.",
                            likes_count=150,
                            comments_count=12,
                            shares_count=3,
                            post_url="https://github.com",
                            post_deeplink="https://github.com",
                            source_app="INSTAGRAM",
                            footer_label="Read more",
                            footer_icon="https://www.python.org/static/favicon.ico",
                            orientation="PORTRAIT",
                            post_type="IMAGE",
                        ),
                    ]
                )
                .add_tip(
                    "Pro Tip: You can horizontally scroll through multiple products, reels, or posts!"
                )
                .add_suggest(["Wow, that's cool", "Show me the code"])
            )
            print("AI Rich Message prepared, sending now...")
            msg = await msg.prepare_asend(client)
            print("Sending AI Rich Message...")
            await client.send_message(chat, msg)
            print("AI Rich Message sent successfully.")

        case "stop":
            log.info("Stopping client...")
            await client.stop()

        case "ping":
            await client.reply_message("pong", message)


@client.event(PairStatusEv)
async def PairStatusMessage(_: NewAClient, message: PairStatusEv):
    log.info(f"Logged in as {message.ID.User}")


async def connect():
    await client.connect()
    await client.idle()


if __name__ == "__main__":
    asyncio.run(connect())
