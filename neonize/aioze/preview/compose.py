from typing import Literal, Optional, TypeVar, overload
from httpx import URL
from linkpreview import Link, LinkPreview
from linkpreview.exceptions import InvalidMimeTypeError
from .grabber import LinkGrabber


async def link_preview(
    url: str = None,
    content: str = None,
    parser: str = "html.parser",
):
    """
    Get link preview
    """
    if content is None:
        try:
            grabber = LinkGrabber()
            content, url = await grabber.get_content(url)
        except InvalidMimeTypeError:
            content = ""

    link = Link(url, content)
    return LinkPreview(link, parser=parser)
