"""AI Rich Response message builder for WhatsApp.

Ports the Baileys ``AIRich`` class to Python. Produces an
``AIRichResponseMessage`` wrapped inside ``Message.botForwardedMessage``.
Supports text (with hyperlinks/citations/LaTeX), code blocks, tables,
images, videos, reels, posts, products, sources, tips, and suggestions.
"""

from __future__ import annotations

import json
import uuid as _uuid
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Self,
    Sequence,
    Union,
)

from ...proto.waE2E.WAWebProtobufsE2E_pb2 import (
    AIRichResponseMessage,
    ContextInfo,
    FutureProofMessage,
    Message,
    MessageContextInfo,
)
from ...proto.waAICommonDeprecated.WAAICommonDeprecated_pb2 import (
    AIRichResponseCodeMetadata,
    AIRichResponseContentItemsMetadata,
    AIRichResponseGridImageMetadata,
    AIRichResponseImageURL,
    AIRichResponseSubMessage,
    AIRichResponseSubMessageType,
    AIRichResponseTableMetadata,
    AI_RICH_RESPONSE_CODE,
    AI_RICH_RESPONSE_CONTENT_ITEMS,
    AI_RICH_RESPONSE_GRID_IMAGE,
    AI_RICH_RESPONSE_TABLE,
    AI_RICH_RESPONSE_TEXT,
    AI_RICH_RESPONSE_TYPE_STANDARD,
)
from ...proto.waAICommon.WAWebProtobufsAICommon_pb2 import (
    AIRichResponseUnifiedResponse,
    BotMetadata,
    BotSourcesMetadata,
    ForwardedAIBotMessageInfo,
)
from .base import CustomInteractiveMessage, InteractiveMessageBuilder

if TYPE_CHECKING:
    from ...aioze.client import NewAClient
    from ...client import NewClient


# ---------------------------------------------------------------------------
# Inline entity extraction (hyperlinks, citations, LaTeX from markdown-like)
# ---------------------------------------------------------------------------


@dataclass
class _InlineEntity:
    key: str
    type: str  # "hyperlink", "citation", "latex"
    metadata: Dict[str, Any] = field(default_factory=dict)


def _extract_inline_entities(
    text: str,
    *,
    hyperlink: bool = True,
    citation: bool = True,
    latex: bool = True,
) -> tuple[str, list[_InlineEntity]]:
    """Parse ``[text](url)`` and ``[text]<url>`` patterns from *text*.

    Returns the transformed text (with ``{{KEY}}`` tags) and a list of
    extracted inline entities.
    """
    entities: list[_InlineEntity] = []
    result = ""
    last = 0
    citation_index = 1
    hyperlink_index = 0
    latex_index = 0
    stack: list[int] = []
    i = 0
    while i < len(text):
        if text[i] == "[" and (i == 0 or text[i - 1] != "\\"):
            stack.append(i)
        elif text[i] == "]" and i + 1 < len(text) and text[i + 1] in ("(", "<"):
            if not stack:
                i += 1
                continue
            start = stack.pop()
            open_ch = text[i + 1]
            close_ch = ")" if open_ch == "(" else ">"
            etype = "link" if open_ch == "(" else "latex"
            end = i + 2
            depth = 1
            while end < len(text) and depth:
                if text[end] == open_ch and text[end - 1] != "\\":
                    depth += 1
                elif text[end] == close_ch and text[end - 1] != "\\":
                    depth -= 1
                end += 1
            if depth:
                i += 1
                continue
            raw = text[start + 1 : i].strip()
            url = text[i + 2 : end - 1].strip()
            if etype == "latex":
                if not latex:
                    i += 1
                    continue
                parts = raw.split("|")
                txt = parts[0] if parts else ""
                key = f"NEONIZE_LATEX_{latex_index}"
                latex_index += 1
                tag = f"{{{{{key}}}}}{txt or 'image'}{{{{/{key}}}}}"
                entities.append(
                    _InlineEntity(
                        key=key,
                        type="latex",
                        metadata={
                            "latex_expression": txt,
                            "latex_image": {
                                "url": url,
                                "width": int(parts[1]) if len(parts) > 1 and parts[1] else 100,
                                "height": int(parts[2]) if len(parts) > 2 and parts[2] else 100,
                            },
                            "font_height": float(parts[3])
                            if len(parts) > 3 and parts[3]
                            else 83.333,
                            "padding": float(parts[4]) if len(parts) > 4 and parts[4] else 15.0,
                            "__typename": "GenAILatexItem",
                        },
                    )
                )
            elif raw:
                if not hyperlink:
                    i += 1
                    continue
                key = f"NEONIZE_HYPERLINK_{hyperlink_index}"
                hyperlink_index += 1
                tag = f"{{{{{key}}}}}{url}{{{{/{key}}}}}"
                entities.append(
                    _InlineEntity(
                        key=key,
                        type="hyperlink",
                        metadata={
                            "display_name": raw,
                            "is_trusted": True,
                            "url": url,
                            "__typename": "GenAIInlineLinkItem",
                        },
                    )
                )
            else:
                if not citation:
                    i += 1
                    continue
                key = f"NEONIZE_CITATION_{citation_index - 1}"
                tag = f"{{{{{key}}}}}{url}{{{{/{key}}}}}"
                entities.append(
                    _InlineEntity(
                        key=key,
                        type="citation",
                        metadata={
                            "reference_id": citation_index,
                            "reference_url": url,
                            "reference_title": url,
                            "reference_display_name": url,
                            "sources": [],
                            "__typename": "GenAISearchCitationItem",
                        },
                    )
                )
                citation_index += 1
            result += text[last:start] + tag
            last = end
            i = end - 1
        i += 1
    result += text[last:]
    return result, entities


