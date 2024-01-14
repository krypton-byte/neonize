import os
import random
import string
import tempfile
from io import BytesIO

import magic
from PIL import Image
from moviepy.editor import VideoFileClip

from .iofile import get_bytes_from_name_or_url


def save_file_to_temp_directory(data: bytes) -> str:
    temp_dir = tempfile.gettempdir()
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    temp_file_name = temp_dir + "/" + random_string

    with open(temp_file_name, "wb") as temp_file:
        temp_file.write(data)

    return temp_file_name


def generate_thumbnail(
    file: str | bytes, thumbnail_size: tuple[int, int] = (200, 200)
) -> bytes:
    buff = BytesIO(get_bytes_from_name_or_url(file))
    byte_stream = BytesIO()
    _type = magic.from_buffer(buff.read(), mime=True).split("/")[0]
    if _type == "image":
        image = Image.open(buff)
        image.thumbnail(thumbnail_size)

        image.save(byte_stream, format="JPEG")
    elif _type == "video":
        filename = save_file_to_temp_directory(buff.getvalue())
        video = VideoFileClip(filename)
        frame = video.get_frame(0)  # Get the first frame of the video
        frame_image = Image.fromarray(frame)
        frame_image.thumbnail(thumbnail_size)

        frame_image.save(byte_stream, format="JPEG")
        os.remove(filename)

    return byte_stream.getvalue()
