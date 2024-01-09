import typing
import io
import requests


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
        if args.startswith("http"):
            return requests.get(args, headers=headers).content
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
