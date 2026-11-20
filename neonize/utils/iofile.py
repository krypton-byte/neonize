import asyncio
import io
import os
import re
import tempfile
import weakref
import zipfile
from pathlib import Path

import httpx
import requests

from .log import log

URL_MATCH = re.compile(r"^https?://")
_DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}
_SYNC_SESSION = requests.Session()
_SYNC_SESSION.headers.update(_DEFAULT_HEADERS)


def _read_file_bytes(path: str) -> bytes:
    with open(path, "rb") as file:
        return file.read()


def get_bytes_from_name_or_url(args: str | bytes) -> bytes:
    """Gets bytes from either a file name or a URL.

    :param args: Either a file name (str) or binary data (bytes).
    :type args: typing.Union[str, bytes]
    :return: The bytes extracted from the specified file name or URL.
    :rtype: bytes
    """
    if isinstance(args, str):
        if URL_MATCH.match(args):
            resp = _SYNC_SESSION.get(args, timeout=30)
            resp.raise_for_status()
            return resp.content
        return _read_file_bytes(args)
    return args


_ASYNC_HTTP_CLIENTS: weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, httpx.AsyncClient] = (
    weakref.WeakKeyDictionary()
)


def _get_async_http_client() -> httpx.AsyncClient:
    loop = asyncio.get_running_loop()
    client = _ASYNC_HTTP_CLIENTS.get(loop)
    if client is None or client.is_closed:
        client = httpx.AsyncClient(timeout=30.0)
        _ASYNC_HTTP_CLIENTS[loop] = client
    return client


async def get_bytes_from_name_or_url_async(args: str | bytes) -> bytes:
    """Gets bytes from either a file name or a URL.

    :param args: Either a file name (str) or binary data (bytes).
    :type args: typing.Union[str, bytes]
    :return: The bytes extracted from the specified file name or URL.
    :rtype: bytes
    """
    if isinstance(args, str):
        if URL_MATCH.match(args):
            client = _get_async_http_client()
            resp = await client.get(args, headers=_DEFAULT_HEADERS)
            resp.raise_for_status()
            return resp.content
        return await asyncio.to_thread(_read_file_bytes, args)
    return args


def write_from_bytesio_or_filename(fn_or_bytesio: io.BytesIO | str, data: bytes):
    """Writes bytes to either a BytesIO object or a file specified by its name.

    :param fn_or_bytesio: Either a BytesIO object or the name of the file to write data to.
    :type fn_or_bytesio: io.BytesIO | str
    :param data: The bytes to be written.
    :type data: bytes
    """
    if isinstance(fn_or_bytesio, io.BytesIO):
        fn_or_bytesio.write(data)
    else:
        with open(fn_or_bytesio, "wb") as file:
            file.write(data)


class TemporaryFile:
    def __init__(
        self,
        prefix: str | None = None,
        suffix: str | None = None,
        dir: str | None = None,
        touch: bool = True,
    ) -> None:
        """
        Initializes a TemporaryFile object. This object represents a temporary file in the system.
        The file is created upon initialization and removed when the object is deleted.

        :param prefix: The prefix of the temporary file name, defaults to None
        :type prefix: Optional[str], optional
        :param suffix: The suffix of the temporary file name, defaults to None
        :type suffix: Optional[str], optional
        :param dir: The directory where the temporary file will be created, defaults to None
        :type dir: Optional[str], optional
        :param touch: If True, the file is immediately created upon object initialization, defaults to True
        :type touch: bool, optional
        """
        params = {}
        if prefix is not None:
            params["prefix"] = prefix
        if suffix is not None:
            params["suffix"] = suffix
        if dir is not None:
            params["dir"] = dir
        fd, name = tempfile.mkstemp(**params)
        os.close(fd)
        self.path = Path(name)
        if not touch:
            try:
                os.unlink(self.path)
            except FileNotFoundError:
                pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass
        log.debug("exc_type: %r, exc_value: %r, traceback: %r" % (exc_type, exc_value, traceback))


def prepare_zip_file_content(file_name_content: dict) -> bytes:
    """
    returns Zip bytes
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, file_data in file_name_content.items():
            zip_file.writestr(file_name, file_data)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()
