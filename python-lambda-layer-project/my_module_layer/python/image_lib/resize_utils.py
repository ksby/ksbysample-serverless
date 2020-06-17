from PIL import Image

thumbnail_size = 320, 180


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(thumbnail_size)
        image.save(resized_path)
