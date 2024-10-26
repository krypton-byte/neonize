import time
from typing import Optional
import httpx

from linkpreview.exceptions import (
    InvalidContentError,
    InvalidMimeTypeError,
    MaximumContentSizeError,
)


class LinkGrabber:
    headers = {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0)"
            " Gecko/20100101"
            " Firefox/95.0"
        ),
        "accept-language": "en-US,en;q=0.5",
        "accept": (
            "text/html" ",application/xhtml+xml" ",application/xml;q=0.9" ",*/*;q=0.8"
        ),
    }

    def __init__(
        self,
        initial_timeout: int = 20,
        maxsize: int = 1048576,
        receive_timeout: int = 10,
        chunk_size: int = 1024,
    ):
        """
        :param initial_timeout in seconds
        :param maxsize in bytes (default 1048576 = 1 MB)
        :param receive_timeout in seconds
        :param chunk_size in bytes
        """
        self.initial_timeout = initial_timeout
        self.maxsize = maxsize
        self.receive_timeout = receive_timeout
        self.chunk_size = chunk_size

    async def get_content(self, url: str, headers: Optional[dict] = None):
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "GET",
                url,
                timeout=self.initial_timeout,
                headers={**self.headers, **headers} if headers else self.headers,
            ) as r:
                r.raise_for_status()

                content_type = r.headers.get("content-type")
                if not content_type:
                    raise InvalidContentError("Invalid content type")

                mime_type = content_type.split(";")[0].lower()
                if mime_type != "text/html":
                    raise InvalidMimeTypeError("Invalid mime type")

                length = r.headers.get("Content-Length")
                if length and int(length) > self.maxsize:
                    raise MaximumContentSizeError("response too large")

                size = 0
                start = time.time()
                content = b""
                async for chunk in r.aiter_bytes(self.chunk_size):
                    if time.time() - start > self.receive_timeout:
                        raise TimeoutError("timeout reached")

                    size += len(chunk)
                    if size > self.maxsize:
                        raise MaximumContentSizeError("response too large")

                    content += chunk

                return content.decode(), url
