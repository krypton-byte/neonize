"""Helpers for constructing WhatsApp Channel Status payloads."""

from ..proto.Neonize_pb2 import UploadResponse
from ..proto.waE2E.WAWebProtobufsE2E_pb2 import (
    AudioMessage,
    ImageMessage,
    Message,
    VideoMessage,
)
from .enum import MediaType


def build_newsletter_status_media_message(
    upload: UploadResponse,
    media_type: MediaType,
    mimetype: str,
    caption: str | None = None,
) -> Message:
    """Build an unencrypted media message for ``status@newsletter`` uploads."""
    shared_fields = {
        "URL": upload.url,
        "directPath": upload.DirectPath,
        "fileSHA256": upload.FileSHA256,
        "fileLength": upload.FileLength,
        "mimetype": mimetype,
    }
    if media_type == MediaType.MediaImage:
        return Message(
            imageMessage=ImageMessage(caption=caption, **shared_fields),
        )
    if media_type == MediaType.MediaVideo:
        return Message(
            videoMessage=VideoMessage(caption=caption, **shared_fields),
        )
    if media_type == MediaType.MediaAudio:
        return Message(
            audioMessage=AudioMessage(PTT=False, **shared_fields),
        )
    raise ValueError("Channel Stories only support image, video, or audio media")
