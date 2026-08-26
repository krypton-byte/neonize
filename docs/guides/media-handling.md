# Media Handling

## Sources Accepted

Media methods accept three input kinds interchangeably:

| Source | Example |
| --- | --- |
| Local path | `"/tmp/photo.jpg"` |
| Raw bytes | `open("photo.jpg", "rb").read()` |
| URL | `"https://example.com/photo.jpg"` |

```python
client.send_image(chat, "https://download.samplelib.com/png/sample-boat-400x300.png")
```

## Sending Media

```python
# Image with caption, as a reply, marked view-once
client.send_image(chat, "photo.jpg", caption="Sunset", quoted=ev.Message, viewonce=True)

# Video with caption and GIF-style looping playback
client.send_video(chat, "clip.mp4", caption="Loop", gifplayback=True)

# Voice note (push-to-talk) vs music audio
client.send_audio(chat, "voice.ogg", ptt=True)
client.send_audio(chat, "song.mp3")

# Document with explicit filename shown to the recipient
client.send_document(chat, "report.pdf", filename="Q3-report.pdf", caption="Report")
```

## Stickers

`send_sticker` converts any image or short video into a WhatsApp sticker.
FFmpeg is required for the conversion.

```python
client.send_sticker(chat, "meme.png")
client.send_sticker(chat, "meme.png", name="Bot", packname="MyPack")  # with EXIF metadata
```

For multiple stickers at once:

```python
files = ["1.png", "2.png", "3.webp"]
for msg in client.build_stickerpack_message(files, packname="Pack", publisher="Me"):
    client.send_message(chat, msg)
```

The pack builder chunks automatically (WhatsApp limits packs to 60 stickers,
each under 1 MB).

## Albums

```python
responses = client.send_album(chat, ["a.jpg", "b.jpg"], caption="Gallery")
```

## Uploading Without Sending

To upload media once and reference it yourself:

```python
from neonize.utils.enum import MediaType

resp = client.upload(png_bytes, MediaType.Photo)
print(resp.URL)   # hosted URL; resp.DirectPath, .MediaKey, ...
```

## Downloading Incoming Media

```python
@client.event(MessageEv)
def on_message(client: NewClient, ev: MessageEv) -> None:
    payload = ev.Message
    if payload.imageMessage:
        data = client.download_any(payload)             # bytes
        client.download_any(payload, f"img/{ev.Info.ID}.jpg")  # or save
```

## Building Message Payloads Manually

Every send method has a `build_*_message` counterpart returning a protobuf
`Message` you can pass to `send_message` — useful for combining media with
interactive elements:

```python
msg = client.build_image_message("photo.jpg", caption="Built manually")
client.send_message(chat, msg)
```

Available builders: `build_image_message`, `build_video_message`,
`build_audio_message`, `build_document_message`, `build_sticker_message`,
`build_stickerpack_message`, `build_album_content`.

## FFmpeg Notes

- Required for sticker conversion and audio transcoding.
- Thumbnails for videos/documents are extracted via `neonize.utils.ffmpeg`.
- If FFmpeg is missing, conversion methods raise `FFProbeError` /
  `ConvertStickerError`; plain text sends are unaffected.

!!! warning "Size limits"
    WhatsApp rejects media above roughly 16 MB for images/audio and 100 MB
    for video/documents. Oversized uploads raise `UploadError`.