# ---------------------------------------------------------------------------
# Code tokenizer
# ---------------------------------------------------------------------------

_KEYWORDS: dict[str, set[str]] = {
    "javascript": {
        "break",
        "case",
        "catch",
        "continue",
        "debugger",
        "delete",
        "do",
        "else",
        "finally",
        "for",
        "function",
        "if",
        "in",
        "instanceof",
        "new",
        "return",
        "switch",
        "this",
        "throw",
        "try",
        "typeof",
        "var",
        "void",
        "while",
        "with",
        "true",
        "false",
        "null",
        "undefined",
        "class",
        "const",
        "let",
        "super",
        "extends",
        "export",
        "import",
        "yield",
        "static",
        "constructor",
        "async",
        "await",
        "get",
        "set",
    },
    "python": {
        "False",
        "None",
        "True",
        "and",
        "as",
        "assert",
        "async",
        "await",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
    },
}

_HIGHLIGHT_MAP = {0: "DEFAULT", 1: "KEYWORD", 2: "METHOD", 3: "STR", 4: "NUMBER", 5: "COMMENT"}
_HIGHLIGHT_PROTO = {
    0: AIRichResponseCodeMetadata.AI_RICH_RESPONSE_CODE_HIGHLIGHT_DEFAULT,
    1: AIRichResponseCodeMetadata.AI_RICH_RESPONSE_CODE_HIGHLIGHT_KEYWORD,
    2: AIRichResponseCodeMetadata.AI_RICH_RESPONSE_CODE_HIGHLIGHT_METHOD,
    3: AIRichResponseCodeMetadata.AI_RICH_RESPONSE_CODE_HIGHLIGHT_STRING,
    4: AIRichResponseCodeMetadata.AI_RICH_RESPONSE_CODE_HIGHLIGHT_NUMBER,
    5: AIRichResponseCodeMetadata.AI_RICH_RESPONSE_CODE_HIGHLIGHT_COMMENT,
}


