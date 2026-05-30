"""Interactive message builders for WhatsApp via neonize.

Provides fluent-builder classes for constructing native-flow buttons,
legacy buttons (v2), carousels, and AI rich response messages.

Classes:
    - :class:`ButtonMessage` – Native-flow interactive buttons.
    - :class:`ButtonV2Message` – Legacy ``ButtonsMessage`` with location header.
    - :class:`CarouselMessage` – Horizontal-scroll card carousel.
    - :class:`AIRichMessage` – AI rich response (text, code, tables, media, etc.).

Button data classes:
    - :class:`ReplyButton`, :class:`UrlButton`, :class:`CopyButton`,
      :class:`CallButton`, :class:`ReminderButton`, :class:`CancelReminderButton`,
      :class:`AddressButton`, :class:`LocationButton`, :class:`SelectionButton`,
      :class:`Row`, :class:`Section`, :class:`ButtonV2Item`.

Base:
    - :class:`CustomInteractiveMessage` – ABC for all interactive messages.
    - :class:`InteractiveMessageBuilder` – Mixin with shared title/body/footer.
"""

from .base import CustomInteractiveMessage, InteractiveMessageBuilder
from .button import (
    AddressButton,
    ButtonMessage,
    CallButton,
    CancelReminderButton,
    CopyButton,
    LocationButton,
    ReminderButton,
    ReplyButton,
    Row,
    Section,
    SelectionButton,
    UrlButton,
)
from .buttonv2 import ButtonV2Item, ButtonV2Message
from .carousel import CarouselMessage
from .ai_rich import AIRichMessage, Product, Reel, Post, Source

__all__ = [
    # Base
    "CustomInteractiveMessage",
    "InteractiveMessageBuilder",
    # Button (native flow)
    "ButtonMessage",
    "ReplyButton",
    "UrlButton",
    "CopyButton",
    "CallButton",
    "ReminderButton",
    "CancelReminderButton",
    "AddressButton",
    "LocationButton",
    "SelectionButton",
    "Row",
    "Section",
    # ButtonV2 (legacy)
    "ButtonV2Message",
    "ButtonV2Item",
    # Carousel
    "CarouselMessage",
    # AI Rich
    "AIRichMessage",
    "Product",
    "Reel",
    "Post",
    "Source",
]
