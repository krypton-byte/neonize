from io import BytesIO
from moviepy.editor import VideoFileClip
from .iofile import (
    get_bytes_from_name_or_url,
)
from .thumbnail import save_file_to_temp_directory
import logging
import magic
from pydub import AudioSegment
from phonenumbers import parse, PhoneNumberFormat, format_number

log = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d [%(name)s %(levelname)s] - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


def get_duration(file: str | bytes) -> float:
    buff = BytesIO(get_bytes_from_name_or_url(file))
    _type = magic.from_buffer(buff.read(), mime=True).split("/")[0]
    filename, temp_file = save_file_to_temp_directory(buff.getvalue())
    aud_or_vid = (
        AudioSegment.from_file(filename)
        if _type == "audio"
        else VideoFileClip(filename)
    )
    temp_file.close()
    return aud_or_vid.duration if _type == "video" else len(aud_or_vid) / 1000


def gen_vcard(name: str, phone_number: str) -> str:
    inter_phone_number = format_number(
        parse(f"{'+' if phone_number[0] != '+' else ''}{phone_number}"),
        PhoneNumberFormat.INTERNATIONAL,
    )
    return (
        f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nitem1.TEL;waid={phone_number}"
        f":{inter_phone_number}\nitem1.X-ABLabel:Ponsel\nEND:VCARD"
    )
