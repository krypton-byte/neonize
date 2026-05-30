"""Legacy ``ButtonsMessage`` builder for WhatsApp.

This module ports the Baileys ``ButtonV2`` class to Python.  ``ButtonV2``
produces a ``ButtonsMessage`` protobuf (field 42 of ``Message``), which is
the older button format that uses a location header hack for attaching a
thumbnail with a title and subtitle.

Example::

    msg = (
        ButtonV2Message()
        .set_title("My Bot")
        .set_subtitle("v2 Buttons")
        .set_body("Choose an option")
        .set_footer("Powered by neonize")
        .set_thumbnail(b"<jpeg bytes>")
        .add_button("📦 Menu", ".menu")
        .add_button("👤 Profile", ".profile")
    )
    proto = msg.prepare_send(client)
    client.send_message(jid, proto)
"""

from __future__ import annotations

import uuid as _uuid
from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Self, Union

from ...proto.waE2E.WAWebProtobufsE2E_pb2 import (
    ButtonsMessage,
    ContextInfo,
    LocationMessage,
    Message,
)
from ...utils.iofile import get_bytes_from_name_or_url
from .base import CustomInteractiveMessage, InteractiveMessageBuilder

if TYPE_CHECKING:
    from ...aioze.client import NewAClient
    from ...client import NewClient


@dataclass(frozen=True, slots=True)
class ButtonV2Item:
    """A single button inside a ``ButtonsMessage``.

    :param display_text: Label shown on the button.
    :param button_id: Unique identifier for the button.
    """

    display_text: str
    button_id: str

    def to_proto(self) -> ButtonsMessage.Button:
        """Serialise to a ``ButtonsMessage.Button`` protobuf."""
        return ButtonsMessage.Button(
            buttonID=self.button_id,
            buttonText=ButtonsMessage.Button.ButtonText(displayText=self.display_text),
            type=ButtonsMessage.Button.RESPONSE,
        )


def _resize_thumbnail(data: bytes, width: int = 300, height: int = 300) -> bytes:
    """Resize an image to a square thumbnail using Pillow.

    Falls back to returning the original bytes if Pillow is unavailable.

    :param data: Raw image bytes.
    :param width: Target width.
    :param height: Target height.
    :returns: Resized PNG bytes.
    """
    try:
        from PIL import Image

        img = Image.open(BytesIO(data))
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except ImportError:
        return data


class ButtonV2Message(CustomInteractiveMessage, InteractiveMessageBuilder):
    """Fluent builder for legacy WhatsApp button messages (``ButtonsMessage``).

    This builder creates messages using the location-header hack: it sets
    ``headerType=6`` (LOCATION) and embeds the title, subtitle, and an
    optional thumbnail inside a ``LocationMessage``.
    """

    def __init__(self) -> None:
        super().__init__()
        self._buttons: List[ButtonV2Item] = []
        self._thumbnail: Optional[bytes] = None

    # -- Setters (fluent API) ------------------------------------------------

    def set_title(self, title: str) -> Self:
        """Set the header title.

        :param title: Title text.
        :returns: ``self`` for chaining.
        """
        self._title = title
        return self

    def set_subtitle(self, subtitle: str) -> Self:
        """Set the header subtitle.

        :param subtitle: Subtitle text.
        :returns: ``self`` for chaining.
        """
        self._subtitle = subtitle
        return self

    def set_body(self, body: str) -> Self:
        """Set the body text.

        :param body: Body text.
        :returns: ``self`` for chaining.
        """
        self._body = body
        return self

    def set_footer(self, footer: str) -> Self:
        """Set the footer text.

        :param footer: Footer text.
        :returns: ``self`` for chaining.
        """
        self._footer = footer
        return self

    def set_context_info(self, context_info: ContextInfo) -> Self:
        """Set context info.

        :param context_info: A ``ContextInfo`` protobuf instance.
        :returns: ``self`` for chaining.
        """
        self._context_info = context_info
        return self

    def set_thumbnail(self, thumbnail: Union[str, bytes]) -> Self:
        """Set a thumbnail image for the location header.

        :param thumbnail: URL string or raw image bytes.
        :returns: ``self`` for chaining.
        """
        raw = get_bytes_from_name_or_url(thumbnail) if isinstance(thumbnail, str) else thumbnail
        self._thumbnail = _resize_thumbnail(raw)
        return self

    # -- Button adders -------------------------------------------------------

    def add_button(self, display_text: str, button_id: Optional[str] = None) -> Self:
        """Add a response button.

        :param display_text: Label on the button.
        :param button_id: Unique identifier; auto-generated if omitted.
        :returns: ``self`` for chaining.
        """
        self._buttons.append(
            ButtonV2Item(
                display_text=display_text,
                button_id=button_id or str(_uuid.uuid4()),
            )
        )
        return self

    # -- Build logic ---------------------------------------------------------

    def _build_buttons_message(self) -> ButtonsMessage:
        """Assemble the ``ButtonsMessage`` protobuf."""
        msg = ButtonsMessage(
            contentText=self._body,
            footerText=self._footer,
            headerType=ButtonsMessage.LOCATION,
            locationMessage=LocationMessage(
                degreesLatitude=0.0,
                degreesLongitude=0.0,
                name=self._title,
                address=self._subtitle,
                JPEGThumbnail=self._thumbnail or b"",
            ),
            buttons=[btn.to_proto() for btn in self._buttons],
        )
        if self._context_info is not None:
            msg.contextInfo.MergeFrom(self._context_info)
        return msg

    # -- CustomInteractiveMessage contract -----------------------------------

    def prepare_send(self, client: "NewClient") -> Message:
        """Build the full ``Message`` protobuf (synchronous).

        :param client: The synchronous neonize client.
        :raises ValueError: If no buttons have been added.
        :returns: A ``Message`` containing the buttons payload.
        """
        if not self._buttons:
            raise ValueError("ButtonV2Message requires at least one button.")
        return Message(buttonsMessage=self._build_buttons_message())

    async def prepare_asend(self, client: "NewAClient") -> Message:
        """Build the full ``Message`` protobuf (asynchronous).

        :param client: The asynchronous neonize client.
        :raises ValueError: If no buttons have been added.
        :returns: A ``Message`` containing the buttons payload.
        """
        if not self._buttons:
            raise ValueError("ButtonV2Message requires at least one button.")
        return Message(buttonsMessage=self._build_buttons_message())
