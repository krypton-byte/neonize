"""Carousel message builder for WhatsApp.

This module ports the Baileys ``Carousel`` class to Python, producing an
``InteractiveMessage`` with a ``CarouselMessage`` payload that contains
multiple cards.  Each card is itself an ``InteractiveMessage`` obtained
from :meth:`ButtonMessage.to_card`.

Example::

    card1 = (
        ButtonMessage()
        .set_title("🍔 Burger")
        .set_body("Delicious burger")
        .set_footer("$5")
        .set_image("https://example.com/burger.jpg")
        .add_reply("🛒 Buy", ".buy_burger")
    )
    card2 = (
        ButtonMessage()
        .set_title("🍕 Pizza")
        .set_body("Mozzarella pizza")
        .set_footer("$7")
        .set_image("https://example.com/pizza.jpg")
        .add_reply("🛒 Buy", ".buy_pizza")
    )

    msg = (
        CarouselMessage()
        .set_body("🛍️ Product List")
        .set_footer("Swipe to see more")
        .add_card(card1.to_card(client))
        .add_card(card2.to_card(client))
    )
    proto = msg.prepare_send(client)
    client.send_message(jid, proto)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Self, Sequence, Union

from ...proto.waE2E.WAWebProtobufsE2E_pb2 import (
    ContextInfo,
    InteractiveMessage,
    Message,
)
from .base import CustomInteractiveMessage, InteractiveMessageBuilder

if TYPE_CHECKING:
    from ...aioze.client import NewAClient
    from ...client import NewClient


class CarouselMessage(CustomInteractiveMessage, InteractiveMessageBuilder):
    """Fluent builder for WhatsApp carousel (horizontal-scroll card) messages.

    A carousel message wraps multiple ``InteractiveMessage`` cards inside a
    ``CarouselMessage`` protobuf.  Each card **must** have a header with
    media (image or video), otherwise WhatsApp will reject it.
    """

    def __init__(self) -> None:
        super().__init__()
        self._cards: List[InteractiveMessage] = []

    # -- Setters (fluent API) ------------------------------------------------

    def set_body(self, body: str) -> Self:
        """Set the carousel body text.

        :param body: Body text.
        :returns: ``self`` for chaining.
        """
        self._body = body
        return self

    def set_footer(self, footer: str) -> Self:
        """Set the carousel footer text.

        :param footer: Footer text.
        :returns: ``self`` for chaining.
        """
        self._footer = footer
        return self

    def set_context_info(self, context_info: ContextInfo) -> Self:
        """Set context info (for quoting, mentions, etc.).

        :param context_info: A ``ContextInfo`` protobuf instance.
        :returns: ``self`` for chaining.
        """
        self._context_info = context_info
        return self

    # -- Card management -----------------------------------------------------

    def add_card(self, card: Union[InteractiveMessage, Sequence[InteractiveMessage]]) -> Self:
        """Append one or more cards to the carousel.

        Each card must have ``header.hasMediaAttachment`` set to ``True``.

        :param card: A single ``InteractiveMessage`` or a sequence of them.
        :raises ValueError: If any card lacks a media attachment in its header.
        :returns: ``self`` for chaining.
        """
        cards = list(card) if isinstance(card, (list, tuple)) else [card]
        for idx, c in enumerate(cards):
            if not c.header.hasMediaAttachment:
                raise ValueError(
                    f"Card [{len(self._cards) + idx}] must include an image or "
                    f"video in its header (hasMediaAttachment must be True)."
                )
        self._cards.extend(cards)
        return self

    # -- Build logic ---------------------------------------------------------

    def _build_interactive_message(self) -> InteractiveMessage:
        """Assemble the ``InteractiveMessage`` with ``CarouselMessage``."""
        interactive = InteractiveMessage(
            header=InteractiveMessage.Header(hasMediaAttachment=False),
            body=InteractiveMessage.Body(text=self._body),
            footer=InteractiveMessage.Footer(text=self._footer),
            carouselMessage=InteractiveMessage.CarouselMessage(cards=self._cards),
        )
        if self._context_info is not None:
            interactive.contextInfo.MergeFrom(self._context_info)
        return interactive

    # -- CustomInteractiveMessage contract -----------------------------------

    def prepare_send(self, client: "NewClient") -> Message:
        """Build the full ``Message`` protobuf (synchronous).

        :param client: The synchronous neonize client.
        :returns: A ``Message`` containing the carousel payload.
        """
        return Message(interactiveMessage=self._build_interactive_message())

    async def prepare_asend(self, client: "NewAClient") -> Message:
        """Build the full ``Message`` protobuf (asynchronous).

        :param client: The asynchronous neonize client.
        :returns: A ``Message`` containing the carousel payload.
        """
        return Message(interactiveMessage=self._build_interactive_message())
