from PIL import Image


def CropMethod(image: Image.Image):
    """
    resize image resolution ratio 1:1
    fn : filename (*.jpg, *.png etc)
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


def ScaleMethod(x, y, res=1280):
    if x > y:
        return [res, int(y / (x / res))]
    elif x < y:
        return [int(x / (y / res)), res]
    return [res, res]


def sticker_scaler(fn):
    """
    fn : filename (*.jpg, *.png etc)
    resize: 512x512
    """
    img = Image.open(fn)
    width, height = ScaleMethod(*img.size, 512)
    return img.resize((int(width), int(height)))


def sticker(fn):
    """
    fn : filename (*.jpg, *.png etc..)
    """
    img = sticker_scaler(fn)
    new_layer = Image.new("RGBA", (512, 512), color=(0, 0, 0, 0))
    new_layer.paste(img, (256 - (int(img.width / 2)), 256 - (int(img.height / 2))))
    return new_layer