def _tokenize_code(code: str, lang: str = "javascript"):
    """Tokenize source code for WhatsApp AI rich response rendering."""
    keywords = _KEYWORDS.get(lang, set())
    tokens: list[tuple[str, int]] = []

    def push(content: str, ttype: int):
        if not content:
            return
        if tokens and tokens[-1][1] == ttype:
            tokens[-1] = (tokens[-1][0] + content, ttype)
        else:
            tokens.append((content, ttype))

    i = 0
    while i < len(code):
        c = code[i]
        if c in " \t\n\r":
            s = i
            while i < len(code) and code[i] in " \t\n\r":
                i += 1
            push(code[s:i], 0)
            continue
        if c == "/" and i + 1 < len(code) and code[i + 1] == "/":
            s = i
            i += 2
            while i < len(code) and code[i] != "\n":
                i += 1
            push(code[s:i], 5)
            continue
        if c == "#" and lang == "python":
            s = i
            while i < len(code) and code[i] != "\n":
                i += 1
            push(code[s:i], 5)
            continue
        if c in "\"'`":
            s = i
            q = c
            i += 1
            while i < len(code):
                if code[i] == "\\" and i + 1 < len(code):
                    i += 2
                elif code[i] == q:
                    i += 1
                    break
                else:
                    i += 1
            push(code[s:i], 3)
            continue
        if c.isdigit():
            s = i
            while i < len(code) and (code[i].isdigit() or code[i] == "."):
                i += 1
            push(code[s:i], 4)
            continue
        if c.isalpha() or c in "_$":
            s = i
            while i < len(code) and (code[i].isalnum() or code[i] in "_$"):
                i += 1
            word = code[s:i]
            if word in keywords:
                push(word, 1)
            else:
                j = i
                while j < len(code) and code[j] in " \t":
                    j += 1
                push(word, 2 if j < len(code) and code[j] == "(" else 0)
            continue
        push(c, 0)
        i += 1

    code_blocks = [
        AIRichResponseCodeMetadata.AIRichResponseCodeBlock(
            highlightType=_HIGHLIGHT_PROTO[t], codeContent=content
        )
        for content, t in tokens
    ]
    unified = [{"content": content, "type": _HIGHLIGHT_MAP[t]} for content, t in tokens]
    return code_blocks, unified


# ---------------------------------------------------------------------------
# Table helpers
# ---------------------------------------------------------------------------


def _build_table_metadata(table: list[list[str]]):
    """Convert a 2D string array to table metadata and unified rows."""
    if not table:
        raise ValueError("Table must have at least one row (header).")
    header, *data_rows = table
    max_len = max(len(header), *(len(r) for r in data_rows)) if data_rows else len(header)
    normalize = lambda r: r + [""] * (max_len - len(r))

    rows_proto = [
        AIRichResponseTableMetadata.AIRichResponseTableRow(items=normalize(header), isHeading=True)
    ] + [AIRichResponseTableMetadata.AIRichResponseTableRow(items=normalize(r)) for r in data_rows]

    unified_rows = [{"is_header": True, "cells": normalize(header)}] + [
        {"is_header": False, "cells": normalize(r)} for r in data_rows
    ]
    return rows_proto, unified_rows


# ---------------------------------------------------------------------------
# Layout helper
# ---------------------------------------------------------------------------


def _new_layout(name: str, data: Any) -> dict:
    key = "primitives" if isinstance(data, list) else "primitive"
    return {"view_model": {key: data, "__typename": f"GenAI{name}LayoutViewModel"}}


# ---------------------------------------------------------------------------
# Data classes for explicit, type-safe parameters
# ---------------------------------------------------------------------------


@dataclass
class Product:
    """A product card for :meth:`AIRichMessage.add_product`.

    :param title: Product title.
    :param brand: Brand name.
    :param price: Display price (e.g. ``"$49.99"``).
    :param sale_price: Sale price text (empty string if not on sale).
    :param product_url: URL linking to the product page.
    :param image_url: URL of the main product image.
    :param icon_url: URL of an icon/favicon for the product source.
    """

    title: str = ""
    brand: str = ""
    price: str = ""
    sale_price: str = ""
    product_url: str = ""
    image_url: str = ""
    icon_url: str = ""


