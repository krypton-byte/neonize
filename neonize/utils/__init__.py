import json
import logging
import os
import re
import subprocess
from io import BytesIO

import magic
from PIL import Image
from moviepy.editor import VideoFileClip
from phonenumbers import parse, PhoneNumberFormat, format_number
from pydub import AudioSegment

from .iofile import (
    get_bytes_from_name_or_url,
)
from .thumbnail import save_file_to_temp_directory

log = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d [%(name)s %(levelname)s] - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


def add_exif(name: str = "", packname: str = "") -> bytes:
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


def get_duration(file: str | bytes) -> float:
    buff = BytesIO(get_bytes_from_name_or_url(file))
    _type = magic.from_buffer(buff.read(), mime=True).split("/")[0]
    filename = save_file_to_temp_directory(buff.getvalue())
    aud_or_vid = (
        AudioSegment.from_file(filename)
        if _type == "audio"
        else VideoFileClip(filename)
    )
    os.remove(filename)
    return aud_or_vid.duration if _type == "video" else len(aud_or_vid) / 1000


def cv_to_webp(
    file: str | bytes, is_video: bool = False, name: str = "", packname: str = ""
) -> BytesIO:
    buff = BytesIO(get_bytes_from_name_or_url(file))
    filename = save_file_to_temp_directory(buff.getvalue())
    output = filename + ".webp"
    ffmpeg_command = [
        "ffmpeg",
        "-v",
        "quiet",
        "-i",
        filename,
        "-vcodec",
        "libwebp",
        "-vf",
        (
            f"scale='if(gt(iw,ih),320,-1)':'if(gt(iw,ih),-1,320)',fps=15, "
            f"pad=320:320:-1:-1:color=white@0.0, split [a][b]; [a] "
            f"palettegen=reserve_transparent=on:transparency_color=ffffff [p]; [b][p] paletteuse"
        ),
        output,
    ]
    if is_video:
        ffmpeg_command.extend(
            [
                "-ss",
                "00:00:00.0",
                "-t",
                "00:00:06.0",
            ]
        )
    subprocess.call(ffmpeg_command)
    if name or packname:
        exif = add_exif(name, packname)
        Image.open(output).save(output, format="webp", exif=exif, save_all=True)
    res = BytesIO(get_bytes_from_name_or_url(output))
    os.remove(filename)
    os.remove(output)
    return res


def gen_vcard(name: str, phone_number: str) -> str:
    inter_phone_number = format_number(
        parse(f"{'+' if phone_number[0] != '+' else ''}{phone_number}"),
        PhoneNumberFormat.INTERNATIONAL,
    )
    return (
        f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nitem1.TEL;waid={phone_number}"
        f":{inter_phone_number}\nitem1.X-ABLabel:Ponsel\nEND:VCARD"
    )


def validate_link(link) -> bool:
    url_pattern = re.compile(
        r"^(https?|ftp)://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
        r"\[?[A-F0-9]*:[A-F0-9:]+]?)"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return bool(re.match(url_pattern, link))
