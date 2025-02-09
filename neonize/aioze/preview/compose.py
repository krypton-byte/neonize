from httpx import HTTPStatusError, ConnectTimeout
from linkpreview import Link, LinkPreview
from linkpreview import LinkGrabber as fallback_LinkGrabber
from linkpreview.exceptions import InvalidMimeTypeError
from .grabber import LinkGrabber


def fallback_grab_link(url: str):
    try:
        grabber = fallback_LinkGrabber(
            initial_timeout=20,
            maxsize=1048576,
            receive_timeout=10,
            chunk_size=1024,
        )
        return grabber.get_content(url, headers={"user-agent": "imessagebot", "accept": "*/*"})
    except Exception:
        return None, url


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
        except ConnectTimeout:
            return False
        except HTTPStatusError:
            content, url = fallback_grab_link(url)
            if not content:
                return

    link = Link(url, content)
    return LinkPreview(link, parser=parser)
