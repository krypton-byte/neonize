from enum import Enum
import json
import os
import time
import subprocess
import tempfile
import logging
from typing import List, Optional, Tuple
from dataclasses import dataclass
from .iofile import URL_MATCH, TemporaryFile, get_bytes_from_name_or_url

log = logging.getLogger(__name__)


class ImageFormat(Enum):
    JPG = "mjpeg"
    PNG = "apng"


@dataclass
class Stream:
    index: int
    codec_type: str
    avg_frame_rate: str
    codec_tag_string: str
    start_pts: int
    tags: dict
    extradata_size: int
    start_time: str
    disposition: dict
    codec_tag: str
    time_base: str
    codec_long_name: str
    codec_name: str
    r_frame_rate: str
    closed_captions: Optional[int] = None  # Video Field
    color_range: Optional[str] = None
    display_aspect_ratio: Optional[str] = None
    color_transfer: Optional[str] = None
    is_avc: Optional[str] = None
    color_primaries: Optional[str] = None
    film_grain: Optional[int] = None
    color_space: Optional[str] = None
    refs: Optional[int] = None
    level: Optional[int] = None
    nal_length_size: Optional[str] = None
    chroma_location: Optional[str] = None
    has_b_frames: Optional[int] = None
    pix_fmt: Optional[str] = None
    sample_aspect_ratio: Optional[str] = None
    bits_per_raw_sample: Optional[str] = None
    profile: Optional[str] = None
    field_order: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    coded_width: Optional[int] = None
    coded_height: Optional[int] = None
    bits_per_sample: Optional[int] = None  # Audio Field
    sample_fmt: Optional[str] = None
    channel_layout: Optional[str] = None
    initial_padding: Optional[int] = None
    channels: Optional[int] = None
    sample_rate: Optional[str] = None


@dataclass
class Format:
    filename: str
    nb_streams: int
    nb_programs: int
    format_name: str
    format_long_name: str
    start_time: float
    duration: float
    size: int
    probe_score: int
    tags: dict

    def __post_init__(self):
        for k, field in self.__class__.__dataclass_fields__.items():
            try:
                setattr(self, k, field.type(getattr(self, k)))
            except Exception as e:
                log.warn(f"{k} field: {e}")


@dataclass
class FFProbeInfo:
    format: Format
    streams: List[Stream]