@dataclass
class Reel:
    """A reel/short-video item for :meth:`AIRichMessage.add_reels`.

    :param username: Creator username displayed on the reel.
    :param video_url: Direct URL to the reel video.
    :param thumbnail_url: URL of the reel thumbnail image.
    :param profile_icon_url: URL of the creator's profile icon.
    :param reels_title: Title text of the reel.
    :param likes_count: Number of likes.
    :param shares_count: Number of shares.
    :param view_count: Number of views.
    :param reel_source: Source platform identifier (e.g. ``"IG"``).
    :param is_verified: Whether the creator account is verified.
    """

    username: str = ""
    video_url: str = ""
    thumbnail_url: str = ""
    profile_icon_url: str = ""
    reels_title: str = ""
    likes_count: int = 0
    shares_count: int = 0
    view_count: int = 0
    reel_source: str = "IG"
    is_verified: bool = False


@dataclass
class Post:
    """A social-media post card for :meth:`AIRichMessage.add_post`.

    :param title: Post title.
    :param subtitle: Post subtitle.
    :param username: Author username.
    :param profile_picture_url: URL of the author's profile picture.
    :param is_verified: Whether the author is verified.
    :param thumbnail_url: URL of the post thumbnail.
    :param post_caption: Post caption text.
    :param likes_count: Number of likes.
    :param comments_count: Number of comments.
    :param shares_count: Number of shares.
    :param post_url: URL to the post.
    :param post_deeplink: Deep-link URL for in-app opening.
    :param source_app: Source application (e.g. ``"INSTAGRAM"``).
    :param footer_label: Footer label text.
    :param footer_icon: Footer icon URL.
    :param orientation: Media orientation (``"LANDSCAPE"`` or ``"PORTRAIT"``).
    :param post_type: Media type (``"VIDEO"`` or ``"IMAGE"``).
    """

    title: str = ""
    subtitle: str = ""
    username: str = ""
    profile_picture_url: str = ""
    is_verified: bool = False
    thumbnail_url: str = ""
    post_caption: str = ""
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    post_url: str = ""
    post_deeplink: str = ""
    source_app: str = "INSTAGRAM"
    footer_label: str = ""
    footer_icon: str = ""
    orientation: str = "LANDSCAPE"
    post_type: str = "VIDEO"


@dataclass
class Source:
    """A search-result source for :meth:`AIRichMessage.add_source`.

    :param display_name: Display name of the source.
    :param url: URL of the source page.
    :param favicon_url: URL of the source's favicon.
    """

    display_name: str = ""
    url: str = ""
    favicon_url: str = ""


# ---------------------------------------------------------------------------
# AIRichMessage builder
# ---------------------------------------------------------------------------


