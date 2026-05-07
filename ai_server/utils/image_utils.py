from PIL import Image


def load_image(path):
    return Image.open(path).convert("RGB")
