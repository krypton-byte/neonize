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

    exif_attr = bytes.fromhex(
        "49 49 2A 00 08 00 00 00 01 00 41 57 07 00 00 00 00 00 16 00 00 00"
    )
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
):
    async with AFFmpeg(file) as ffmpeg:
        sticker = await ffmpeg.cv_to_webp(
            enforce_not_broken=enforce_not_broken,
            animated_gif=animated_gif,
            max_sticker_size=MAX_STICKER_SIZE,
            is_webm=is_webm,
        )
    if not WEBPMUX_IS_AVAILABLE:
        return sticker, False

    exif_filename = TemporaryFile(prefix=None, touch=False).__enter__()
    with open(exif_filename.path, "wb") as file:
        file.write(add_exif(name=name, packname=packname))
    temp = tempfile.gettempdir() + "/" + f"{uuid.uuid4()}" + ".webp"
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
    exif_filename.__exit__(None, None, None)
    with open(temp, "rb") as file:
        buf = file.read()
    os.remove(temp)
    return buf, True


def convert_to_sticker(
    file: bytes,
    name="",
    packname="",
    enforce_not_broken=False,
    animated_gif=False,
    is_webm=False,
):
    with FFmpeg(file) as ffmpeg:
        sticker = ffmpeg.cv_to_webp(
            enforce_not_broken=enforce_not_broken,
            animated_gif=animated_gif,
            max_sticker_size=MAX_STICKER_SIZE,
            is_webm=is_webm,
        )
    if not WEBPMUX_IS_AVAILABLE:
        return sticker, False

    exif_filename = TemporaryFile(prefix=None, touch=False).__enter__()
    with open(exif_filename.path, "wb") as file:
        file.write(add_exif(name=name, packname=packname))
    temp = tempfile.gettempdir() + "/" + f"{uuid.uuid4()}" + ".webp"
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
    exif_filename.__exit__(None, None, None)
    with open(temp, "rb") as file:
        buf = file.read()
    os.remove(temp)
    return buf, True


astick_sem = asyncio.Semaphore(20)


async def aio_convert_to_webp(
    sticker, name, packname, crop=False, passthrough=True, transparent=False
):
    sticker = await get_bytes_from_name_or_url_async(sticker)
    animated = is_webm = is_image = saved_exif = stk = False
    mime = magic.from_buffer(sticker, mime=True)
    if mime == "image/webp":
        io_save = BytesIO(sticker)
        img = Image.open(io_save)
        if len(ImageSequence.all_frames(img)) < 2:
            is_image = True
    elif passthrough:
        raise ConvertStickerError(
            "File is not a webp, which is required for passthrough."
        )
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
        async with astick_sem:
            sticker, saved_exif = await aio_convert_to_sticker(
                sticker,
                name,
                packname,
                enforce_not_broken=True,
                animated_gif=transparent,
                is_webm=is_webm,
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


stick_sem = threading.Semaphore(20)


def convert_to_webp(
    sticker, name, packname, crop=False, passthrough=True, transparent=False
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
        raise ConvertStickerError(
            "File is not a webp, which is required for passthrough."
        )
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