class AIRichMessage(CustomInteractiveMessage, InteractiveMessageBuilder):
    """Fluent builder for WhatsApp AI Rich Response messages.

    Produces an ``AIRichResponseMessage`` wrapped inside
    ``Message.botForwardedMessage`` (a ``FutureProofMessage``).
    """

    def __init__(self) -> None:
        super().__init__()
        self._submessages: list[AIRichResponseSubMessage] = []
        self._sections: list[dict] = []
        self._rich_response_sources: list[BotSourcesMetadata.BotSourceItem] = []

    # -- Setters -------------------------------------------------------------

    def set_title(self, title: str) -> Self:
        self._title = title
        return self

    def set_footer(self, footer: str) -> Self:
        self._footer = footer
        return self

    def set_context_info(self, context_info: ContextInfo) -> Self:
        self._context_info = context_info
        return self

    # -- Content adders ------------------------------------------------------

    def add_text(
        self,
        text: str,
        *,
        hyperlink: bool = True,
        citation: bool = True,
        latex: bool = True,
    ) -> Self:
        """Add a rich text block with optional inline entity extraction.

        Supports ``[text](url)`` for hyperlinks, ``[](url)`` for citations,
        and ``[id|w|h]<url>`` for LaTeX images.
        """
        extracted, entities = _extract_inline_entities(
            text, hyperlink=hyperlink, citation=citation, latex=latex
        )
        inline_entities = [{"key": e.key, "metadata": e.metadata} for e in entities]

        self._submessages.append(
            AIRichResponseSubMessage(
                messageType=AI_RICH_RESPONSE_TEXT,
                messageText=extracted,
            )
        )
        primitive: Dict[str, Any] = {
            "text": extracted,
            "__typename": "GenAIMarkdownTextUXPrimitive",
        }
        if inline_entities:
            primitive["inline_entities"] = inline_entities
        self._sections.append(_new_layout("Single", primitive))
        return self

    def add_code(self, language: str, code: str) -> Self:
        """Add a syntax-highlighted code block."""
        code_blocks, unified = _tokenize_code(code, language)
        self._submessages.append(
            AIRichResponseSubMessage(
                messageType=AI_RICH_RESPONSE_CODE,
                codeMetadata=AIRichResponseCodeMetadata(
                    codeLanguage=language,
                    codeBlocks=code_blocks,
                ),
            )
        )
        self._sections.append(
            _new_layout(
                "Single",
                {
                    "language": language,
                    "code_blocks": unified,
                    "__typename": "GenAICodeUXPrimitive",
                },
            )
        )
        return self

    def add_table(self, table: list[list[str]]) -> Self:
        """Add a table. First row is the header."""
        rows_proto, unified_rows = _build_table_metadata(table)
        self._submessages.append(
            AIRichResponseSubMessage(
                messageType=AI_RICH_RESPONSE_TABLE,
                tableMetadata=AIRichResponseTableMetadata(title="", rows=rows_proto),
            )
        )
        self._sections.append(
            _new_layout(
                "Single",
                {
                    "rows": unified_rows,
                    "__typename": "GenAITableUXPrimitive",
                },
            )
        )
        return self

    def add_image(self, image_url: Union[str, list[str]]) -> Self:
        """Add one or more images by URL."""
        urls = image_url if isinstance(image_url, list) else [image_url]
        image_urls_proto = [
            AIRichResponseImageURL(imagePreviewURL=u, imageHighResURL=u) for u in urls
        ]
        self._submessages.append(
            AIRichResponseSubMessage(
                messageType=AI_RICH_RESPONSE_GRID_IMAGE,
                gridImageMetadata=AIRichResponseGridImageMetadata(
                    gridImageURL=AIRichResponseImageURL(imagePreviewURL=urls[0]),
                    imageURLs=image_urls_proto,
                ),
            )
        )
        for u in urls:
            self._sections.append(
                _new_layout(
                    "Single",
                    {
                        "media": {"url": u, "mime_type": "image/png"},
                        "imagine_type": "IMAGE",
                        "status": {"status": "READY"},
                        "__typename": "GenAIImaginePrimitive",
                    },
                )
            )
        return self

    def add_video(self, url: Union[str, list[str]], *, duration: int = 0) -> Self:
        """Add one or more videos by URL.

        :param url: A single video URL or a list of video URLs.
        :param duration: Video duration in seconds (applies to all URLs).
        """
        urls = url if isinstance(url, list) else [url]
        self._submessages.append(
            AIRichResponseSubMessage(
                messageType=AI_RICH_RESPONSE_TEXT,
                messageText="[ VIDEO ]",
            )
        )
        for u in urls:
            self._sections.append(
                _new_layout(
                    "Single",
                    {
                        "media": {"url": u, "mime_type": "video/mp4", "duration": duration},
                        "imagine_type": "ANIMATE",
                        "status": {"status": "READY"},
                        "__typename": "GenAIImaginePrimitive",
                    },
                )
            )
        return self

    def add_source(self, source: Union["Source", list["Source"]]) -> Self:
        """Add search result sources.

        :param source: A single :class:`Source` or a list of them.
        """
        items = source if isinstance(source, list) else [source]
        source_data = [
            {
                "source_type": "THIRD_PARTY",
                "source_display_name": s.display_name,
                "source_subtitle": "AI",
                "source_url": s.url,
                "favicon": {
                    "url": s.favicon_url,
                    "mime_type": "image/jpeg",
                    "width": 16,
                    "height": 16,
                },
            }
            for s in items
        ]
        self._sections.append(
            _new_layout(
                "Single",
                {
                    "sources": source_data,
                    "__typename": "GenAISearchResultPrimitive",
                },
            )
        )
        return self

    def add_reels(self, reel: Union["Reel", list["Reel"]]) -> Self:
        """Add reel/short-video item(s).

        :param reel: A single :class:`Reel` or a list of them.
        """
        items = reel if isinstance(reel, list) else [reel]
        reel_items = [
            AIRichResponseContentItemsMetadata.AIRichResponseContentItemMetadata(
                reelItem=AIRichResponseContentItemsMetadata.AIRichResponseReelItem(
                    title=r.username,
                    profileIconURL=r.profile_icon_url,
                    thumbnailURL=r.thumbnail_url,
                    videoURL=r.video_url,
                ),
            )
            for r in items
        ]
        self._submessages.append(
            AIRichResponseSubMessage(
                messageType=AI_RICH_RESPONSE_CONTENT_ITEMS,
                contentItemsMetadata=AIRichResponseContentItemsMetadata(
                    contentType=AIRichResponseContentItemsMetadata.CAROUSEL,
                    itemsMetadata=reel_items,
                ),
            )
        )
        for idx, r in enumerate(items):
            self._rich_response_sources.append(
                BotSourcesMetadata.BotSourceItem(
                    provider=BotSourcesMetadata.BotSourceItem.OTHER,
                    thumbnailCDNURL=r.thumbnail_url,
                    sourceProviderURL=r.video_url,
                    sourceQuery="",
                    faviconCDNURL=r.profile_icon_url,
                    citationNumber=idx + 1,
                    sourceTitle=r.username,
                )
            )
        primitives = [
            {
                "reels_url": r.video_url,
                "thumbnail_url": r.thumbnail_url,
                "creator": r.username,
                "avatar_url": r.profile_icon_url,
                "reels_title": r.reels_title or r.username,
                "likes_count": r.likes_count,
                "shares_count": r.shares_count,
                "view_count": r.view_count,
                "reel_source": r.reel_source,
                "is_verified": r.is_verified,
                "__typename": "GenAIReelPrimitive",
            }
            for r in items
        ]
        self._sections.append(_new_layout("HScroll", primitives))
        return self

    def add_product(
        self,
        product: Union["Product", list["Product"]],
    ) -> Self:
        """Add product card(s).

        :param product: A single :class:`Product` or a list of them.
        """
        items = product if isinstance(product, list) else [product]
        self._submessages.append(
            AIRichResponseSubMessage(
                messageType=AI_RICH_RESPONSE_TEXT,
                messageText="[ PRODUCT ]",
            )
        )
        products = [
            {
                "title": p.title,
                "brand": p.brand,
                "price": p.price,
                "sale_price": p.sale_price,
                "product_url": p.product_url,
                "image": {"url": p.image_url},
                "additional_images": [{"url": p.icon_url}],
                "__typename": "GenAIProductItemCardPrimitive",
            }
            for p in items
        ]
        is_multi = isinstance(product, list)
        layout = "HScroll" if is_multi else "Single"
        self._sections.append(_new_layout(layout, products if is_multi else products[0]))
        return self

    def add_post(self, post: Union["Post", list["Post"]]) -> Self:
        """Add social-media post card(s).

        :param post: A single :class:`Post` or a list of them.
        """
        posts = post if isinstance(post, list) else [post]
        self._submessages.append(
            AIRichResponseSubMessage(
                messageType=AI_RICH_RESPONSE_TEXT,
                messageText="[ POST ]",
            )
        )
        primitives = [
            {
                "title": p.title,
                "subtitle": p.subtitle,
                "username": p.username,
                "profile_picture_url": p.profile_picture_url,
                "is_verified": p.is_verified,
                "thumbnail_url": p.thumbnail_url,
                "post_caption": p.post_caption,
                "likes_count": p.likes_count,
                "comments_count": p.comments_count,
                "shares_count": p.shares_count,
                "post_url": p.post_url,
                "post_deeplink": p.post_deeplink,
                "source_app": p.source_app,
                "footer_label": p.footer_label,
                "footer_icon": p.footer_icon,
                "is_carousel": len(posts) > 1,
                "orientation": p.orientation,
                "post_type": p.post_type,
                "__typename": "GenAIPostPrimitive",
            }
            for p in posts
        ]
        self._sections.append(_new_layout("HScroll", primitives))
        return self

    def add_tip(self, text: str) -> Self:
        """Add a metadata/tip text."""
        self._submessages.append(
            AIRichResponseSubMessage(
                messageType=AI_RICH_RESPONSE_TEXT,
                messageText=text,
            )
        )
        self._sections.append(
            _new_layout(
                "Single",
                {
                    "text": text,
                    "__typename": "GenAIMetadataTextPrimitive",
                },
            )
        )
        return self

    def add_suggest(self, suggestions: Union[str, list[str]]) -> Self:
        """Add follow-up suggestion pill(s)."""
        items = suggestions if isinstance(suggestions, list) else [suggestions]
        pills = [
            {
                "prompt_text": t,
                "prompt_type": "SUGGESTED_PROMPT",
                "__typename": "GenAIFollowUpSuggestionPillPrimitive",
            }
            for t in items
        ]
        self._sections.append(_new_layout("ActionRow", pills))
        return self

    # -- Build ---------------------------------------------------------------

    def _build_message(self, *, forwarded: bool = True) -> Message:
        forward_ctx = ContextInfo()
        if forwarded:
            forward_ctx.forwardingScore = 1
            forward_ctx.isForwarded = True
            forward_ctx.forwardedAiBotMessageInfo.MergeFrom(
                ForwardedAIBotMessageInfo(botJID="0@bot")
            )
            forward_ctx.forwardOrigin = ContextInfo.META_AI  # 4

        if self._context_info is not None:
            forward_ctx.MergeFrom(self._context_info)

        sections = list(self._sections)
        if self._footer:
            sections.append(
                _new_layout(
                    "Single",
                    {
                        "text": self._footer,
                        "__typename": "GenAIMetadataTextPrimitive",
                    },
                )
            )

        # The proto field ``data`` is ``bytes``.  In the JS reference the JSON
        # is base64-encoded and passed as a *string* to
        # ``generateWAMessageFromContent`` which then decodes it back to raw
        # bytes during protobuf serialisation.  Since Python builds the proto
        # directly, we must supply the **raw JSON bytes** – not a base64
        # re-encoding.
        unified_data = json.dumps(
            {
                "response_id": str(_uuid.uuid4()),
                "sections": sections,
            }
        )

        rich_msg = AIRichResponseMessage(
            messageType=AI_RICH_RESPONSE_TYPE_STANDARD,
            submessages=self._submessages,
            unifiedResponse=AIRichResponseUnifiedResponse(
                data=unified_data.encode("utf-8"),
            ),
            contextInfo=forward_ctx,
        )

        inner_message = Message(richResponseMessage=rich_msg)
        bot_metadata = BotMetadata(
            messageDisclaimerText=self._title,
            richResponseSourcesMetadata=BotSourcesMetadata(sources=self._rich_response_sources),
        )

        return Message(
            messageContextInfo=MessageContextInfo(
                deviceListMetadataVersion=2,
                botMetadata=bot_metadata,
            ),
            botForwardedMessage=FutureProofMessage(message=inner_message),
        )

    def prepare_send(self, client: "NewClient") -> Message:
        """Build the full ``Message`` protobuf (synchronous)."""
        return self._build_message()

    async def prepare_asend(self, client: "NewAClient") -> Message:
        """Build the full ``Message`` protobuf (asynchronous)."""
        return self._build_message()