class FFmpeg:
    def __init__(self, data: bytes | str, prefix: Optional[str] = None) -> None:
        """
        Initializes the FFmpeg class. If the data is a URL, it retrieves the data from the URL
        and writes it to a temporary file. If the data is a string that is not a URL, it treats
        the string as a filename. If the data is bytes, it writes the bytes to a temporary file.

        :param data: The input data. This can be a URL, a filename, or bytes.
        :type data: bytes | str
        :param prefix: The prefix for the temporary file, if one is created. If None, no prefix is used.
        :type prefix: Optional[str], optional
        """
        if isinstance(data, str):
            if URL_MATCH.match(data):
                self.filename = TemporaryFile(prefix=prefix, touch=False).__enter__()
                with open(self.filename.path, "wb") as file:
                    file.write(get_bytes_from_name_or_url(data))
            else:
                self.filename = data
        else:
            self.filename = TemporaryFile(prefix=prefix, touch=False).__enter__()
            with open(self.filename.path, "wb") as file:
                file.write(data)

    def __enter__(self):
        return self

    def __exit__(self, *ex):
        if not isinstance(self.filename, str):
            self.filename.__exit__(None, None, None)

    @property
    def filepath(self):
        if isinstance(self.filename, str):
            return self.filename
        return self.filename.path.__str__()

    def cv_to_webp(self, animated: bool = True) -> bytes:
        """
        This function converts a given file to webp format using ffmpeg.
        If the animated flag is set to True, it will only convert the first 6 seconds of the file.

        :param animated: If True, only the first 6 seconds of the file will be converted, defaults to True
        :type animated: bool, optional
        :return: The converted file in bytes
        :rtype: bytes
        """
        temp = tempfile.gettempdir() + "/" + time.time().__str__() + ".webp"
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            self.filepath,
            "-vcodec",
            "libwebp",
            "-vf",
            (
                f"scale='if(gt(iw,ih),512,-1)':'if(gt(iw,ih),-1,512)',fps=15, "
                f"pad=512:512:-1:-1:color=white@0.0, split [a][b]; [a] "
                f"palettegen=reserve_transparent=on:transparency_color=ffffff [p]; [b][p] paletteuse"
            ),
            temp,
        ]
        if animated:
            ffmpeg_command.extend(
                [
                    "-ss",
                    "00:00:00.0",
                    "-t",
                    "00:00:06.0",
                ]
            )
        self.call(ffmpeg_command)
        with open(temp, "rb") as file:
            buf = file.read()
        os.remove(temp)
        return buf

    def call(self, cmd: List[str]):
        popen = subprocess.Popen(
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
        )
        out = popen.stdout.read()  # type: ignore
        popen.wait(10)
        if popen.returncode != 0:
            raise RuntimeError(
                f"stderr: {popen.stderr.read().decode()} Return code: {popen.returncode}"  # type: ignore
            )
        return out

    def to_mp3(self) -> bytes:
        temp = tempfile.gettempdir() + "/" + time.time().__str__() + ".mp3"
        self.call(
            [
                "ffmpeg",
                "-i",
                self.filepath,
                "-vn",
                "-ar",
                "44100",
                "-ac",
                "2",
                "-b:a",
                "192k",
                temp,
            ]
        )
        with open(temp, "rb") as file:
            buf = file.read()
        os.remove(temp)
        return buf

    def extract_thumbnail(
        self,
        format: ImageFormat = ImageFormat.JPG,
        size: Optional[Tuple[int, int] | int] = 200,
    ) -> bytes:
        """
        Extracts a thumbnail from a video file.

        :param format: The format of the output thumbnail, defaults to ImageFormat.JPG
        :type format: ImageFormat, optional
        :param size: The size of the output thumbnail. If an integer is provided, the thumbnail will be scaled
                     while maintaining the aspect ratio. If a tuple of two integers is provided, it will be used
                     as the exact dimensions for the thumbnail, defaults to 200
        :type size: Optional[Tuple[int, int]  |  int], optional
        :return: The bytes representing the thumbnail image.
        :rtype: bytes
        """
        extra = []
        if isinstance(size, int):
            for stream in self.extract_info().streams:
                if stream.codec_type == "video":
                    extra.extend(
                        [
                            "-vf",
                            "scale='if(gt(iw,ih),%i,-1)':'if(gt(iw,ih),-1,%i)'"
                            % (size, size),
                        ]
                    )
        elif isinstance(size, Tuple):
            extra.extend(["-s", "x".join(map(str, size))])
        return self.call(
            [
                "ffmpeg",
                "-i",
                self.filepath,
                "-vframes",
                "1",
                "-an",
                *extra,
                "-f",
                format.value,
                "-",
            ]
        )

    def extract_info(self) -> FFProbeInfo:
        """
        Extracts media file information using ffprobe tool.

        This method uses ffprobe, a tool from the FFmpeg package, to extract
        information about a media file. It returns the information in the form of
        an FFProbeInfo object, which contains the format and streams of the media file.

        :return: An FFProbeInfo object containing the format and streams of the media file.
        :rtype: FFProbeInfo
        """
        data = json.loads(
            self.call(
                [
                    "ffprobe",
                    "-i",
                    self.filepath,
                    "-print_format",
                    "json",
                    "-show_format",
                    "-show_streams",
                ]
            )
        )
        streams: List[dict] = data["streams"]
        format: dict = data["format"]
        return FFProbeInfo(
            format=Format(
                **{
                    i: format.get(i, None)
                    for i, _ in Format.__dataclass_fields__.items()
                }
            ),
            streams=[
                Stream(
                    **{
                        field: data.get(field, None)
                        for field, _ in Stream.__dataclass_fields__.items()
                    }
                )
                for data in streams
            ],
        )
