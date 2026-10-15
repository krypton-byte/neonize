from neonize.proto.Neonize_pb2 import UploadResponse
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import AudioMessage, VideoMessage
from neonize.utils.enum import MediaType
from neonize.utils.newsletter_status import build_newsletter_status_media_message


def test_build_image_newsletter_status_payload_is_plaintext_media():
    upload = UploadResponse(
        url="https://mmg.whatsapp.net/file",
        DirectPath="/m1/file",
        Handle="newsletter-handle",
        FileSHA256=b"sha256",
        FileLength=123,
    )

    message = build_newsletter_status_media_message(
        upload, MediaType.MediaImage, "image/jpeg", "Story caption"
    )

    assert message.imageMessage.URL == upload.url
    assert message.imageMessage.directPath == upload.DirectPath
    assert message.imageMessage.fileSHA256 == upload.FileSHA256
    assert message.imageMessage.fileLength == upload.FileLength
    assert message.imageMessage.mimetype == "image/jpeg"
    assert message.imageMessage.caption == "Story caption"
    assert not message.imageMessage.mediaKey
    assert not message.imageMessage.fileEncSHA256


def test_build_video_and_audio_newsletter_status_payloads():
    upload = UploadResponse(
        url="https://mmg.whatsapp.net/file",
        DirectPath="/m1/file",
        FileSHA256=b"hash",
        FileLength=50,
    )

    video = build_newsletter_status_media_message(
        upload, MediaType.MediaVideo, "video/mp4", "Video caption"
    )
    audio = build_newsletter_status_media_message(
        upload, MediaType.MediaAudio, "audio/ogg", None
    )

    assert isinstance(video.videoMessage, VideoMessage)
    assert video.videoMessage.caption == "Video caption"
    assert isinstance(audio.audioMessage, AudioMessage)
    assert audio.audioMessage.PTT is False
    assert not audio.audioMessage.mediaKey


def test_reject_unsupported_newsletter_status_media_type():
    upload = UploadResponse(url="https://mmg.whatsapp.net/file")

    try:
        build_newsletter_status_media_message(
            upload, MediaType.MediaDocument, "application/pdf"
        )
    except ValueError as exc:
        assert "image, video, or audio" in str(exc)
    else:
        raise AssertionError("document payloads must be rejected for Channel Stories")
