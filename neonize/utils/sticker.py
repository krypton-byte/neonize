import asyncio
import json
import os
import tempfile
import threading
import uuid
from io import BytesIO

import magic
from PIL import Image, ImageSequence

from ..exc import ConvertStickerError
from .calc import auto_sticker, original_sticker
from .ffmpeg import AFFmpeg, FFmpeg
from .iofile import (
    TemporaryFile,
    get_bytes_from_name_or_url,
    get_bytes_from_name_or_url_async,
)
from .platform import is_executable_installed


def add_exif(name: str = "", packname: str = "") -> bytes:
    """
    Adds EXIF metadata to a sticker pack.

    :param name: Name of the sticker pack, defaults to an empty string.
    :type name: str, optional
    :param packname: Publisher of the sticker pack, defaults to an empty string.
    :type packname: str, optional
    :return: Byte array containing the EXIF metadata.
    :rtype: bytes
    """
    json_data = {
        "sticker-pack-id": "com.snowcorp.stickerly.android.stickercontentprovider b5e7275f-f1de-4137-961f-57becfad34f2",
        "sticker-pack-name": name,
        "sticker-pack-publisher": packname,
        "android-app-store-link": "https://play.google.com/store/apps/details?id=com.marsvard.stickermakerforwhatsapp",
        "ios-app-store-link": "https://itunes.apple.com/app/sticker-maker-studio/id1443326857",
    }

    exif_attr = bytes.fromhex("49 49 2A 00 08 00 00 00 01 00 41 57 07 00 00 00 00 00 16 00 00 00")
    json_buffer = json.dumps(json_data).encode("utf-8")
    exif = exif_attr + json_buffer
    exif_length = len(json_buffer)
    exif = exif[:14] + exif_length.to_bytes(4, "little") + exif[18:]
    return exif


def webpmux_is_installed():
    return is_executable_installed("webpmux")


MAX_STICKER_SIZE = 512000
WEBPMUX_IS_AVAILABLE = False
if webpmux_is_installed():
    MAX_STICKER_SIZE = 712000
    WEBPMUX_IS_AVAILABLE = True


async def aio_convert_to_sticker(
    file: bytes,
    name="",
    packname="",
    enforce_not_broken=False,
    animated_gif=False,
    is_webm=False,
    quality=75,
    compression_level=4,
):
    async with AFFmpeg(file) as ffmpeg:
        sticker = await ffmpeg.cv_to_webp(
            enforce_not_broken=enforce_not_broken,
            animated_gif=animated_gif,
            max_sticker_size=MAX_STICKER_SIZE,
            is_webm=is_webm,
            quality=quality,
            compression_level=compression_level,
        )
    if not WEBPMUX_IS_AVAILABLE:
        return sticker, False

    buf = await aio_add_exif_to_sticker(sticker, name, packname)
    return (buf if buf is not None else sticker), buf is not None


async def aio_add_exif_to_sticker(sticker, name, packname):
    if not WEBPMUX_IS_AVAILABLE:
        return None
    with TemporaryFile(prefix=None, touch=False) as exif_filename:
        exif_bytes = add_exif(name=name, packname=packname)
        await asyncio.to_thread(_write_sticker_bytes, exif_filename.path, exif_bytes)
        temp = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.webp")
        async with AFFmpeg(sticker) as ffmpeg:
            cmd = [
                "webpmux",
                "-set",
                "exif",
                f"{exif_filename.path}",
                ffmpeg.filepath,
                "-o",
                temp,
            ]
            await ffmpeg.call(cmd)
        return await asyncio.to_thread(_read_and_unlink, temp)


def convert_to_sticker(
    file: bytes,
    name="",
    packname="",
    enforce_not_broken=False,
    animated_gif=False,
    is_webm=False,
    quality=75,
    compression_level=4,
):
    with FFmpeg(file) as ffmpeg:
        sticker = ffmpeg.cv_to_webp(
            enforce_not_broken=enforce_not_broken,
            animated_gif=animated_gif,
            max_sticker_size=MAX_STICKER_SIZE,
            is_webm=is_webm,
            quality=quality,
            compression_level=compression_level,
        )
    if not WEBPMUX_IS_AVAILABLE:
        return sticker, False

    buf = add_exif_to_sticker(sticker, name, packname)
    return (buf if buf is not None else sticker), buf is not None


