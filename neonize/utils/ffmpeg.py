import asyncio
from enum import Enum
import json
import os
import shlex
import time
import subprocess
import tempfile
import logging
from typing import List, Optional, Tuple
from dataclasses import dataclass
from .iofile import (
    URL_MATCH,
    TemporaryFile,
    get_bytes_from_name_or_url,
    get_bytes_from_name_or_url_async,
)

log = logging.getLogger(__name__)


class ImageFormat(Enum):
    """
    Enumeration for image formats.

    Attributes:
        JPG (str): JPEG format identifier.
        PNG (str): PNG format identifier.
    """

    JPG = "mjpeg"
    PNG = "apng"


@dataclass
class Stream:
    """
    Data class representing a stream in multimedia.

    Attributes:
        index (int): Index of the stream.
        codec_type (str): Type of codec used in the stream.
        avg_frame_rate (str): Average frame rate of the stream.
        codec_tag_string (str): Codec tag string.
        start_pts (int): Starting presentation timestamp.
        tags (dict): Tags associated with the stream.
        extradata_size (int): Size of the extra data.
        start_time (str): Start time of the stream.
        disposition (dict): Disposition of the stream.
        codec_tag (str): Codec tag.
        time_base (str): Time base.
        codec_long_name (str): Long name of the codec.
        codec_name (str): Name of the codec.
        r_frame_rate (str): Real frame rate.
        closed_captions (Optional[int]): Closed captions (Video field).
        color_range (Optional[str]): Color range.
        display_aspect_ratio (Optional[str]): Display aspect ratio.
        color_transfer (Optional[str]): Color transfer.
        is_avc (Optional[str]): AVC flag.
        color_primaries (Optional[str]): Color primaries.
        film_grain (Optional[int]): Film grain.
        color_space (Optional[str]): Color space.
        refs (Optional[int]): Number of reference frames.
        level (Optional[int]): Codec level.
        nal_length_size (Optional[str]): NAL length size.
        chroma_location (Optional[str]): Chroma location.
        has_b_frames (Optional[int]): B-frames flag.
        pix_fmt (Optional[str]): Pixel format.
        sample_aspect_ratio (Optional[str]): Sample aspect ratio.
        bits_per_raw_sample (Optional[str]): Bits per raw sample.
        profile (Optional[str]): Codec profile.
        field_order (Optional[str]): Field order.
        width (Optional[int]): Width of the video frame.
        height (Optional[int]): Height of the video frame.
        coded_width (Optional[int]): Coded width of the video frame.
        coded_height (Optional[int]): Coded height of the video frame.
        bits_per_sample (Optional[int]): Bits per sample (Audio field).
        sample_fmt (Optional[str]): Sample format.
        channel_layout (Optional[str]): Channel layout.
        initial_padding (Optional[int]): Initial padding.
        channels (Optional[int]): Number of channels.
        sample_rate (Optional[str]): Sample rate.
    """

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
    closed_captions: Optional[int] = None
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
    bits_per_sample: Optional[int] = None
    sample_fmt: Optional[str] = None
    channel_layout: Optional[str] = None
    initial_padding: Optional[int] = None
    channels: Optional[int] = None
    sample_rate: Optional[str] = None


@dataclass
class Format:
    """
    Data class representing the format of multimedia content.

    Attributes:
        filename (str): Name of the file.
        nb_streams (int): Number of streams in the file.
        nb_programs (int): Number of programs in the file.
        format_name (str): Name of the format.
        format_long_name (str): Long name of the format.
        start_time (float): Start time of the format.
        duration (float): Duration of the content.
        size (int): Size of the file in bytes.
        probe_score (int): Probe score of the file.
        tags (dict): Tags associated with the format.
    """

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
    """
    Data class representing FFProbe information for a media file.

    Attributes:
        format (Format): The format information of the media file.
        streams (List[Stream]): List of streams in the media file.
    """

    format: Format
    streams: List[Stream]


