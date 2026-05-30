"""Interactive button message builders for WhatsApp native-flow buttons.

This module ports the Baileys ``Button`` class to Python, providing a fluent
builder API for constructing native-flow interactive messages that support
quick-reply buttons, URL buttons, copy buttons, call buttons, selection
lists, reminder buttons, address messages, and location requests.

The resulting ``Message`` protobuf wraps an ``InteractiveMessage`` with a
``NativeFlowMessage`` payload.

Example::

    msg = (
        ButtonMessage()
        .set_title("Menu")
        .set_subtitle("Pick an option")
        .set_body("What would you like to do?")
        .set_footer("© MyBot")
        .add_reply("📦 Menu", ".menu")
        .add_reply("👤 Profile", ".profile")
        .add_url("🌐 Website", "https://example.com")
        .add_selection("📚 Categories")
        .add_section("Main")
        .add_row("Downloader", "Download media", ".dl")
        .add_section("Tools")
        .add_row("AI Chat", "Chat with AI", ".ai")
    )
    proto = msg.prepare_send(client)
    client.send_message(jid, proto)
"""

from __future__ import annotations

import json
import uuid as _uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Self, Union

from ...proto.waE2E.WAWebProtobufsE2E_pb2 import (
    ContextInfo,
    ImageMessage,
    InteractiveMessage,
    Message,
    VideoMessage,
    DocumentMessage,
)
from ...utils.iofile import get_bytes_from_name_or_url
from .base import CustomInteractiveMessage, InteractiveMessageBuilder

if TYPE_CHECKING:
    from ...aioze.client import NewAClient
    from ...client import NewClient


# ---------------------------------------------------------------------------
# Button data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ReplyButton:
    """A quick-reply button that sends a text response when tapped.

    :param display_text: Label shown on the button.
    :param id: Identifier returned when the button is tapped.
    """

    display_text: str
    id: str
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_native_flow(self) -> InteractiveMessage.NativeFlowMessage.NativeFlowButton:
        """Serialise to a ``NativeFlowButton`` protobuf."""
        params = {"display_text": self.display_text, "id": self.id, **self.extra}
        return InteractiveMessage.NativeFlowMessage.NativeFlowButton(
            name="quick_reply",
            buttonParamsJSON=json.dumps(params),
        )


@dataclass(frozen=True, slots=True)
class UrlButton:
    """A CTA-URL button that opens a link when tapped.

    :param display_text: Label shown on the button.
    :param url: The URL to open.
    :param webview_interaction: Whether to open inside a webview.
    """

    display_text: str
    url: str
    webview_interaction: bool = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_native_flow(self) -> InteractiveMessage.NativeFlowMessage.NativeFlowButton:
        params = {
            "display_text": self.display_text,
            "url": self.url,
            "webview_interaction": self.webview_interaction,
            **self.extra,
        }
        return InteractiveMessage.NativeFlowMessage.NativeFlowButton(
            name="cta_url",
            buttonParamsJSON=json.dumps(params),
        )


@dataclass(frozen=True, slots=True)
class CopyButton:
    """A CTA-copy button that copies a code to the clipboard.

    :param display_text: Label shown on the button.
    :param copy_code: The text to copy.
    """

    display_text: str
    copy_code: str
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_native_flow(self) -> InteractiveMessage.NativeFlowMessage.NativeFlowButton:
        params = {"display_text": self.display_text, "copy_code": self.copy_code, **self.extra}
        return InteractiveMessage.NativeFlowMessage.NativeFlowButton(
            name="cta_copy",
            buttonParamsJSON=json.dumps(params),
        )


@dataclass(frozen=True, slots=True)
class CallButton:
    """A CTA-call button that initiates a phone call.

    :param display_text: Label shown on the button.
    :param id: Phone number or identifier for the call.
    """

    display_text: str
    id: str
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_native_flow(self) -> InteractiveMessage.NativeFlowMessage.NativeFlowButton:
        params = {"display_text": self.display_text, "id": self.id, **self.extra}
        return InteractiveMessage.NativeFlowMessage.NativeFlowButton(
            name="cta_call",
            buttonParamsJSON=json.dumps(params),
        )


@dataclass(frozen=True, slots=True)
class ReminderButton:
    """A CTA-reminder button.

    :param display_text: Label shown on the button.
    :param id: Identifier for the reminder action.
    """

    display_text: str
    id: str
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_native_flow(self) -> InteractiveMessage.NativeFlowMessage.NativeFlowButton:
        params = {"display_text": self.display_text, "id": self.id, **self.extra}
        return InteractiveMessage.NativeFlowMessage.NativeFlowButton(
            name="cta_reminder",
            buttonParamsJSON=json.dumps(params),
        )


