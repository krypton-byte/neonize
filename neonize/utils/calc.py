from io import BytesIO
from typing import Tuple
from PIL import Image


from PIL import Image


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


def AspectRatioMethod(
    width: int | float, height: int | float, res: int = 1280
) -> Tuple[int, int]:
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
