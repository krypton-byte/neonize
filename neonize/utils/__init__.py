import logging
import os
import subprocess
from io import BytesIO

import magic
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


def vid_to_webp(file: str | bytes) -> BytesIO:
    buff = BytesIO(get_bytes_from_name_or_url(file))
    filename = save_file_to_temp_directory(buff.getvalue())
    output = filename + ".webp"
    ffmpeg_command = [
        "ffmpeg",
        "-v", "quiet",
        "-i", filename,
        "-vcodec", "libwebp",
        "-ss", "00:00:00.0",
        "-t", "00:00:06.0",
        "-vf", (
            f"scale='min(320,iw)':min'(320,ih)':force_original_aspect_ratio=decrease,fps=15, "
            f"pad=320:320:-1:-1:color=white@0.0, split [a][b]; [a] "
            f"palettegen=reserve_transparent=on:transparency_color=ffffff [p]; [b][p] paletteuse"
        ),
        output
    ]
    subprocess.call(ffmpeg_command)
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