@dataclass(frozen=True, slots=True)
class CancelReminderButton:
    """A CTA-cancel-reminder button.

    :param display_text: Label shown on the button.
    :param id: Identifier for the cancel-reminder action.
    """

    display_text: str
    id: str
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_native_flow(self) -> InteractiveMessage.NativeFlowMessage.NativeFlowButton:
        params = {"display_text": self.display_text, "id": self.id, **self.extra}
        return InteractiveMessage.NativeFlowMessage.NativeFlowButton(
            name="cta_cancel_reminder",
            buttonParamsJSON=json.dumps(params),
        )


@dataclass(frozen=True, slots=True)
class AddressButton:
    """An address-message button.

    :param display_text: Label shown on the button.
    :param id: Identifier for the address action.
    """

    display_text: str
    id: str
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_native_flow(self) -> InteractiveMessage.NativeFlowMessage.NativeFlowButton:
        params = {"display_text": self.display_text, "id": self.id, **self.extra}
        return InteractiveMessage.NativeFlowMessage.NativeFlowButton(
            name="address_message",
            buttonParamsJSON=json.dumps(params),
        )


@dataclass(frozen=True, slots=True)
class LocationButton:
    """A send-location button that requests the user's location.

    :param extra: Optional additional parameters.
    """

    extra: Dict[str, Any] = field(default_factory=dict)

    def to_native_flow(self) -> InteractiveMessage.NativeFlowMessage.NativeFlowButton:
        return InteractiveMessage.NativeFlowMessage.NativeFlowButton(
            name="send_location",
            buttonParamsJSON=json.dumps(self.extra),
        )


@dataclass(frozen=True, slots=True)
class Row:
    """A single row inside a selection section.

    :param title: The primary title of the row.
    :param description: A short description displayed below the title.
    :param id: The identifier returned when this row is selected.
    :param header: An optional header displayed above the title.
    """

    title: str
    description: str = ""
    id: str = ""
    header: str = ""


@dataclass(slots=True)
class Section:
    """A section within a selection list.

    :param title: The section header label.
    :param rows: The rows belonging to this section.
    :param highlight_label: An optional highlight label.
    """

    title: str = ""
    highlight_label: str = ""
    rows: List[Row] = field(default_factory=list)

    def add_row(
        self,
        title: str,
        description: str = "",
        id: str = "",
        header: str = "",
    ) -> "Section":
        """Append a row to this section.

        :returns: ``self`` for fluent chaining.
        """
        self.rows.append(Row(title=title, description=description, id=id, header=header))
        return self


# Type alias for any button variant
ButtonType = Union[
    ReplyButton,
    UrlButton,
    CopyButton,
    CallButton,
    ReminderButton,
    CancelReminderButton,
    AddressButton,
    LocationButton,
]


# ---------------------------------------------------------------------------
# SelectionButton  – manages the single_select native-flow button
# ---------------------------------------------------------------------------


class SelectionButton:
    """A selection list button that contains sections and rows.

    :param title: The title of the selection list.
    """

    def __init__(self, title: str) -> None:
        self.title = title
        self.sections: List[Section] = []
        self._current_section_index: int = -1

    def add_section(self, title: str = "", highlight_label: str = "") -> "SelectionButton":
        """Add a new section to the selection list.

        :param title: Section header text.
        :param highlight_label: Optional highlight label.
        :returns: ``self`` for fluent chaining.
        """
        self.sections.append(Section(title=title, highlight_label=highlight_label))
        self._current_section_index = len(self.sections) - 1
        return self

    def add_row(
        self,
        title: str,
        description: str = "",
        id: str = "",
        header: str = "",
    ) -> "SelectionButton":
        """Add a row to the current section.

        :raises RuntimeError: If no section has been created yet.
        :returns: ``self`` for fluent chaining.
        """
        if self._current_section_index < 0:
            raise RuntimeError("You must create a section before adding rows.")
        self.sections[self._current_section_index].add_row(title, description, id, header)
        return self

    def to_native_flow(self) -> InteractiveMessage.NativeFlowMessage.NativeFlowButton:
        """Serialise to a ``NativeFlowButton`` protobuf."""
        sections_data = [
            {
                "title": s.title,
                "highlight_label": s.highlight_label,
                "rows": [
                    {"header": r.header, "title": r.title, "description": r.description, "id": r.id}
                    for r in s.rows
                ],
            }
            for s in self.sections
        ]
        params = {"title": self.title, "sections": sections_data}
        return InteractiveMessage.NativeFlowMessage.NativeFlowButton(
            name="single_select",
            buttonParamsJSON=json.dumps(params),
        )


