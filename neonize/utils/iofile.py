import os
from pathlib import Path
import re
import tempfile
import typing
import io
import requests
import httpx
from .log import log
from typing import Optional

URL_MATCH = re.compile(r"^https?://")


def get_bytes_from_name_or_url(args: typing.Union[str, bytes]) -> bytes:
    """Gets bytes from either a file name or a URL.

    :param args: Either a file name (str) or binary data (bytes).
    :type args: typing.Union[str, bytes]
    :return: The bytes extracted from the specified file name or URL.
    :rtype: bytes
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    }
    if isinstance(args, str):
        if URL_MATCH.match(args):
            return requests.get(args, headers=headers).content
        else:
            with open(args, "rb") as file:
                return file.read()
    else:
        return args


async def get_bytes_from_name_or_url_async(args: typing.Union[str, bytes]) -> bytes:
    """Gets bytes from either a file name or a URL.

    :param args: Either a file name (str) or binary data (bytes).
    :type args: typing.Union[str, bytes]
    :return: The bytes extracted from the specified file name or URL.
    :rtype: bytes
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    }
    if isinstance(args, str):
        if URL_MATCH.match(args):
            async with httpx.AsyncClient(timeout=None) as client:
                return (await client.get(args, headers=headers)).content
        else:
            with open(args, "rb") as file:
                return file.read()
    else:
        return args


def write_from_bytesio_or_filename(
    fn_or_bytesio: typing.Union[io.BytesIO, str], data: bytes
):
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
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        dir: Optional[str] = None,
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
        if prefix != None:
            params["prefix"] = prefix
        if suffix != None:
            params["suffix"] = suffix
        if dir != None:
            params["dir"] = dir
        self.path = Path(tempfile.mktemp(**params))
        if touch:
            self.path.touch()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.remove(self.path)
        log.debug(
            "exc_type: %r, exc_value: %r, traceback: %r"
            % (exc_type, exc_value, traceback)
        )
