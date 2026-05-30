"""Base classes for interactive WhatsApp message builders.

This module provides the foundational abstractions for building interactive
messages (buttons, carousels, AI rich responses) compatible with the neonize
WhatsApp client. All interactive message types inherit from
:class:`CustomInteractiveMessage` and implement the ``prepare_send`` /
``prepare_asend`` contract so that the client layer can serialise them to
protobuf and relay them transparently.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional

from ...proto.waE2E.WAWebProtobufsE2E_pb2 import (
    ContextInfo,
    Message,
)

if TYPE_CHECKING:
    from ...aioze.client import NewAClient
    from ...client import NewClient


class CustomInteractiveMessage(ABC):
    """Abstract base for all interactive message types.

    Subclasses must implement :meth:`prepare_send` (synchronous) and
    :meth:`prepare_asend` (asynchronous).  Both methods receive the
    appropriate client instance and must return a fully-constructed
    :class:`Message` protobuf ready for ``client.send_message``.
    """

    @abstractmethod
    def prepare_send(self, client: "NewClient") -> Message:
        """Build the protobuf ``Message`` synchronously.

        :param client: The synchronous neonize client instance.
        :returns: A ``Message`` protobuf ready for sending.
        """
        ...

    @abstractmethod
    async def prepare_asend(self, client: "NewAClient") -> Message:
        """Build the protobuf ``Message`` asynchronously.

        :param client: The asynchronous neonize client instance.
        :returns: A ``Message`` protobuf ready for sending.
        """
        ...


class InteractiveMessageBuilder(ABC):
    """Mixin providing common header / body / footer / contextInfo fields.

    All concrete interactive message builders (Button, ButtonV2, Carousel,
    AIRich) extend this class so that ``set_title``, ``set_body``, etc. are
    available with a fluent-chaining API.
    """

    def __init__(self) -> None:
        self._title: str = ""
        self._subtitle: str = ""
        self._body: str = ""
        self._footer: str = ""
        self._context_info: Optional[ContextInfo] = None