# ---------------------------------------------------------------------------
# ButtonMessage  – the main builder
# ---------------------------------------------------------------------------


class ButtonMessage(CustomInteractiveMessage, InteractiveMessageBuilder):
    """Fluent builder for WhatsApp native-flow interactive button messages.

    This class constructs a ``Message`` containing an ``InteractiveMessage``
    with a ``NativeFlowMessage`` payload.  It supports images, videos, and
    documents as header media.

    Usage follows the **builder pattern** – every setter returns ``self``
    so calls can be chained::

        msg = (
            ButtonMessage()
            .set_title("Hello")
            .set_body("World")
            .add_reply("OK", "ok_id")
        )
    """

    def __init__(self) -> None:
        super().__init__()
        self._buttons: List[Union[ButtonType, SelectionButton]] = []
        self._media: Optional[bytes] = None
        self._media_type: Optional[str] = None  # "image", "video", "document"
        self._media_mimetype: Optional[str] = None
        self._params: Dict[str, Any] = {}

    # -- Setters (fluent API) ------------------------------------------------

    def set_title(self, title: str) -> Self:
        """Set the header title text.

        :param title: The title string.
        :returns: ``self`` for chaining.
        """
        self._title = title
        return self

    def set_subtitle(self, subtitle: str) -> Self:
        """Set the header subtitle text.

        :param subtitle: The subtitle string.
        :returns: ``self`` for chaining.
        """
        self._subtitle = subtitle
        return self

    def set_body(self, body: str) -> Self:
        """Set the message body text.

        :param body: The body string.
        :returns: ``self`` for chaining.
        """
        self._body = body
        return self

    def set_footer(self, footer: str) -> Self:
        """Set the footer text.

        :param footer: The footer string.
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

    def set_params(self, params: Dict[str, Any]) -> Self:
        """Set native-flow message-level parameters.

        :param params: A dictionary of parameters to be serialised as JSON.
        :returns: ``self`` for chaining.
        """
        self._params = params
        return self

    # -- Media setters -------------------------------------------------------

    def set_image(self, image: Union[str, bytes]) -> Self:
        """Attach an image to the message header.

        :param image: URL string or raw bytes of the image.
        :returns: ``self`` for chaining.
        """
        self._media = get_bytes_from_name_or_url(image) if isinstance(image, str) else image
        self._media_type = "image"
        return self

    def set_video(self, video: Union[str, bytes]) -> Self:
        """Attach a video to the message header.

        :param video: URL string or raw bytes of the video.
        :returns: ``self`` for chaining.
        """
        self._media = get_bytes_from_name_or_url(video) if isinstance(video, str) else video
        self._media_type = "video"
        return self

    def set_document(self, document: Union[str, bytes], mimetype: str = "application/pdf") -> Self:
        """Attach a document to the message header.

        :param document: URL string or raw bytes of the document.
        :param mimetype: MIME type of the document.
        :returns: ``self`` for chaining.
        """
        self._media = (
            get_bytes_from_name_or_url(document) if isinstance(document, str) else document
        )
        self._media_type = "document"
        self._media_mimetype = mimetype
        return self

    # -- Button adders -------------------------------------------------------

    def add_reply(self, display_text: str, id: str, **extra: Any) -> Self:
        """Add a quick-reply button.

        :param display_text: Button label.
        :param id: Identifier returned on tap.
        :returns: ``self`` for chaining.
        """
        self._buttons.append(ReplyButton(display_text=display_text, id=id, extra=extra))
        return self

    def add_url(
        self,
        display_text: str,
        url: str,
        webview_interaction: bool = False,
        **extra: Any,
    ) -> Self:
        """Add a CTA-URL button.

        :param display_text: Button label.
        :param url: URL to open.
        :param webview_interaction: Open in webview if ``True``.
        :returns: ``self`` for chaining.
        """
        self._buttons.append(
            UrlButton(
                display_text=display_text,
                url=url,
                webview_interaction=webview_interaction,
                extra=extra,
            )
        )
        return self

    def add_copy(self, display_text: str, copy_code: str, **extra: Any) -> Self:
        """Add a CTA-copy button.

        :param display_text: Button label.
        :param copy_code: Text to copy to clipboard.
        :returns: ``self`` for chaining.
        """
        self._buttons.append(
            CopyButton(display_text=display_text, copy_code=copy_code, extra=extra)
        )
        return self

    def add_call(self, display_text: str, id: str, **extra: Any) -> Self:
        """Add a CTA-call button.

        :param display_text: Button label.
        :param id: Phone number or call identifier.
        :returns: ``self`` for chaining.
        """
        self._buttons.append(CallButton(display_text=display_text, id=id, extra=extra))
        return self

    def add_reminder(self, display_text: str, id: str, **extra: Any) -> Self:
        """Add a CTA-reminder button.

        :param display_text: Button label.
        :param id: Reminder identifier.
        :returns: ``self`` for chaining.
        """
        self._buttons.append(ReminderButton(display_text=display_text, id=id, extra=extra))
        return self

    def add_cancel_reminder(self, display_text: str, id: str, **extra: Any) -> Self:
        """Add a CTA-cancel-reminder button.

        :param display_text: Button label.
        :param id: Reminder identifier to cancel.
        :returns: ``self`` for chaining.
        """
        self._buttons.append(CancelReminderButton(display_text=display_text, id=id, extra=extra))
        return self

    def add_address(self, display_text: str, id: str, **extra: Any) -> Self:
        """Add an address-message button.

        :param display_text: Button label.
        :param id: Address identifier.
        :returns: ``self`` for chaining.
        """
        self._buttons.append(AddressButton(display_text=display_text, id=id, extra=extra))
        return self

    def add_location(self, **extra: Any) -> Self:
        """Add a send-location button.

        :returns: ``self`` for chaining.
        """
        self._buttons.append(LocationButton(extra=extra))
        return self

    # -- Selection (list) API -----------------------------------------------

    def add_selection(self, title: str) -> Self:
        """Add a selection list button and make it the active selection.

        Subsequent :meth:`add_section` and :meth:`add_row` calls operate on
        the most recently added selection.

        :param title: Title of the selection list.
        :returns: ``self`` for chaining.
        """
        self._buttons.append(SelectionButton(title=title))
        return self

    def add_section(self, title: str = "", highlight_label: str = "") -> Self:
        """Add a section to the current (last-added) selection list.

        :param title: Section header.
        :param highlight_label: Optional highlight label.
        :raises RuntimeError: If no selection has been added yet.
        :returns: ``self`` for chaining.
        """
        selection = self._get_current_selection()
        selection.add_section(title, highlight_label)
        return self

    def add_row(
        self,
        title: str,
        description: str = "",
        id: str = "",
        header: str = "",
    ) -> Self:
        """Add a row to the current section of the current selection list.

        :param title: Row title.
        :param description: Row description.
        :param id: Row identifier.
        :param header: Optional row header.
        :raises RuntimeError: If no selection or section has been added yet.
        :returns: ``self`` for chaining.
        """
        selection = self._get_current_selection()
        selection.add_row(title, description, id, header)
        return self

    def clear_buttons(self) -> Self:
        """Remove all buttons.

        :returns: ``self`` for chaining.
        """
        self._buttons.clear()
        return self

    # -- Internal helpers ----------------------------------------------------

    def _get_current_selection(self) -> SelectionButton:
        """Return the last-added ``SelectionButton``, or raise."""
        for btn in reversed(self._buttons):
            if isinstance(btn, SelectionButton):
                return btn
        raise RuntimeError("You must call add_selection() before add_section() / add_row().")

    def _build_header(
        self,
        uploaded_media: Optional[Dict[str, Any]] = None,
    ) -> InteractiveMessage.Header:
        """Construct the ``InteractiveMessage.Header`` protobuf.

        :param uploaded_media: A dict containing upload result fields (url,
            DirectPath, FileEncSHA256, etc.) or ``None``.
        """
        header = InteractiveMessage.Header(
            title=self._title,
            subtitle=self._subtitle,
            hasMediaAttachment=self._media is not None,
        )
        if uploaded_media is not None and self._media_type is not None:
            if self._media_type == "image":
                header.imageMessage.MergeFrom(
                    ImageMessage(
                        URL=uploaded_media["url"],
                        directPath=uploaded_media["DirectPath"],
                        fileEncSHA256=uploaded_media["FileEncSHA256"],
                        fileLength=uploaded_media["FileLength"],
                        fileSHA256=uploaded_media["FileSHA256"],
                        mediaKey=uploaded_media["MediaKey"],
                        mimetype=uploaded_media.get("mimetype", "image/jpeg"),
                    )
                )
            elif self._media_type == "video":
                header.videoMessage.MergeFrom(
                    VideoMessage(
                        URL=uploaded_media["url"],
                        directPath=uploaded_media["DirectPath"],
                        fileEncSHA256=uploaded_media["FileEncSHA256"],
                        fileLength=uploaded_media["FileLength"],
                        fileSHA256=uploaded_media["FileSHA256"],
                        mediaKey=uploaded_media["MediaKey"],
                        mimetype=uploaded_media.get("mimetype", "video/mp4"),
                    )
                )
            elif self._media_type == "document":
                header.documentMessage.MergeFrom(
                    DocumentMessage(
                        URL=uploaded_media["url"],
                        directPath=uploaded_media["DirectPath"],
                        fileEncSHA256=uploaded_media["FileEncSHA256"],
                        fileLength=uploaded_media["FileLength"],
                        fileSHA256=uploaded_media["FileSHA256"],
                        mediaKey=uploaded_media["MediaKey"],
                        mimetype=uploaded_media.get(
                            "mimetype", self._media_mimetype or "application/pdf"
                        ),
                    )
                )
        return header

    def _upload_media(self, client: "NewClient") -> Optional[Dict[str, Any]]:
        """Upload the attached media using the synchronous client."""
        if self._media is None:
            return None
        import magic as _magic

        upload = client.upload(self._media)
        return {
            "url": upload.url,
            "DirectPath": upload.DirectPath,
            "FileEncSHA256": upload.FileEncSHA256,
            "FileLength": upload.FileLength,
            "FileSHA256": upload.FileSHA256,
            "MediaKey": upload.MediaKey,
            "mimetype": _magic.from_buffer(self._media, mime=True),
        }

    async def _aupload_media(self, client: "NewAClient") -> Optional[Dict[str, Any]]:
        """Upload the attached media using the asynchronous client."""
        if self._media is None:
            return None
        import magic as _magic

        upload = await client.upload(self._media)
        return {
            "url": upload.url,
            "DirectPath": upload.DirectPath,
            "FileEncSHA256": upload.FileEncSHA256,
            "FileLength": upload.FileLength,
            "FileSHA256": upload.FileSHA256,
            "MediaKey": upload.MediaKey,
            "mimetype": _magic.from_buffer(self._media, mime=True),
        }

    def _build_native_flow_buttons(
        self,
    ) -> List[InteractiveMessage.NativeFlowMessage.NativeFlowButton]:
        """Convert all internal buttons to ``NativeFlowButton`` protobufs."""
        return [btn.to_native_flow() for btn in self._buttons]

    def _build_interactive_message(
        self,
        uploaded_media: Optional[Dict[str, Any]] = None,
    ) -> InteractiveMessage:
        """Assemble the ``InteractiveMessage`` protobuf."""
        interactive = InteractiveMessage(
            header=self._build_header(uploaded_media),
            body=InteractiveMessage.Body(text=self._body),
            footer=InteractiveMessage.Footer(text=self._footer),
            nativeFlowMessage=InteractiveMessage.NativeFlowMessage(
                buttons=self._build_native_flow_buttons(),
                messageParamsJSON=json.dumps(self._params) if self._params else "",
            ),
        )
        if self._context_info is not None:
            interactive.contextInfo.MergeFrom(self._context_info)
        return interactive

    def to_card(self, client: "NewClient") -> InteractiveMessage:
        """Build this button message as a carousel card (synchronous).

        Uploads media if present and returns an ``InteractiveMessage`` suitable
        for embedding inside a :class:`CarouselMessage`.

        :param client: The synchronous neonize client.
        :returns: An ``InteractiveMessage`` protobuf (card payload).
        """
        uploaded = self._upload_media(client)
        return self._build_interactive_message(uploaded)

    async def to_acard(self, client: "NewAClient") -> InteractiveMessage:
        """Build this button message as a carousel card (asynchronous).

        :param client: The asynchronous neonize client.
        :returns: An ``InteractiveMessage`` protobuf (card payload).
        """
        uploaded = await self._aupload_media(client)
        return self._build_interactive_message(uploaded)

    # -- CustomInteractiveMessage contract -----------------------------------

    def prepare_send(self, client: "NewClient") -> Message:
        """Build the full ``Message`` protobuf (synchronous).

        :param client: The synchronous neonize client.
        :returns: A ``Message`` containing the interactive button payload.
        """
        uploaded = self._upload_media(client)
        interactive = self._build_interactive_message(uploaded)
        return Message(interactiveMessage=interactive)

    async def prepare_asend(self, client: "NewAClient") -> Message:
        """Build the full ``Message`` protobuf (asynchronous).

        :param client: The asynchronous neonize client.
        :returns: A ``Message`` containing the interactive button payload.
        """
        uploaded = await self._aupload_media(client)
        interactive = self._build_interactive_message(uploaded)
        return Message(interactiveMessage=interactive)
