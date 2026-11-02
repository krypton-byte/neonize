import hashlib
import hmac
import math
from io import BytesIO

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from PIL import Image

MEDIA_KEY_INFO = {
    "video": b"WhatsApp Video Keys",
    "image": b"WhatsApp Image Keys",
    "audio": b"WhatsApp Audio Keys",
    "document": b"WhatsApp Document Keys",
}


def get_media_keys(media_key: bytes, app_info: bytes):
    """Direct port of whatsmeow's getMediaKeys()"""
    expanded = HKDF(
        algorithm=hashes.SHA256(),
        length=112,
        salt=None,
        info=app_info,
    ).derive(media_key)

    return (
        expanded[0:16],  # iv
        expanded[16:48],  # cipher_key
        expanded[48:80],  # mac_key
        expanded[80:],  # ref_key (unused in upload)
    )


def get_sidecar_from_upload(plaintext: bytes, media_key: bytes, media_type: str = "video") -> bytes:
    iv, cipher_key, mac_key, _ = get_media_keys(media_key, MEDIA_KEY_INFO[media_type])

    cipher = AES.new(cipher_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, 16))
    mac = hmac.new(mac_key, iv + ciphertext, hashlib.sha256).digest()[:10]

    return generate_streaming_sidecar(ciphertext + mac, iv, mac_key)


def generate_streaming_sidecar(ciphertext: bytes, iv: bytes, mac_key: bytes) -> bytes:
    CHUNK_SIZE = 64 * 1024
    IV_LENGTH = 16
    HMAC_LENGTH = 10

    full_data = iv + ciphertext
    data_size = len(full_data)
    num_chunks = math.ceil((data_size - IV_LENGTH) / CHUNK_SIZE)

    sidecar = bytearray(num_chunks * HMAC_LENGTH)

    for c in range(num_chunks):
        start = c * CHUNK_SIZE
        end = min(start + IV_LENGTH + CHUNK_SIZE, data_size)
        chunk = full_data[start:end]

        sig = hmac.new(mac_key, chunk, hashlib.sha256).digest()[:HMAC_LENGTH]
        sidecar[c * HMAC_LENGTH : (c + 1) * HMAC_LENGTH] = sig

    return bytes(sidecar)


def crop_image(image: Image.Image) -> Image.Image:
    """
    Crops an image to make it square. If the image is already square, it is returned as is.
    If the image is not square, the longer dimension is cropped equally from both sides to make it square.

    :param image: An image that needs to be cropped
    :type image: Image.Image
    :return: A square cropped image
    :rtype: Image.Image
    """
    width, height = image.size
    if width == height:
        return image
    offset = int(abs(height - width) / 2)
    if width > height:
        image = image.crop([offset, 0, width - offset, height])  # type: ignore
    else:
        image = image.crop([0, offset, width, height - offset])  # type: ignore
    return image


def AspectRatioMethod(width: float, height: float, res: int = 1280) -> tuple[int, int]:
    """Calculate the aspect ratio of a given width and height with respect to a resolution.

    :param width: The width of the given area.
    :type width: int | float
    :param height: The height of the given area.
    :type height: int | float
    :param res: The resolution to calculate the aspect ratio with, defaults to 1280.
    :type res: int, optional
    :return: A tuple containing the calculated width and height based on the aspect ratio.
    :rtype: Tuple[int, int]
    """
    if width > height:
        return (res, int(width / (width / res)))
    elif width < height:
        return (int(width / (height / res)), res)
    return (res, res)


def sticker_scaler(fn: str | BytesIO | Image.Image):
    """
    This function rescales an image to a maximum dimension of 512 pixels while maintaining the aspect ratio.
    The function takes the filename of the image as an input and returns the rescaled image.

    :param fn: Filename of the image to be rescaled
    :type fn: str
    :return: Rescaled image
    :rtype: PIL.Image.Image
    """
    img = fn if isinstance(fn, Image.Image) else Image.open(fn)
    width, height = AspectRatioMethod(*img.size, 512)
    return img.resize((int(width), int(height)))


def auto_sticker(fn: str | BytesIO | Image.Image):
    """
    This function creates a new sticker image with a specified size (512 x 512).
    The original image is placed at the center of the new sticker.

    :param fn: The file name of the original image.
    :type fn: str
    :return: The new sticker image with the original image at the center.
    :rtype: Image object
    """
    img = fn if isinstance(fn, Image.Image) else Image.open(fn)
    new_layer = Image.new("RGBA", (512, 512), color=(0, 0, 0, 0))
    new_layer.paste(img, (256 - (int(img.width / 2)), 256 - (int(img.height / 2))))
    return new_layer


def original_sticker(image: str | BytesIO | Image.Image):
    """
    This function creates a new sticker image with a square background.
    The original image is placed at the center of the new sticker.

    :param image: The file name of the original image.
    :return: The new sticker image with the original image at the center (uncropped).
    :rtype: Image object
    """
    img = image if isinstance(image, Image.Image) else Image.open(image)
    orig_width, orig_height = img.size
    square_size = max(orig_width, orig_height)
    square_img = Image.new("RGBA", (square_size, square_size), (0, 0, 0, 0))
    x_offset = (square_size - orig_width) // 2
    y_offset = (square_size - orig_height) // 2
    square_img.paste(img, (x_offset, y_offset), img if img.mode == "RGBA" else None)
    return square_img