def add_exif_to_sticker(sticker, name, packname):
    if not WEBPMUX_IS_AVAILABLE:
        return None
    with TemporaryFile(prefix=None, touch=False) as exif_filename:
        _write_sticker_bytes(exif_filename.path, add_exif(name=name, packname=packname))
        temp = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.webp")
        with FFmpeg(sticker) as ffmpeg:
            cmd = [
                "webpmux",
                "-set",
                "exif",
                f"{exif_filename.path}",
                ffmpeg.filepath,
                "-o",
                temp,
            ]
            ffmpeg.call(cmd)
        return _read_and_unlink(temp)


astick_sem = asyncio.Semaphore(20)


def _write_sticker_bytes(path, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)


def _read_and_unlink(path: str) -> bytes:
    try:
        with open(path, "rb") as f:
            return f.read()
    finally:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass


def _process_image_sticker_sync(
    sticker: bytes, name: str, packname: str, crop: bool
) -> tuple[bytes, bool]:
    io_save = BytesIO(sticker)
    stk = auto_sticker(io_save) if crop else original_sticker(io_save)
    io_out = BytesIO()
    stk.save(
        io_out,
        format="webp",
        exif=add_exif(name, packname),
        save_all=True,
        loop=0,
    )
    return io_out.getvalue(), False


async def aio_convert_to_webp(
    sticker,
    name,
    packname,
    crop=False,
    passthrough=True,
    transparent=False,
    quality=75,
    compression_level=4,
):
    sticker = await get_bytes_from_name_or_url_async(sticker)

    def _inspect_mime_and_frames(data: bytes) -> tuple[bool, bool, bool]:
        _is_webm = _is_image = False
        mime = magic.from_buffer(data, mime=True)
        if mime == "image/webp":
            img = Image.open(BytesIO(data))
            if len(ImageSequence.all_frames(img)) < 2:
                _is_image = True
        elif passthrough:
            raise ConvertStickerError("File is not a webp, which is required for passthrough.")
        elif mime == "video/webm":
            _is_webm = True
        elif mime.split("/")[0] == "image":
            _is_image = True
        return _is_image, _is_webm, (not _is_image)

    is_image, is_webm, animated = await asyncio.to_thread(_inspect_mime_and_frames, sticker)
    if passthrough:
        return sticker, animated
    if is_image:
        out_bytes, _ = await asyncio.to_thread(
            _process_image_sticker_sync, sticker, name, packname, crop
        )
        return out_bytes, animated

    animated = True
    async with astick_sem:
        sticker_bytes, saved_exif = await aio_convert_to_sticker(
            sticker,
            name,
            packname,
            enforce_not_broken=True,
            animated_gif=transparent,
            is_webm=is_webm,
            quality=quality,
            compression_level=compression_level,
        )
    if saved_exif:
        return sticker_bytes, animated

    def _save_pillow_webp(data: bytes) -> bytes:
        stk = Image.open(BytesIO(data))
        io_out = BytesIO()
        stk.save(
            io_out,
            format="webp",
            exif=add_exif(name, packname),
            save_all=True,
            loop=0,
        )
        return io_out.getvalue()

    return await asyncio.to_thread(_save_pillow_webp, sticker_bytes), animated


stick_sem = threading.Semaphore(20)


def convert_to_webp(
    sticker,
    name,
    packname,
    crop=False,
    passthrough=True,
    transparent=False,
    quality=75,
    compression_level=4,
):
    sticker = get_bytes_from_name_or_url(sticker)
    animated = is_webm = is_image = saved_exif = stk = False
    mime = magic.from_buffer(sticker, mime=True)
    if mime == "image/webp":
        io_save = BytesIO(sticker)
        img = Image.open(io_save)
        if len(ImageSequence.all_frames(img)) < 2:
            is_image = True
    elif passthrough:
        raise ConvertStickerError("File is not a webp, which is required for passthrough.")
    elif mime == "video/webm":
        is_webm = True
    elif (mime := mime.split("/"))[0] == "image":
        is_image = True
    animated = not is_image
    if passthrough:
        return sticker, animated
    if is_image:
        io_save = BytesIO(sticker)
        stk = auto_sticker(io_save) if crop else original_sticker(io_save)
        io_save = BytesIO()
        # io_save.seek(0)
    else:
        animated = True
        with stick_sem:
            sticker, saved_exif = convert_to_sticker(
                sticker,
                name,
                packname,
                enforce_not_broken=True,
                animated_gif=transparent,
                is_webm=is_webm,
                quality=quality,
                compression_level=compression_level,
            )
        if saved_exif:
            io_save = BytesIO(sticker)
        else:
            stk = Image.open(BytesIO(sticker))
            io_save = BytesIO()
    if not saved_exif:
        stk.save(
            io_save,
            format="webp",
            exif=add_exif(name, packname),
            save_all=True,
            loop=0,
        )
    return io_save.getvalue(), animated