class AFFmpeg:
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
        self.__file_data = data
        self.prefix = prefix

    async def __aenter__(self):
        if isinstance(self.__file_data, str):
            if URL_MATCH.match(self.__file_data):
                self.filename = TemporaryFile(prefix=self.prefix, touch=False).__enter__()
                with open(self.filename.path, "wb") as file:
                    file.write(await get_bytes_from_name_or_url_async(self.__file_data))
            else:
                self.filename = self.__file_data
        else:
            self.filename = TemporaryFile(prefix=self.prefix, touch=False).__enter__()
            with open(self.filename.path, "wb") as file:
                file.write(self.__file_data)
        return self

    async def __aexit__(self, *args, **kwargs):
        if not isinstance(self.filename, str):
            self.filename.__exit__(None, None, None)

    @property
    def filepath(self):
        if isinstance(self.filename, str):
            return self.filename
        return self.filename.path.__str__()

    async def cv_to_webp(self, animated: bool = True, enforce_not_broken: bool = False) -> bytes:
        """
        This function converts a given file to webp format using ffmpeg.
        If the animated flag is set to True, it will only convert the first 6 seconds of the file.

        :param animated: If True, only the first 6 seconds of the file will be converted, defaults to True
        :type animated: bool, optional
        :param enforce_not_broken: Enforce non-broken stickers by constraining sticker size to WA limits, defaults to False
        :type enforce_not_broken: bool, optional
        :return: The converted file in bytes
        :rtype: bytes
        """
        MAX_STICKER_FILESIZE = 512000
        temp = tempfile.gettempdir() + "/" + time.time().__str__() + ".webp"
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            self.filepath,
            "-vcodec",
            "libwebp",
            "-vf",
            (
                "scale='if(gt(iw,ih),512,-1)':'if(gt(iw,ih),-1,512)',fps=15, "
                "pad=512:512:-1:-1:color=white@0.0, split [a][b]; [a] "
                "palettegen=reserve_transparent=on:transparency_color=ffffff [p]; [b][p] paletteuse"
            ),
        ]
        if enforce_not_broken:
            duration = int((await self.extract_info()).format.duration)
            if not duration:
                duration = 1
            if duration > 6 and animated:
                duration = 6
            bitrate = f"{MAX_STICKER_FILESIZE // duration}k"
            ffmpeg_command.extend(
                [
                    "-loop",
                    "0",
                    "-preset",
                    "picture",
                    "-fs",
                    f"{MAX_STICKER_FILESIZE}",
                    "-q:v",
                    bitrate,
                ]
            )
        if animated:
            ffmpeg_command.extend(
                [
                    "-ss",
                    "00:00:00.0",
                    "-t",
                    "00:00:06.0",
                ]
            )
        ffmpeg_command.append(temp)
        await self.call(ffmpeg_command)
        with open(temp, "rb") as file:
            buf = file.read()
        os.remove(temp)
        return buf

    async def call(self, cmd: List[str]):
        cmd_str = shlex.join(cmd) if any(" " in part for part in cmd) else " ".join(cmd)
        popen = await asyncio.create_subprocess_shell(
            cmd_str if os.name == "nt" else shlex.join(cmd),
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            # shell=True if os.name == "nt" else False,
        )
        stdout, stderr = await popen.communicate()  # type: ignore
        if popen.returncode != 0:
            raise RuntimeError(
                f"stderr: {stderr} Return code: {popen.returncode}"  # type: ignore
            )
        return stdout

    async def gif_to_mp4(self) -> bytes:
        """
        This function convertes a gif to mp4 format.
        """
        temp = tempfile.gettempdir() + "/" + time.time().__str__() + ".mp4"
        await self.call(
            [
                "ffmpeg",
                "-i",
                self.filepath,
                "-movflags",
                "faststart",
                "-pix_fmt",
                "yuv420p",
                "-vf",
                "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                "-crf",
                "17",
                temp,
            ]
        )
        with open(temp, "rb") as file:
            buf = file.read()
        os.remove(temp)
        return buf

    async def to_mp3(self) -> bytes:
        temp = tempfile.gettempdir() + "/" + time.time().__str__() + ".mp3"
        await self.call(
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

    async def extract_thumbnail(
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
            for stream in (await self.extract_info()).streams:
                if stream.codec_type == "video":
                    extra.extend(
                        [
                            "-vf",
                            "scale='if(gt(iw,ih),%i,-1)':'if(gt(iw,ih),-1,%i)'" % (size, size),
                        ]
                    )
        elif isinstance(size, Tuple):
            extra.extend(["-s", "x".join(map(str, size))])
        return await self.call(
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

    async def extract_info(self) -> FFProbeInfo:
        """
        Extracts media file information using ffprobe tool.

        This method uses ffprobe, a tool from the FFmpeg package, to extract
        information about a media file. It returns the information in the form of
        an FFProbeInfo object, which contains the format and streams of the media file.

        :return: An FFProbeInfo object containing the format and streams of the media file.
        :rtype: FFProbeInfo
        """
        data = json.loads(
            await self.call(
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
                **{i: format.get(i, None) for i, _ in Format.__dataclass_fields__.items()}
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

    def cv_to_webp(self, animated: bool = True, enforce_not_broken: bool = False) -> bytes:
        """
        This function converts a given file to webp format using ffmpeg.
        If the animated flag is set to True, it will only convert the first 6 seconds of the file.

        :param animated: If True, only the first 6 seconds of the file will be converted, defaults to True
        :type animated: bool, optional
        :param enforce_not_broken: Enforce non-broken stickers by constraining sticker size to WA limits, defaults to False
        :type enforce_not_broken: bool, optional
        :return: The converted file in bytes
        :rtype: bytes
        """
        MAX_STICKER_FILESIZE = 512000
        temp = tempfile.gettempdir() + "/" + time.time().__str__() + ".webp"
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            self.filepath,
            "-vcodec",
            "libwebp",
            "-vf",
            (
                "scale='if(gt(iw,ih),512,-1)':'if(gt(iw,ih),-1,512)',fps=15, "
                "pad=512:512:-1:-1:color=white@0.0, split [a][b]; [a] "
                "palettegen=reserve_transparent=on:transparency_color=ffffff [p]; [b][p] paletteuse"
            ),
        ]
        if enforce_not_broken:
            duration = int(self.extract_info().format.duration)
            if not duration:
                duration = 1
            if duration > 6 and animated:
                duration = 6
            bitrate = f"{MAX_STICKER_FILESIZE // duration}k"
            ffmpeg_command.extend(
                [
                    "-loop",
                    "0",
                    "-preset",
                    "picture",
                    "-fs",
                    f"{MAX_STICKER_FILESIZE}",
                    "-q:v",
                    bitrate,
                ]
            )
        if animated:
            ffmpeg_command.extend(
                [
                    "-ss",
                    "00:00:00.0",
                    "-t",
                    "00:00:06.0",
                ]
            )
        ffmpeg_command.append(temp)
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

    def gif_to_mp4(self) -> bytes:
        """
        This function convertes a gif to mp4 format.
        """
        temp = tempfile.gettempdir() + "/" + time.time().__str__() + ".mp4"
        self.call(
            [
                "ffmpeg",
                "-i",
                self.filepath,
                "-movflags",
                "faststart",
                "-pix_fmt",
                "yuv420p",
                "-vf",
                "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                "-crf",
                "17",
                temp,
            ]
        )
        with open(temp, "rb") as file:
            buf = file.read()
        os.remove(temp)
        return buf

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
                            "scale='if(gt(iw,ih),%i,-1)':'if(gt(iw,ih),-1,%i)'" % (size, size),
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
                **{i: format.get(i, None) for i, _ in Format.__dataclass_fields__.items()}
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
